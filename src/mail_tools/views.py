from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse

from accounts.models import Account
from commons.mail_wrapper import send_email_with_template

from .forms import BroadcastEmailForm
from .registry import all_previews, get_preview


@staff_member_required
def preview_list(request: HttpRequest) -> HttpResponse:
    return render(request, "mail_tools/list.html", {"previews": list(all_previews())})


@staff_member_required
def preview_detail(request: HttpRequest, slug: str) -> HttpResponse:
    try:
        preview = get_preview(slug)
    except LookupError as exc:
        raise Http404(str(exc))

    context = {"__preview": preview, **preview.context}
    return TemplateResponse(request, preview.template_name, context)


@staff_member_required
def broadcast_email(request: HttpRequest) -> HttpResponse:
    form = BroadcastEmailForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        preview = form.get_preview()
        body_override = form.cleaned_data.get("body_html")
        subject = form.cleaned_data["subject"]
        recipients = form.cleaned_data["recipients"]

        _send_broadcast(preview, subject, body_override, recipients)

        messages.success(request, f"Queued email using '{preview.label}' for {recipients.count()} recipient(s).")
        return redirect(reverse("mail_tools:broadcast"))

    return render(
        request,
        "mail_tools/broadcast.html",
        {
            "form": form,
        },
    )


def _send_broadcast(preview, subject: str, body_override: str | None, recipients) -> None:
    for account in recipients:
        if not isinstance(account, Account):
            continue
        context = preview.build_context(user_name=account.username, overrides={"body_html": body_override})
        send_email_with_template(account.email, subject, preview.template_name, context)
