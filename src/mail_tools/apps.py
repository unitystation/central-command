from django.apps import AppConfig


class MailToolsConfig(AppConfig):
    name = "mail_tools"
    verbose_name = "Mail Tools"

    def ready(self) -> None:
        # Ensure registry entries are loaded on startup.
        from . import registry  # noqa: F401
