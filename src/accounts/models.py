from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import AccountNameValidator


class Account(AbstractUser):

    email = models.EmailField(verbose_name="Email address", unique=True)
    """ Email address used to login """


    account_identifier = models.CharField(
        verbose_name="Account identifier",
        max_length=28,
        primary_key=True,
        validators=[AccountNameValidator()],
    )
    """ account identifier, unique indentifier that can be used to identify this account (banlists, job bans, etc). Can't be ever changed. """


    username = models.CharField(
        verbose_name="Public username",
        max_length=28,
        unique=False,
        validators=[AccountNameValidator()],
    )
    """ public username, shows in OOC, can be changed whenever. """


    is_verified = models.BooleanField(default=False)
    """ is this account verified to be who they claim to be? Are they famous?!"""


    legacy_id = models.CharField(
        verbose_name="Legacy ID",
        max_length=28,
        blank=True,
        default="null",
    )
    """ legacy id, represents the old strings we used to identify accounts on Firebase. """


    characters_data = models.JSONField(
        verbose_name="Characters data",
        default=dict,
    )
    """ all characters data is here """


    is_authorized_server = models.BooleanField(default=False)
    """Can this account broadcast the server state to the server list api? Can this account write to persistence layer?"""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["account_identifier", "username"]

    def __str__(self):
        return f"{self.account_identifier} as {self.username}"