"""Module providing Folder tables for NearBeach"""

from django.db import models

from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.customer import CustomerForeignKey
from NearBeach.models.kanban_board.kanban_card import KanbanCardForeignKey
from NearBeach.models.organisation import OrganisationForeignKey
from NearBeach.models.project import ProjectForeignKey
from NearBeach.models.request_for_change.request_for_change import RequestForChangeForeignKey
from NearBeach.models.requirement.requirement import RequirementForeignKey
from NearBeach.models.requirement.requirement_item import RequirementItemForeignKey
from NearBeach.models.task import TaskForeignKey


class Folder(
    CommonInfo,
    ProjectForeignKey,
    TaskForeignKey,
    CustomerForeignKey,
    OrganisationForeignKey,
    RequirementForeignKey,
    RequirementItemForeignKey,
    RequestForChangeForeignKey,
    KanbanCardForeignKey,
):
    """Class containing Folder fields"""

    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.description)

    class Meta:
        """Meta definition for Folder model."""

        verbose_name_plural = "Folders"
