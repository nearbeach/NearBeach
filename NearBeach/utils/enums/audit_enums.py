"""Module providing enums for the audit log"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditAction(models.TextChoices):
    """Class of enum options for the kind of change an audit entry records"""

    CREATE = "create", _("Created")
    UPDATE = "update", _("Updated")
    STATUS_CHANGE = "status_change", _("Status changed")
    CLOSE = "close", _("Closed")
    DELETE = "delete", _("Deleted")
    ERASE = "erase", _("Personal data erased")
