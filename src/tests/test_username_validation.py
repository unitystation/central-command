from django.test import TestCase

from accounts.validators import IDENTIFIER_REGEX


class IdentifierRegexTest(TestCase):
    # a valid identifier has at least 3 characters with letters, numbers, dashes, underscores, dots and no other special
    # characters.
    def test_valid_identifier(self):
        valid_identifiers = [
            "username123",
            "user_name",
            "user-name",
            "user.name",
            "user123",
            "123",
            "abc",
        ]

        for identifier in valid_identifiers:
            with self.subTest(identifier=identifier):
                self.assertRegex(identifier, IDENTIFIER_REGEX)

    def test_invalid_identifier(self):
        invalid_identifiers = [
            "us",  # Too short
            "user!",  # Invalid character
            "user@name",  # Invalid character
            "user name",  # Invalid character (space)
        ]

        for identifier in invalid_identifiers:
            with self.subTest(identifier=identifier):
                self.assertNotRegex(identifier, IDENTIFIER_REGEX)
