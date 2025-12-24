"""Module providing Document tables for NearBeach"""
import uuid

from django.db import models
from django.conf import settings

from NearBeach.models import Folder
from NearBeach.models.field.common_info import CommonInfo
from NearBeach.models.organisation.customer import Customer
from NearBeach.private_media import FileStorage
from NearBeach.models.kanban_board.kanban_card import KanbanCard
from NearBeach.models.organisation.organisation import Organisation
from NearBeach.models.request_for_change.request_for_change import RequestForChange
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.project.project import Project
from NearBeach.models.task.task import Task


class Document(CommonInfo):
    """Class containing Document fields."""
    document_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    document_description = models.CharField(max_length=255)
    document_url_location = models.TextField(
        # Contains URLS
        blank=True,
        default="",
    )
    document = models.FileField(blank=True, null=True, storage=FileStorage())
    document_upload_successfully = models.BooleanField(
        default=False,
    )
    is_purged = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.document_description)

    class Meta:
        """Meta definition for Document model."""

        verbose_name_plural = "Documents"


class DocumentPermission(CommonInfo):
    """Class containing Document Permission fields"""
    document_permission_id = models.BigAutoField(primary_key=True)
    document_key = models.ForeignKey(
        "Document",
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
