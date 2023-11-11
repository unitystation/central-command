from django.db import models

from .validators import validate_semantic_version


class Character(models.Model):
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
    """To what account/server is this character related to?"""

    fork_compatibility = models.CharField(
        max_length=25,
        help_text='What fork is this character compatible with? This is a simple string, like "Unitystation" or '
        '"tg".',
        default="Unitystation",
    )

    character_sheet_version = models.CharField(
        max_length=10,
        help_text="What character sheet version is this character compatible with? This should be semantically "
        'versioned, like "1.0.0" or "0.1.0".',
        validators=[validate_semantic_version],
    )

    data = models.JSONField(
        name="data", verbose_name="Character data", help_text="Unstructured character data in JSON format."
    )
    """The character data."""

    def __str__(self):
        return f"{self.account.unique_identifier}'s character"


class Other(models.Model):
    account = models.OneToOneField("accounts.Account", on_delete=models.CASCADE, primary_key=True)
    """To what account/server is this extra unordered persistent data related to?"""

    other_data = models.JSONField(default=dict)
    """The extra unordered persistent data."""

    def __str__(self):
        return f"{self.account.pk}'s other data"


class PolyPhrase(models.Model):
    said_by = models.CharField(max_length=28, blank=True, default="Who knows?")
    """What account identifier said this phrase originally? Can be blank"""

    phrase = models.CharField(max_length=128)

    def __str__(self):
        if self.said_by:
            return f"{self.said_by}: {self.phrase}"
        return f"{self.pk}: {self.phrase}"
