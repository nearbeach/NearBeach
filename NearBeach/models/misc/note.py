"""Module proves Object Note tables for NearBeach"""

from django.db import models

from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.kanban_board.kanban_card import KanbanCardForeignKey
from NearBeach.models.organisation import OrganisationForeignKey
from NearBeach.models.project import ProjectForeignKey
from NearBeach.models.request_for_change.request_for_change import RequestForChangeForeignKey
from NearBeach.models.requirement.requirement import RequirementForeignKey
from NearBeach.models.requirement.requirement_item import RequirementItemForeignKey
from NearBeach.models.task import TaskForeignKey


class ObjectNote(
    CommonInfo,
    KanbanCardForeignKey,
    OrganisationForeignKey,
    ProjectForeignKey,
    RequestForChangeForeignKey,
    RequirementForeignKey,
    RequirementItemForeignKey,
    TaskForeignKey,
):
    """Class contains fields for Object Note table"""

    id = models.BigAutoField(primary_key=True)
    note = models.TextField(
        blank=False,
        default="",
    )

    class Meta:
        """Meta definition for ObjectNote"""

        verbose_name_plural = "Object Notes"
