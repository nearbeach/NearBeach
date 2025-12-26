"""Module providing Document tables for NearBeach"""

from django.db import models
from django.conf import settings

from NearBeach.models.customer import CustomerForeignKey
from NearBeach.models.document.document import Document
from NearBeach.models.document.folder import Folder
from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.kanban_board.kanban_card import KanbanCardForeignKey
from NearBeach.models.organisation import OrganisationForeignKey
from NearBeach.models.project import ProjectForeignKey
from NearBeach.models.request_for_change.request_for_change import RequestForChangeForeignKey
from NearBeach.models.requirement.requirement import RequirementForeignKey
from NearBeach.models.requirement.requirement_item import RequirementItemForeignKey
from NearBeach.models.task import TaskForeignKey


class DocumentPermission(
    CommonInfo,
    CustomerForeignKey,
    KanbanCardForeignKey,
    ProjectForeignKey,
    OrganisationForeignKey,
    RequestForChangeForeignKey,
    RequirementForeignKey,
    RequirementItemForeignKey,
    TaskForeignKey,
):
    """Class containing Document Permission fields"""

    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    new_object = models.UUIDField(
        blank=True,
        null=True,
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_profile_picture = models.BooleanField(
        default=False,
    )
    is_purged = models.BooleanField(
        default=False,
    )

    class Meta:
        """Meta definition for Document Permission model."""

        verbose_name_plural = "Document Permissions"
