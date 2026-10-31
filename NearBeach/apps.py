from __future__ import unicode_literals

from django.apps import AppConfig


class NearBeachConfig(AppConfig):
    name = "NearBeach"

    def ready(self):
        # Register the signal handlers that clear the cached initial data
        from NearBeach.utils import initial_data_cache  # noqa: F401
