from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError
from django.db.models import Model

from accounts.models import Account


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password: str, user: Model | None = None):
        if user is None:
            return

        if not isinstance(user, Account):
            raise Exception(
                f"User is not an instance of Account: {user}. Check if the right user model is being set at settings.py."
            )

        custom_attributes = [
            user.username,
            user.email,
            user.unique_identifier,
        ]

        for attribute in custom_attributes:
            if not attribute or not password:
                continue

            password = password.lower()
            attribute = attribute.lower()

            if password in attribute or attribute in password:
                raise ValidationError(
                    "The password is too similar to the %(verbose_name)s.",
                    code="password_too_similar",
                    params={"verbose_name": attribute},
                )
