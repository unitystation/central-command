from django.db import models


class Other(models.Model):
    account = models.OneToOneField(
        "accounts.Account", on_delete=models.CASCADE, primary_key=True
    )
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
