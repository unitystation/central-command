import re

from django.core.exceptions import ValidationError


def validate_semantic_version(version: str) -> None:
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        raise ValidationError(f"{version} is not a valid semantic version. Format should be: MAJOR.MINOR.PATCH")
