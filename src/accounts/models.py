from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import AccountNameValidator, UsernameValidator


class Account(AbstractUser):
    email = models.EmailField(
        verbose_name="Email address",
        unique=True,
        help_text=(
            "Email address must be unique. It is used to login and confirm the account."
        ),
    )

    account_identifier = models.CharField(
        verbose_name="Account identifier",
        max_length=28,
        primary_key=True,
        validators=[AccountNameValidator()],
        help_text=(
            "Account identifier is used to identify your account. "
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
        help_text=(
            "Is this account verified to be who they claim to be? Are they famous?!"
        ),
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

    characters_data = models.JSONField(
        verbose_name="Characters data",
        default=dict,
        help_text=(
            "Characters data is used to store all the characters associated with this "
            "account."
        ),
    )

    is_authorized_server = models.BooleanField(
        default=False,
        verbose_name="Authorized server",
        help_text=(
            "Can this account broadcast the server state to the server list api? "
            "Can this account write to persistence layer?"
        ),
    )

    verification_token = models.UUIDField(
        verbose_name="Verification token",
        blank=True,
        default=uuid4(),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["account_identifier", "username"]

    def __str__(self):
        return f"{self.account_identifier} as {self.username}"
