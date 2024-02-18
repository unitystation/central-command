from django.test import TestCase

from accounts.validators import IDENTIFIER_REGEX, USERNAME_REGEX


class IdentifierRegexTest(TestCase):
    # a valid identifier has at least 3 characters with letters, numbers, dashes, underscores, dots and no other special
    # characters.
    def test_valid_identifier(self):
        valid_identifiers = ["username123", "user_name", "user-name", "user.name", "user123", "123", "abc"]

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


class UsernameRegexTest(TestCase):
    # a valid username has at least 3 characters, letters, numbers, dashes, underscores, dots, and spaces but no
    # consecutive whitespaces.
    def test_valid_username(self):
        # List of valid usernames
        valid_usernames = [
            "username",
            "user name",
            "user_name",
            "user.name",
            "user-name",
            "user123",
            "123 username",
            "user name123",
            "u n",
            "u.n",
            "u_n",
            "u-n",
        ]

        # Test that each valid username is correctly matched by the USERNAME_REGEX
        for username in valid_usernames:
            with self.subTest(username=username):
                self.assertRegex(username, USERNAME_REGEX)

    def test_invalid_username(self):
        # List of invalid usernames
        invalid_usernames = [
            "us",  # Too short
            "user!name",  # Contains an invalid character
            "user@name",  # Contains an invalid character
            "  username",  # Leading whitespace
            "username  ",  # Trailing whitespace
            "user  name",  # Consecutive whitespaces
        ]

        # Test that each invalid username is not matched by the USERNAME_REGEX
        for username in invalid_usernames:
            with self.subTest(username=username):
                self.assertNotRegex(username, USERNAME_REGEX)
