from django.apps import AppConfig


class OvWagConfig(AppConfig):
    name = 'ov_wag'

    def ready(self):
        from ov_wag.auth import connect_signals  # noqa: PLC0415

        connect_signals()
