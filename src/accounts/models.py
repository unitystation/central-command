from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .validators import AccountNameValidator, UsernameValidator


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
        validators=[UsernameValidator()],
        help_text=(
            "Public username is used to identify your account publicly and shows in "
            "OOC. This can be changed at any time"
        ),
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


class PasswordResetRequestModel(models.Model):
    token = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token} as {self.account} created at {self.created_at}"

    def is_token_valid(self):
        return timezone.now() <= timedelta(minutes=60)
