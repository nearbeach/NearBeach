"""Module providing status enums for NearBeach."""

from django.db import models


class ObjectHigherOrderStatus(models.TextChoices):
    """Class containing Object Higher Order Status."""

    BACKLOG = "Backlog"
    NORMAL = "Normal"
    BLOCKED = "Blocked"
    CLOSED = "Closed"


class SprintStatus(models.TextChoices):
    """Class containing Sprint Status enums"""

    DRAFT = "Draft"
    CURRENT = "Current"
    FINISHED = "Finished"
