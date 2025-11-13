import os
import socket
import tempfile

from pathlib import Path

from aiosmtpd.controller import Controller
from django.core.management import call_command
from django.test import TestCase, override_settings
from post_office import mail
from post_office.models import STATUS, Email


class _InMemorySMTPHandler:
    def __init__(self):
        self.envelopes = []

    async def handle_DATA(self, server, session, envelope):  # noqa: N802 the name is required by aiosmtpd
        self.envelopes.append(envelope)
        return "250 OK"


def _allocate_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    try:
        return sock.getsockname()[1]
    finally:
        sock.close()


class PostOfficeSMTPIntegrationTest(TestCase):
    def setUp(self):
        self.smtp_handler = _InMemorySMTPHandler()
        self.smtp_port = _allocate_port()
        self.smtp_controller = Controller(self.smtp_handler, hostname="127.0.0.1", port=self.smtp_port)
        self.smtp_controller.start()
        self.addCleanup(self.smtp_controller.stop)

    def test_queued_email_is_delivered_via_local_debug_server(self):
        recipients = ["recipient@example.com"]
        sender = "sender@example.com"
        subject = "Queue smoke test"
        body = "Hello from the queue"

        with override_settings(
            EMAIL_BACKEND="post_office.EmailBackend",
            EMAIL_HOST="127.0.0.1",
            EMAIL_PORT=self.smtp_port,
            EMAIL_USE_TLS=False,
            EMAIL_HOST_USER="",
            EMAIL_HOST_PASSWORD="",
        ):
            mail.send(recipients=recipients, sender=sender, subject=subject, message=body)

            self.assertEqual(Email.objects.filter(status=STATUS.queued).count(), 1)

            fd, lockfile_path = tempfile.mkstemp()
            os.close(fd)
            try:
                call_command("send_queued_mail", processes=1, lockfile=lockfile_path, verbosity=0)
            finally:
                Path(lockfile_path).unlink()

        sent_emails = Email.objects.filter(status=STATUS.sent)
        self.assertEqual(sent_emails.count(), 1)
        self.assertEqual(len(self.smtp_handler.envelopes), 1)
        envelope = self.smtp_handler.envelopes[0]
        self.assertEqual(envelope.mail_from, sender)
        self.assertEqual(envelope.rcpt_tos, recipients)
        self.assertIn(subject, envelope.content.decode())
