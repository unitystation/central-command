from collections.abc import Iterable
from typing import cast

from django import forms

from accounts.models import Account

from .registry import TemplatePreview, broadcastable_previews, get_preview


def _preview_choices() -> Iterable[tuple[str, str]]:
    return [(preview.slug, preview.label) for preview in broadcastable_previews()]


class BroadcastEmailForm(forms.Form):
    template_slug = forms.ChoiceField(label="Template")
    subject = forms.CharField(label="Subject", max_length=120)
    body_html = forms.CharField(
        label="Body (HTML)",
        widget=forms.HiddenInput(),
        required=False,
        help_text="Optional rich text body injected into the template (used by the info template).",
    )
    recipients = forms.ModelMultipleChoiceField(
        label="Recipients",
        queryset=Account.objects.none(),
        widget=forms.SelectMultiple(attrs={"size": 12}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        template_field = cast(forms.ChoiceField, self.fields["template_slug"])
        template_field.choices = list(_preview_choices())
        recipients_field = cast(forms.ModelMultipleChoiceField, self.fields["recipients"])
        recipients_field.queryset = Account.objects.order_by("email")
        self.preview: TemplatePreview | None = None

    def clean_template_slug(self) -> str:
        slug = self.cleaned_data["template_slug"]
        try:
            preview = get_preview(slug)
        except LookupError as exc:
            raise forms.ValidationError(str(exc))
        if not preview.allow_broadcast:
            raise forms.ValidationError("This template cannot be used for manual sending.")
        self.preview = preview
        return slug

    def get_preview(self) -> TemplatePreview:
        if self.preview is None:
            raise ValueError("Preview not set. Did you call is_valid()?")
        return self.preview
