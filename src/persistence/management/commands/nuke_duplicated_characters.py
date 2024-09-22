import json
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Account
from persistence.models import Character

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Finds all duplicated characters in the database and deletes them by comparing their JSON data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Dry run mode: shows what would be deleted without actually deleting anything.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if dry_run:
            logger.info("Running nuke duplicated characters command in dry run mode")
        else:
            logger.warning(
                "we are about to run the nuke duplicated characters command! This operation can not be undone."
            )

        total_deleted = 0

        accounts = Account.objects.all()
        for account in accounts:
            character_map = self.get_character_map(account)
            duplicates = self.get_duplicates(character_map)

            if duplicates:
                total_deleted += self.process_duplicates(account, duplicates, dry_run)

        if dry_run:
            logger.info("Dry run completed. No characters were deleted.")
        else:
            logger.info("Total duplicated characters deleted: %d", total_deleted)

    @staticmethod
    def get_character_map(account) -> dict:
        """Returns a dictionary mapping character data (as serialized JSON) to a list of characters."""
        characters = Character.objects.filter(account=account)
        character_map: dict[str, list[Character]] = {}

        for character in characters:
            data_str = json.dumps(character.data, sort_keys=True)
            if data_str in character_map:
                character_map[data_str].append(character)
            else:
                character_map[data_str] = [character]

        return character_map

    @staticmethod
    def get_duplicates(character_map: dict) -> list:
        """Returns a list of duplicate characters for a given character map."""
        return [chars[1:] for chars in character_map.values() if len(chars) > 1]

    def process_duplicates(self, account: Account, duplicates: list, dry_run: bool) -> int:
        """Processes the duplicates, logging and optionally deleting them."""
        total_deleted = 0

        for chars_to_delete in duplicates:
            char_ids = [char.id for char in chars_to_delete]

            if dry_run:
                logger.info(
                    "[Dry run] would delete these duplicated characters for account %s: %s",
                    account.unique_identifier,
                    char_ids,
                )
            else:
                self.delete_characters(account, char_ids)

            total_deleted += len(chars_to_delete)

        return total_deleted

    @staticmethod
    def delete_characters(account, char_ids: list):
        """Deletes the characters with the specified IDs."""
        with transaction.atomic():
            Character.objects.filter(id__in=char_ids).delete()
            logger.warning(
                "Deleted the following characters for account %s: %s",
                account.unique_identifier,
                char_ids,
            )
            logger.warning("This operation cannot be undone; they are gone forever...")
