"""Module provides notification enums for NearBeach"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationLocation(models.TextChoices):
    ALL_OPTIONS = "all", _("All Options")
    DASHBOARD = "dashboard", _("Dashboard Screen")
    LOGIN = "login", _("Login Screen")


NOTIFICATION_LOCATION = (
    ("all", "All Options"),
    ("dashboard", "Dashboard Screen"),
    ("login", "Login Screen"),
)
