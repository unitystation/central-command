from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError

from accounts.models import Account


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password: str, user: Account | None = None):  # type: ignore
        if not user:
            return

        custom_attributes = [user.username, user.email, getattr(user, "unique_identifier", "")]
        for attribute in custom_attributes:
            if not attribute or not password:
                continue
            if password.lower() in attribute.lower() or attribute.lower() in password.lower():
                raise ValidationError(
                    "The password is too similar to the %(verbose_name)s.",
                    code="password_too_similar",
                    params={"verbose_name": attribute},
                )
