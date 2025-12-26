"""Module providing tables for misc functionality in NearBeach."""

import uuid

from django.db import models
from django.conf import settings
from knox.models import AuthToken

from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.kanban_board.kanban_board import KanbanBoardForeignKey
from NearBeach.models.kanban_board.kanban_card import KanbanCardForeignKey
from NearBeach.models.permission.group import Group
from NearBeach.models.project import ProjectForeignKey
from NearBeach.models.request_for_change.request_for_change import RequestForChangeForeignKey
from NearBeach.models.requirement.requirement import RequirementForeignKey
from NearBeach.models.requirement.requirement_item import RequirementItemForeignKey
from NearBeach.models.task import TaskForeignKey
from NearBeach.utils.enums.notification_enums import NotificationLocation
from NearBeach.utils.enums.object_enums import ObjectTemplateType
from NearBeach.utils.enums.scheduled_object_enums import ScheduledObjectEnum


class ExtendsAuthToken(AuthToken):
    """Class Extends AuthToken."""

    description = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )
    change_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )


class Notification(CommonInfo):
    """
    Class contains fields for Notification tables

    Administrator can utilise this field to store notifications to tell users.
    Notifications can appear on;
    - Login screen
    - Dashboard
    """

    id = models.BigAutoField(primary_key=True)
    header = models.CharField(
        blank=False,
        null=False,
        max_length=255,
    )
    message = models.TextField(
        blank=True,
        default="",
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(
        max_length=20,
        choices=NotificationLocation,
        default=NotificationLocation.ALL_OPTIONS,
    )

    class Meta:
        """Meta definition for Notification table."""

        verbose_name_plural = "Notifications"


class ObjectTemplate(CommonInfo):
    """Class contains fields for ObjectTemplate table"""

    id = models.BigAutoField(primary_key=True)
    type = models.IntegerField(
        choices=ObjectTemplateType,
    )
    json = models.JSONField()

    class Meta:
        """Meta definition for ObjectTemplate table."""

        verbose_name_plural = "Object Templates"


class ObjectTemplateGroup(CommonInfo):
    """Class contains fields for ObjectTemplateGroup table"""

    id = models.BigAutoField(primary_key=True)
    object_template = models.ForeignKey(
        ObjectTemplate,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for ObjectTemplateGroup table."""

        verbose_name_plural = "Object Template Groups"


class PublicLink(
    CommonInfo,
    KanbanBoardForeignKey,
    KanbanCardForeignKey,
    ProjectForeignKey,
    RequestForChangeForeignKey,
    RequirementForeignKey,
    RequirementItemForeignKey,
    TaskForeignKey,
):
    """Class contains fields for PublicLink table"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        """Meta definition for PublicLink table."""

        verbose_name_plural = "Public Links"


class ScheduledObject(CommonInfo):
    """Class contains fields for ScheduledObject table"""

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    last_run = models.DateField(
        blank=True,
        null=True,
    )
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True,
        null=True,
    )
    next_scheduled_run = models.DateField(
        blank=True,
        null=True,
    )
    number_of_repeats = models.IntegerField(default=-1)
    run_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    frequency = models.CharField(
        choices=ScheduledObjectEnum,
        max_length=50,
    )
    frequency_attribute = models.JSONField(
        null=True,
        blank=True,
    )
    object_template = models.ForeignKey(
        ObjectTemplate,
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for ScheduledObject table."""

        verbose_name_plural = "Scheduled Objects"
