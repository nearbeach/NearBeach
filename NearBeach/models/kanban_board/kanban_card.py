"""Module providing Kanban Card tables for NearBeach."""

from django.db import models

from NearBeach.models.common_info import CommonInfo
from NearBeach.models.kanban_board.kanban_board import (
    KanbanBoard,
    KanbanColumn,
    KanbanLevel,
)
from NearBeach.models.project import Project
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.task import Task
from NearBeach.utils.enums.object_enums import ObjectPriority


class KanbanCard(CommonInfo):
    """Class containing Kanban Card fields."""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        default="",
    )
    sort_number = models.IntegerField()
    kanban_level = models.ForeignKey(
        KanbanLevel,
        on_delete=models.CASCADE,
    )
    kanban_column = models.ForeignKey(
        KanbanColumn,
        on_delete=models.CASCADE,
    )
    kanban_board = models.ForeignKey(
        KanbanBoard,
        on_delete=models.CASCADE,
    )
    priority = models.IntegerField(
        choices=ObjectPriority,
        default=ObjectPriority.NORMAL,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement_item = models.ForeignKey(
        RequirementItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_archived = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        """Meta definition for Kanban Card model."""

        verbose_name_plural = "Kanban Cards"
        ordering = ["-id"]
