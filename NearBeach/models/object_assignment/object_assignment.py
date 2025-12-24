"""Module providing object assignment tables for NearBeach."""

from django.db import models
from django.conf import settings

from NearBeach.models import KanbanBoard, KanbanCard, Customer
from NearBeach.models.common_info import CommonInfo
from NearBeach.models.organisation import Organisation
from NearBeach.models.permission.group import Group
from NearBeach.models.project import Project
from NearBeach.models.request_for_change.change_task import ChangeTask
from NearBeach.models.request_for_change.request_for_change import RequestForChange
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.task import Task
from NearBeach.utils.enums.object_enums import ObjectLinkRelationship


class ObjectAssignment(CommonInfo):
    """
    Class containing fields for the Object Assignment table.

    Object permissions is the centralised permissions for all objects
    - Requirement
    - Project
    - Task
    - Kanban board
    - Request for change
    - Card

    These permission are only "ACCESS" permissions.
    The user/group's over-riding permissions determine if
    the user can add, edit etc.
    """

    id = models.BigAutoField(primary_key=True)
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_assigned_user",
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        Group,
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
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    kanban_board = models.ForeignKey(
        KanbanBoard,
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
    request_for_change = models.ForeignKey(
        RequestForChange,
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
    change_task = models.ForeignKey(
        ChangeTask,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    meta_object = models.BigIntegerField(
        blank=True,
        null=True,
    )
    meta_object_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )
    meta_object_status = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )
    link_relationship = models.CharField(
        max_length=10,
        choices=ObjectLinkRelationship,
        blank=True,
        default="",
    )
    parent_link = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    class Meta:
        """Meta definitions for the object assignment table"""
        verbose_name_plural = "Object Assignment Tables"
