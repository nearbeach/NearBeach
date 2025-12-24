"""Module providing Kanban Board tables for NearBeach"""

from django.db import models

from NearBeach.models.field.common_info import CommonInfo
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.utils.enums.kanban_board_enums import KanbanBoardStatusChoice
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class KanbanBoard(CommonInfo):
    """Class containing Kanban Board status choices."""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        Requirement,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=10,
        choices=KanbanBoardStatusChoice,
        default="Open",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        """Meta for Kanban Board model."""

        verbose_name_plural = "Kanban Boards"
        ordering = ["-id"]


class KanbanColumn(CommonInfo):
    """Class containing Kanban Column fields."""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    property = models.CharField(
        max_length=10,
        choices=ObjectHigherOrderStatus,
        default="Normal",
    )
    sort_number = models.IntegerField()
    kanban_board = models.ForeignKey(
        KanbanBoard,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        """Meta for Kanban Column model."""

        verbose_name_plural = "Kanban Columns"
        ordering = ["sort_number", "id"]


class KanbanLevel(CommonInfo):
    """Class containing Kanban Level fields."""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    sort_number = models.IntegerField()
    kanban_board = models.ForeignKey(
        "KanbanBoard",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        """Meta for Kanban Level model."""

        verbose_name_plural = "Kanban Levels"
        ordering = ["sort_number", "id"]
