from django.core.management.base import BaseCommand

from accounts.models import Account
from server.models import AccountModerationInfo


class Command(BaseCommand):
    help = "creates AccountModerationInfo for existing accounts"

    def handle(self, *args, **options):
        for account in Account.objects.all():
            AccountModerationInfo.objects.get_or_create(account=account)
        self.stdout.write(self.style.SUCCESS("Successfully created AccountModerationInfo for all accounts"))
