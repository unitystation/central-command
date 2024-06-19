import secrets
import string

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import Account


class CodeScanInformation(models.Model):
    version = models.TextField(primary_key=True)

    def __str__(self):
        return self.version


def generate_listing_key():
    alphabet = string.ascii_letters + string.digits + "-_"
    return "".join(secrets.choice(alphabet) for _ in range(30))


class ServerInformation(models.Model):
    owner = models.ForeignKey(
        verbose_name="Owner",
        to=Account,
        on_delete=models.CASCADE,
        help_text="Who created and/or is responsible for this server",
    )
    name = models.TextField(
        verbose_name="Name",
        max_length=50,
        help_text="Name this server uses to present itself in the servers list",
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=200,
        help_text="A brief description of what this server is about",
    )
    icon = models.URLField(
        verbose_name="Icon",
        blank=True,
        help_text="URL of the image this server uses to present itself in the servers list",
    )
    rules = models.TextField(
        verbose_name="Rules",
        blank=True,
        help_text="The rules that players must follow on this server",
    )
    motd = models.TextField(
        verbose_name="Message of the Day (MOTD)",
        help_text="Message displayed to players when they join the server",
    )
    is_18_plus = models.BooleanField(
        verbose_name="18+",
        default=False,
        help_text="Indicates if this server is intended for players aged 18 and above",
    )
    code_scan_version = models.ForeignKey(
        verbose_name="CodeScan Version",
        to=CodeScanInformation,
        on_delete=models.PROTECT,
        help_text="What version should this build of the game be tested against in CodeScan",
    )
    is_delisted = models.BooleanField(
        verbose_name="Is Delisted",
        help_text="Indicates if this server is delisted from the servers list",
    )
    listing_key = models.TextField(
        unique=True,
        verbose_name="Listing Key",
        null=True,
        blank=True,
        help_text="A unique key used for listing this server. Do not lose this key!",
    )

    def __str__(self):
        return f"Server: {self.name} by: {self.owner.unique_identifier}"


@receiver(pre_save, sender=ServerInformation)
def set_listing_key(sender, instance: ServerInformation, **kwargs):
    if not instance.listing_key:
        unique_key_found = False
        while not unique_key_found:
            new_key = generate_listing_key()
            if not ServerInformation.objects.filter(listing_key=new_key).exists():
                instance.listing_key = new_key
                unique_key_found = True


# class ServerStatus(models.Model):
#     server = models.ForeignKey(
#         ServerInformation, related_name="status", on_delete=models.CASCADE
#     )
#     is_passworded = models.BooleanField()
#     fork_name = models.TextField()
#     build_version = models.TextField()
#     current_map = models.TextField()
#     game_mode = models.TextField()
#     ingame_time = models.TextField()
#     round_time = models.TextField()
#     player_count = models.PositiveSmallIntegerField()
#     player_count_max = models.PositiveSmallIntegerField()
#     ip = models.TextField()
#     port = models.PositiveSmallIntegerField()
#     windows_download = models.URLField()
#     osx_download = models.URLField()
#     linux_download = models.URLField()
#     fps = models.PositiveSmallIntegerField()


class AccountModerationInfo(models.Model):
    account = models.OneToOneField(to=Account, related_name="moderation_info", on_delete=models.CASCADE)
    can_create_servers = models.BooleanField(default=True)
    can_list_servers = models.BooleanField(default=True)

    def __str__(self):
        return f"Moderation for {self.account.unique_identifier}"


class ServerAdmonition(models.Model):
    SEVERITY_LEVELS = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    owner_moderation = models.ForeignKey(AccountModerationInfo, related_name="admonitions", on_delete=models.CASCADE)
    server = models.ForeignKey(
        ServerInformation,
        related_name="admonitions",
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        help_text="When was this admonition created",
    )
    reason = models.TextField(verbose_name="Reason", help_text="Why was this server warned?")
    severity = models.CharField(
        max_length=6,
        choices=SEVERITY_LEVELS,
        default="low",
        help_text="The severity level of the admonition",
    )

    def __str__(self):
        return f"[{self.get_severity_display()}]: {self.reason}"
