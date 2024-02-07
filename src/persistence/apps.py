from django.apps import AppConfig


class PersistenceConfig(AppConfig):
    name = "persistence"

    def ready(self):
        import commons.schema  # noqa: F401
