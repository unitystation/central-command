import logging

from datetime import timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand

from accounts.models import ConnectionChallenge

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Delete expired connection challenges (older than 3 minutes)"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(minutes=3)
        deleted, _ = ConnectionChallenge.objects.filter(created_at__lt=cutoff).delete()
        logger.info(f"Deleted {deleted} expired connection challenges.")