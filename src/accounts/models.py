from datetime import timedelta
from secrets import token_urlsafe
from urllib.parse import urljoin
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from commons.mail_wrapper import send_email_with_template

from .validators import AccountNameValidator


class Account(AbstractUser):
    email = models.EmailField(
        verbose_name="Email address",
        unique=True,
        help_text="Email address must be unique. It is used to login and confirm the account.",
    )

    unique_identifier = models.CharField(
        verbose_name="Unique identifier",
        max_length=28,
        primary_key=True,
        validators=[AccountNameValidator()],
        help_text=(
            "Unique identifier is used to identify your account. "
            "This will be used for bans, job bans, etc and can't ever be changed"
        ),
    )

    username = models.CharField(
        verbose_name="Public username",
        max_length=28,
        unique=False,
        validators=[MinLengthValidator(3), UnicodeUsernameValidator()],
        help_text=(
            "Public username is used to identify your account publicly and shows in "
            "OOC. This can be changed at any time"
        ),
    )

    is_confirmed = models.BooleanField(
        default=False,
        verbose_name="Confirmed",
        help_text="Has this account been confirmed via email?",
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verified",
        help_text="Is this account verified to be who they claim to be? Are they famous?!",
    )

    legacy_id = models.CharField(
        verbose_name="Legacy ID",
        max_length=28,
        blank=True,
        default="null",
        help_text=(
            "Legacy ID is used to identify your account in the old database. "
            "This is used for bans, job bans, etc and can't ever be changed"
        ),
    )

    verification_token = models.UUIDField(
        verbose_name="Verification token",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["unique_identifier", "username"]

    def save(self, *args, **kwargs):
        if self.verification_token is None:
            self.verification_token = uuid4()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unique_identifier} as {self.username}"

    def send_confirmation_mail(self):
        confirmation_token = token_urlsafe(32)

        previous_confirmations = AccountConfirmation.objects.filter(account=self)
        previous_confirmations.delete()

        AccountConfirmation.objects.create(
            token=confirmation_token,
            account=self,
        )

        send_email_with_template(
            recipient=self.email,
            subject="Confirm your account",
            template="confirm_template.html",
            context={
                "user_name": self.username,
                "link": urljoin(settings.ACCOUNT_CONFIRMATION_URL, confirmation_token),
            },
        )


class AccountConfirmation(models.Model):
    token = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Account confirmation request for {self.account} created at {self.created_at}"

    def is_token_valid(self):
        if self.created_at is None:
            return False
        return (self.created_at + timedelta(hours=settings.ACCOUNT_CONFIRMATION_TOKEN_TTL)) > timezone.now()


class PasswordResetRequestModel(models.Model):
    token = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset request for {self.account} created at {self.created_at}"

    def is_token_valid(self):
        if self.created_at is None:
            return False
        return (self.created_at + timedelta(minutes=settings.PASS_RESET_TOKEN_TTL)) > timezone.now()
