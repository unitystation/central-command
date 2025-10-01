import logging

from datetime import timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand

from accounts.models import SHA512Token

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete expired SHA512 tokens (older than 3 minutes)"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(minutes=3)
        deleted, _ = SHA512Token.objects.filter(created_at__lt=cutoff).delete()
        self.stdout.write(f"Deleted {deleted} expired SHA512 tokens.")
