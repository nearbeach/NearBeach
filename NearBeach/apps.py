from __future__ import unicode_literals

from django.apps import AppConfig


class NearBeachConfig(AppConfig):
    name = "NearBeach"

    def ready(self):
        # Register the signal handlers that clear the cached initial data
        from NearBeach.utils import initial_data_cache  # noqa: F401

        # The admin login is a second way in - give it the same throttle and two-factor check as the main login
        from django.contrib import admin
        from NearBeach.utils.secure_admin import harden_admin_site
        harden_admin_site(admin.site)
