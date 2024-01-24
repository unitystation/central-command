from django.conf import settings
from django.template.loader import render_to_string
from post_office import mail


def send_email_with_template(recipient: str, subject: str, template: str, context: dict) -> None:
    email_subject = f"Unitystation: {subject}"
    email_body = render_to_string(template, context)
    mail.send(
        recipients=[recipient],
        subject=email_subject,
        html_message=email_body,
        sender=settings.EMAIL_HOST_USER,
    )
