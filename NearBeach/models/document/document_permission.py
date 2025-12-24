"""Module providing Document tables for NearBeach"""
from django.db import models
from django.conf import settings

from NearBeach.models import Folder, Document
from NearBeach.models.common_info import CommonInfo
from NearBeach.models.customer import Customer
from NearBeach.models.kanban_board.kanban_card import KanbanCard
from NearBeach.models.organisation import Organisation
from NearBeach.models.request_for_change.request_for_change import RequestForChange
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.project import Project
from NearBeach.models.task import Task


class DocumentPermission(CommonInfo):
    """Class containing Document Permission fields"""
    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        Project,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    organisation = models.ForeignKey(
        Organisation,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        Customer,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    requirement = models.ForeignKey(
        Requirement,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    requirement_item = models.ForeignKey(
        RequirementItem,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    request_for_change = models.ForeignKey(
        RequestForChange,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    kanban_card = models.ForeignKey(
        KanbanCard,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_TABLE,
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
