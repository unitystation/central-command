from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from uuid import uuid4

from django.core import signing
from django.db import models

from accounts.models import Account
from commons.cache import get_baby_server_heartbeat

SERVERLIST_TOKEN_SALT = "baby_serverlist.serverlist_token"


class BabyServer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    serverlist_token = models.TextField(unique=True, editable=False)
    whitelisted = models.BooleanField(default=False)
    owner = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="baby_servers",
    )
    objects = models.Manager()

    def __str__(self) -> str:
        return f"BabyServer(id={self.id}, owner={self.owner.unique_identifier})"

    def save(self, *args, **kwargs):
        if not self.serverlist_token:
            self.serverlist_token = self.generate_serverlist_token()
        super().save(*args, **kwargs)

    def generate_serverlist_token(self) -> str:
        """Create a signed token that uniquely identifies this server and can be validated by clients."""
        payload = {
            "server_id": str(self.id),
            "owner_id": str(self.owner.unique_identifier),
            "nonce": token_urlsafe(16),
        }
        return signing.dumps(payload, salt=SERVERLIST_TOKEN_SALT)

    def is_live(self) -> bool:
        """Return True when the server has reported within the last 12 seconds."""
        heartbeat_iso = get_baby_server_heartbeat(str(self.id))
        if not heartbeat_iso:
            return False
        try:
            heartbeat_time = datetime.fromisoformat(heartbeat_iso)
        except ValueError:
            return False
        if heartbeat_time.tzinfo is None:
            heartbeat_time = heartbeat_time.replace(tzinfo=UTC)
        return datetime.now(tz=UTC) - heartbeat_time <= timedelta(seconds=12)
