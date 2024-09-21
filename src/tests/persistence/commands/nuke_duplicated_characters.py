import json

from django.core.management import call_command
from django.test import TestCase

from accounts.models import Account
from persistence.models import Character


class DeleteDuplicateCharactersCommandTest(TestCase):
    def setUp(self):
        # Create two test accounts
        self.account1 = Account.objects.create(
            unique_identifier="testuser1", username="testuser1", email="user1@test.com"
        )
        self.account2 = Account.objects.create(
            unique_identifier="testuser2", username="testuser2", email="user2@test.com"
        )

        # Define character data
        data_unique1 = {"Name": "Unique Character", "Age": 30}
        data_unique2 = {"Name": "Unique Character", "Age": 25}
        data_duplicate = {"Name": "Duplicate Character", "Age": 40}

        # Add characters to account1
        Character.objects.create(account=self.account1, data=data_unique1)
        Character.objects.create(account=self.account1, data=data_unique2)
        Character.objects.create(account=self.account1, data=data_duplicate)
        Character.objects.create(account=self.account1, data=data_duplicate)

        # Add characters to account2
        Character.objects.create(account=self.account2, data=data_unique1)
        Character.objects.create(account=self.account2, data=data_unique2)
        Character.objects.create(account=self.account2, data=data_duplicate)
        Character.objects.create(account=self.account2, data=data_duplicate)

    def test_delete_duplicate_characters_command(self):
        # Verify initial character counts
        self.assertEqual(Character.objects.filter(account=self.account1).count(), 4)
        self.assertEqual(Character.objects.filter(account=self.account2).count(), 4)

        # Run the command in dry-run mode
        call_command("nuke_duplicated_characters", "--dry-run")

        # Ensure no characters were deleted in dry-run mode
        self.assertEqual(Character.objects.filter(account=self.account1).count(), 4)
        self.assertEqual(Character.objects.filter(account=self.account2).count(), 4)

        # Run the command without dry-run to delete duplicates
        call_command("nuke_duplicated_characters")

        # Verify duplicates are deleted
        self.assertEqual(Character.objects.filter(account=self.account1).count(), 3)
        self.assertEqual(Character.objects.filter(account=self.account2).count(), 3)

        # Collect remaining character data for account1
        remaining_data_account1 = Character.objects.filter(account=self.account1).values_list("data", flat=True)
        data_strings_account1 = [json.dumps(data, sort_keys=True) for data in remaining_data_account1]
        self.assertEqual(len(set(data_strings_account1)), 3)  # Should be 3 unique characters

        # Collect remaining character data for account2
        remaining_data_account2 = Character.objects.filter(account=self.account2).values_list("data", flat=True)
        data_strings_account2 = [json.dumps(data, sort_keys=True) for data in remaining_data_account2]
        self.assertEqual(len(set(data_strings_account2)), 3)  # Should be 3 unique characters
