from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.deconstruct import deconstructible


@deconstructible()
class AccountNameValidator(ASCIIUsernameValidator):
    regex = r"^[\w\s@+-]+\Z"
    message = (
        "Enter a valid username. This value may contain only English letters, "
        "numbers, spaces, and +/-/_ characters."
    )