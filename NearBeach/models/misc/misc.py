"""Module providing tables for misc functionality in NearBeach."""
from django.db import models
from django.conf import settings
from knox.models import AuthToken

from NearBeach.models.field.common_info import CommonInfo


class ExtendsAuthToken(AuthToken):
    """Class Extends AuthToken."""

    description = models.CharField(max_length=255, blank=True)
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

    notification_id = models.BigAutoField(primary_key=True)
    notification_header = models.CharField(
        blank=False,
        null=False,
        max_length=255,
    )
    notification_message = models.TextField(
        blank=True,
        default="",
    )
    notification_start_date = models.DateTimeField()
    notification_end_date = models.DateTimeField()
    notification_location = models.CharField(
        max_length=20,
        choices=NOTIFICATION_LOCATION,
        default="All",
    )


class ObjectTemplate(CommonInfo):
    object_template_id = models.BigAutoField(primary_key=True)
    object_template_type = models.IntegerField(
        choices=OBJECT_TEMPLATE_TYPE,
    )
    object_template_json = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class ObjectTemplateGroup(CommonInfo):
    object_template_group_id = models.BigAutoField(primary_key=True)
    object_template = models.ForeignKey(
        "ObjectTemplate",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class PublicLink(CommonInfo):
    public_link_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    public_link_is_active = models.BooleanField(
        default=True,
    )
    requirement = models.ForeignKey(
        "Requirement",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    kanban_board = models.ForeignKey(
        "KanbanBoard",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    kanban_card = models.ForeignKey(
        "KanbanCard",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    creation_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.public_link_id)


class ScheduledObject(CommonInfo):
    schedule_object_id = models.BigAutoField(primary_key=True)
    schedule_object_title = models.CharField(max_length=255)
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
        choices=SCHEDULED_OBJECT_FREQUENCY,
        max_length=50,
    )
    frequency_attribute = models.JSONField(
        null=True,
        blank=True,
    )
    object_template = models.ForeignKey(
        "ObjectTemplate",
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )
