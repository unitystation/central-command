from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.deconstruct import deconstructible


@deconstructible()
class AccountNameValidator(ASCIIUsernameValidator):
    # match account identifier that only has letters, numbers, dash, underscore
    # and at least 3 characters
    regex = r"^[a-zA-Z0-9_\-]{3,}$"
    message = (
        "Enter a valid account identifier. This value may contain only English "
        "letters, numbers, and -/_ characters."
    )


@deconstructible()
class UsernameValidator(ASCIIUsernameValidator):
    # match username that has at least 3 characters, letters, numbers, dashes,
    # underscores, dots, and spaces but no consecutive whitespaces
    regex = r"^[a-zA-Z0-9\.\-_](?!.* {2})[ \w.-_]{2,}$"
    message = (
        "Enter a valid username. This value may contain only English letters, "
        "numbers, dashes, underscores, dots, and spaces."
    )
