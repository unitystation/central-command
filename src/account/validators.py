import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.contrib.auth.validators import ASCIIUsernameValidator


@deconstructible()
class AccountNameValidator(ASCIIUsernameValidator):
    regex = r"^[\w\s@+-]+\Z"
    message = (
        "Enter a valid username. This value may contain only English letters, "
        "numbers, spaces, and +/-/_ characters."
    )


@deconstructible()
class NoBadWordsValidator(validators.RegexValidator):
    badwords: str
    inverse_match = True
    flags = re.IGNORECASE
    message = (
        "Please don't use slurs or bad words for your username."
        "\nUnitystation is meant to be a fun place for everyone!"
    )

    def __call__(self, value):
        self.generate_bad_words_regex()
        super().__call__(value)

    def generate_bad_words_regex(self):
        formatted_regex = r"[\w@+-_]*({0})[\w@+-_]*"  # todo this regex might be weak af, improve if you know how

        try:
            with open("badwords.txt", "r", encoding="UTF-8") as f:
                bad_list = f.readlines()
        except FileNotFoundError:
            self.regex = None
            self.inverse_match = False
            return
        bad_list = [w.replace("\n", "").strip() for w in bad_list]
        self.regex = re.compile(formatted_regex.format("|".join(bad_list)), self.flags)
