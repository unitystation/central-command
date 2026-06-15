from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Optional

from django.conf import settings


@dataclass(frozen=True)
class TemplatePreview:
    slug: str
    label: str
    template_name: str
    context: dict[str, Any]
    allow_broadcast: bool = False

    def build_context(
        self,
        *,
        user_name: Optional[str] = None,
        overrides: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        data = deepcopy(self.context)
        if user_name:
            data["user_name"] = user_name
        if overrides:
            data.update({k: v for k, v in overrides.items() if v not in (None, "")})
        return data


_registry: dict[str, TemplatePreview] = {}


def register(preview: TemplatePreview) -> None:
    if preview.slug in _registry:
        raise ValueError(f"Duplicate mail preview slug '{preview.slug}'")
    _registry[preview.slug] = preview


def all_previews() -> Iterable[TemplatePreview]:
    return _registry.values()


def broadcastable_previews() -> Iterable[TemplatePreview]:
    return (preview for preview in _registry.values() if preview.allow_broadcast)


def get_preview(slug: str) -> TemplatePreview:
    try:
        return _registry[slug]
    except KeyError as exc:
        raise LookupError(f"No mail preview registered for '{slug}'") from exc


register(
    TemplatePreview(
        slug="confirm-account",
        label="Account confirmation",
        template_name="confirm_template.html",
        context={
            "user_name": "Alex Crew",
            "link": f"{settings.ACCOUNT_CONFIRMATION_URL}?token=example-token",
        },
    )
)

register(
    TemplatePreview(
        slug="password-reset",
        label="Password reset",
        template_name="password_reset.html",
        context={
            "user_name": "Alex Crew",
            "link": f"{settings.PASS_RESET_URL}?token=example-token",
        },
    )
)

register(
    TemplatePreview(
        slug="info",
        label="Informational message",
        template_name="info_template.html",
        context={
            "user_name": "Alex Crew",
            "body_html": "<p>We wanted to let you know that scheduled maintenance will occur on <strong>Saturday at 18:00 UTC</strong>. Servers may be unavailable for roughly 30 minutes.</p><p>Thanks for your patience!</p>",
        },
        allow_broadcast=True,
    )
)
