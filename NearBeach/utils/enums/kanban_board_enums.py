"""Module providing enums for Kanban Board."""

from django.db import models


class KanbanBoardStatusChoice(models.TextChoices):
    """Class containing Kanban Board status choices."""

    OPEN = "Open"
    CLOSED = "Closed"
