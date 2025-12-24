"""Module providing Folder tables for NearBeach"""

from django.db import models

from NearBeach.models.common_info import CommonInfo
from NearBeach.models.customer import Customer
from NearBeach.models.kanban_board.kanban_card import KanbanCard
from NearBeach.models.organisation import Organisation
from NearBeach.models.request_for_change.request_for_change import RequestForChange
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.project import Project
from NearBeach.models.task import Task


class Folder(CommonInfo):
    """Class containing Folder fields"""

    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        RequirementItem,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        RequestForChange,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    kanban_card = models.ForeignKey(
        KanbanCard,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    folder_description = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.folder_description)

    class Meta:
        """Meta definition for Folder model."""

        verbose_name_plural = "Folders"
