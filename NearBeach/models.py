from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .private_media import FileStorage
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings


# If user has overwritten the AUTH_USER_MODEL, user that. Otherwise default to User
USER_MODEL = getattr(settings, "AUTH_USER_MODEL", User)

# ENUM choices
DISCOUNT_CHOICE = (
    ("Percentage", "Percentage"),
    ("Amount", "Amount"),
)

KANBAN_BOARD_STATUS_CHOICE = (
    ("Open", "Open"),
    ("Closed", "Closed"),
)

KANBAN_CARD_PRIORITY = (
    (0, "Highest"),
    (1, "High"),
    (2, "Normal"),
    (3, "Low"),
    (4, "Lowest"),
)

LINK_RELATIONSHIP = (
    ("block", "Block"),
    ("duplicate", "Duplicate"),
    ("relate", "Relate"),
    ("subobject", "Subobject"),
)

NOTIFICATION_LOCATION = (
    ("all", "All Options"),
    ("dashboard", "Dashboard Screen"),
    ("login", "Login Screen"),
)

OBJECT_HIGHER_ORDER_STATUS = (
    ("Backlog", "Backlog"),
    ("Normal", "Normal"),
    ("Blocked", "Blocked"),
    ("Closed", "Closed"),
)

PAGE_LAYOUT = (
    ("Landscape", "Landscape"),
    ("Portrait", "Portrait"),
)

PARENT_LINK = (
    ("change_task", "change_task"),
    ("kanban_card", "kanban_card"),
    ("requirement", "requirement"),
    ("requirement_item", "requirement_item"),
    ("request_for_change", "request_for_change"),
    ("project", "project"),
    ("task", "task"),
)

PERMISSION_LEVEL = (
    (0, "No Permission"),
    (1, "Read Only"),
    (2, "Edit Only"),
    (3, "Add and Edit"),
    (4, "Full Permission"),
)

PERMISSION_BOOLEAN = (
    (0, "No Permission"),
    (1, "Has Permission"),
)

PROJECT_STATUS_CHOICE = (
    ("New", "New"),
    ("Backlog", "Backlog"),
    ("Blocked", "Blocked"),
    ("In Progress", "In Progress"),
    ("Test/Review", "Test/Review"),
    ("Closed", "Closed"),
)


RATING_SCORE = (
    (1, "1 Star"),
    (2, "2 Star"),
    (3, "3 Star"),
    (4, "4 Star"),
    (5, "5 Star"),
)

RFC_APPROVAL = (
    (1, "Waiting"),
    (2, "Approved"),
    (3, "Rejected"),
    (4, "Cancel"),
)

RFC_IMPACT = (
    (3, "High"),
    (2, "Medium"),
    (1, "Low"),
)

RFC_PRIORITY = (
    (4, "Critical"),
    (3, "High"),
    (2, "Medium"),
    (1, "Low"),
)

RFC_RISK = (
    (5, "Very High"),
    (4, "High"),
    (3, "Moderate"),
    (2, "Low"),
    (1, "None"),
)

RFC_STATUS = (
    (1, "Draft"),
    (2, "Waiting for approval"),
    (3, "Approved"),
    (4, "Started"),
    (5, "Finished"),
    (6, "Rejected"),
    (7, "Paused"),
    (8, "Ready for QA"),
    (9, "Failed"),
)

RFC_TYPE = (
    (4, "Emergency"),
    (3, "High"),
    (2, "Medium"),
    (1, "Low"),
)

SPRINT_STATUS = (
    ("Draft", "Draft"),
    ("Current", "Current"),
    ("Finished", "Finished"),
)

WANT_CHOICE = (
    ("0", "Do not want to do"),
    ("1", "Want to do"),
)
SKILL_CHOICE = (
    ("0", "Can not do"),
    ("1", "Willing to learn"),
    ("2", "Knows a little"),
    ("3", "Knows a lot"),
    ("4", "Proficient"),
)

WEBSITE_SOURCE = (
    ("Twitter", "Twitter"),
    ("Facebook", "Facebook"),
    ("Github", "Github"),
    ("Gitlab", "Gitlab"),
    ("Website", "Website"),
    ("LinkedIn", "LinkedIn"),
    ("Staff Page", "Staff page"),
    ("Other", "Other"),
)


# List of tables - in alphabetical order
class Bug(models.Model):
    bug_id = models.BigAutoField(primary_key=True)
    bug_client = models.ForeignKey(
        "BugClient",
        on_delete=models.CASCADE,
    )
    # Just stores the code of the bug
    bug_code = models.CharField(max_length=255)
    bug_description = models.TextField()
    bug_status = models.CharField(max_length=50)  # Updated manually?
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_description)


class BugClient(models.Model):
    bug_client_id = models.BigAutoField(primary_key=True)
    bug_client_name = models.CharField(max_length=50)
    list_of_bug_client = models.ForeignKey(
        "ListOfBugClient",
        on_delete=models.CASCADE,
    )
    bug_client_url = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_client_name)


class ChangeTask(models.Model):
    change_task_id = models.BigAutoField(primary_key=True)
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
    )
    change_task_title = models.CharField(
        max_length=255,
    )
    change_task_description = models.TextField(
        blank=True,
        null=True,
        default="",
    )
    change_task_start_date = models.DateTimeField()
    change_task_end_date = models.DateTimeField()
    change_task_seconds = models.BigIntegerField(
        default=0,
    )
    change_task_assigned_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="change_assigned_user",
    )
    change_task_qa_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="change_qa_user",
    )
    change_task_required_by = models.CharField(
        max_length=255,
        default="Stakeholder(s)",
    )
    change_task_status = models.IntegerField(
        choices=RFC_STATUS,  # Similar FLOW to RFC
    )
    is_downtime = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    creation_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str("$" + str(self.change_task_title))


class ChangeTaskBlock(models.Model):
    change_task_block_id = models.BigAutoField(primary_key=True)
    change_task_blocks = models.ForeignKey(
        ChangeTask,
        on_delete=models.CASCADE,
        related_name="change_task_blocks",
    )
    blocked_change_task = models.ForeignKey(
        ChangeTask,
        on_delete=models.CASCADE,
        related_name="blocked_change_task",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
    )
    creation_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_creation_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str("$" + str(self.change_task_title))


class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    customer_title = models.ForeignKey(
        "ListOfTitle",
        on_delete=models.CASCADE,
    )
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=200)
    customer_profile_picture = models.ForeignKey(
        "document",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(
            str(self.customer_id)
            + " - "
            + self.customer_first_name
            + " "
            + self.customer_last_name
        )


class Document(models.Model):
    document_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    document_description = models.CharField(max_length=255)
    document_url_location = models.TextField(
        # Contains URLS
        null=True,
        blank=True,
        default="",
    )
    document = models.FileField(
        blank=True,
        null=True,
        storage=FileStorage(),
    )
    document_upload_successfully = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.document_description)


class DocumentPermission(models.Model):
    document_permisssion_id = models.BigAutoField(primary_key=True)
    document_key = models.ForeignKey(
        "document",
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        "project",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        "task",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    organisation = models.ForeignKey(
        "organisation",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        "customer",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    requirement = models.ForeignKey(
        "requirement",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    request_for_change = models.ForeignKey(
        "RequestForChange",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    kanban_card = models.ForeignKey(
        "KanbanCard",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    new_object = models.UUIDField(
        blank=True,
        null=True,
    )
    folder = models.ForeignKey(
        "folder",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_profile_picture = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class Folder(models.Model):
    folder_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(
        "project", on_delete=models.CASCADE, blank=True, null=True
    )
    task = models.ForeignKey("task", on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        "requirement",
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
    request_for_change = models.ForeignKey(
        "RequestForChange",
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
    folder_description = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.folder_description)


class Group(models.Model):
    group_id = models.BigAutoField(primary_key=True)
    group_name = models.CharField(
        max_length=50,
    )
    parent_group = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def natural_key(self):
        return (self.group_id, self.group_name)

    def __str__(self):
        return str(self.group_name)


class GroupPermission(models.Model):
    group_permission_id = models.BigAutoField(primary_key=True)
    permission_set = models.ForeignKey(
        "PermissionSet",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey("group", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.permission_set)


class KanbanBoard(models.Model):
    kanban_board_id = models.BigAutoField(primary_key=True)
    kanban_board_name = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        "requirement",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    kanban_board_status = models.CharField(
        max_length=10,
        choices=KANBAN_BOARD_STATUS_CHOICE,
        default="Open",
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
        return str(self.kanban_board_name)


class KanbanCard(models.Model):
    kanban_card_id = models.BigAutoField(primary_key=True)
    kanban_card_text = models.CharField(max_length=255)
    kanban_card_description = models.TextField(
        blank=True,
        default="",
    )
    kanban_card_sort_number = models.IntegerField()
    kanban_level = models.ForeignKey(
        "KanbanLevel",
        on_delete=models.CASCADE,
    )
    kanban_column = models.ForeignKey(
        "KanbanColumn",
        on_delete=models.CASCADE,
    )
    kanban_board = models.ForeignKey(
        "KanbanBoard",
        on_delete=models.CASCADE,
    )
    kanban_card_priority = models.IntegerField(
        choices=KANBAN_CARD_PRIORITY,
        default=2,
    )
    project = models.ForeignKey(
        "project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_archived = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.kanban_card_text)


class KanbanColumn(models.Model):
    kanban_column_id = models.BigAutoField(primary_key=True)
    kanban_column_name = models.CharField(max_length=255)
    kanban_column_property = models.CharField(
        max_length=10,
        choices=OBJECT_HIGHER_ORDER_STATUS,
        default="Normal",
    )
    kanban_column_sort_number = models.IntegerField()
    kanban_board = models.ForeignKey(
        "KanbanBoard",
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

    def __str__(self):
        return str(self.kanban_column_name)


class KanbanLevel(models.Model):
    kanban_level_id = models.BigAutoField(primary_key=True)
    kanban_level_name = models.CharField(max_length=255)
    kanban_level_sort_number = models.IntegerField()
    kanban_board = models.ForeignKey(
        "KanbanBoard",
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

    def __str__(self):
        return str(self.kanban_level_name)


class ListOfBugClient(models.Model):
    list_of_bug_client_id = models.BigAutoField(primary_key=True)
    bug_client_name = models.CharField(max_length=50)
    bug_client_api_url = models.CharField(max_length=255)

    # The different API commands
    api_open_bugs = models.CharField(max_length=255)  # Find all open bugs
    api_search_bugs = models.CharField(max_length=255)  # Search command

    # Get that particular bug information - direct link to bug
    api_bug = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_client_name)


class ListOfProjectStatus(models.Model):
    project_status_id = models.BigAutoField(primary_key=True)
    project_status = models.CharField(
        max_length=100,
    )
    project_higher_order_status = models.CharField(
        max_length=10,
        choices=OBJECT_HIGHER_ORDER_STATUS,
        default="Backlog",
    )
    project_status_sort_order = models.PositiveIntegerField(
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.project_status)

class ListOfRequirementItemStatus(models.Model):
    requirement_item_status_id = models.BigAutoField(primary_key=True)
    requirement_item_status = models.CharField(
        max_length=100,
    )
    requirement_item_higher_order_status = models.CharField(
        max_length=10,
        choices=OBJECT_HIGHER_ORDER_STATUS,
        default="Normal",
    )
    requirement_item_status_sort_order = models.PositiveIntegerField(
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_status)


class ListOfRequirementItemType(models.Model):
    requirement_item_type_id = models.BigAutoField(primary_key=True)
    requirement_item_type = models.CharField(
        max_length=100,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_type)


class ListOfRequirementStatus(models.Model):
    requirement_status_id = models.BigAutoField(primary_key=True)
    requirement_status = models.CharField(
        max_length=50,
    )
    requirement_higher_order_status = models.CharField(
        max_length=10,
        choices=OBJECT_HIGHER_ORDER_STATUS,
        default="Normal",
    )
    requirement_status_sort_order = models.PositiveIntegerField(
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_status)


class ListOfRequirementType(models.Model):
    requirement_type_id = models.BigAutoField(primary_key=True)
    requirement_type = models.CharField(
        max_length=100,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_type)


class ListOfRFCStatus(models.Model):
    rfc_status_id = models.BigAutoField(primary_key=True)
    rfc_status = models.CharField(
        max_length=100,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.rfc_status)


class ListOfTaskStatus(models.Model):
    task_status_id = models.BigAutoField(primary_key=True)
    task_status = models.CharField(
        max_length=100,
    )
    task_higher_order_status = models.CharField(
        max_length=10,
        choices=OBJECT_HIGHER_ORDER_STATUS,
        default="Backlog",
    )
    task_status_sort_order = models.PositiveIntegerField(
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.task_status)


class ListOfTitle(models.Model):
    title_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.title)


class Notification(models.Model):
    """
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
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_change_user",
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class ObjectAssignment(models.Model):
    """
    Object permissions is the centralised permissions for all objects
    - Requirement
    - Project
    - Task
    - Kanban board
    - Request for change
    - Card

    These permission are only "ACCESS" permissions.
    The user/group's over riding permissions determine if
    the user can add, edit etc.
    """

    object_assignment_id = models.BigAutoField(primary_key=True)
    assigned_user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_assigned_user",
        null=True,
        blank=True,
    )
    group_id = models.ForeignKey(
        "group",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        "requirement",
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
        "project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "task",
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
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    change_task = models.ForeignKey(
        "ChangeTask",
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
        default='',
    )
    meta_object_status = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    link_relationship = models.CharField(
        max_length=10,
        choices=LINK_RELATIONSHIP,
        blank=True,
        default='',
    )
    parent_link = models.CharField(
        max_length=20,
        blank=True,
        default='',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class ObjectNote(models.Model):
    object_note_id = models.BigAutoField(primary_key=True)
    object_note = models.TextField(
        blank=False,
        default="",
    )
    kanban_card = models.ForeignKey(
        "KanbanCard",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        "requirement",
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
        "project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "task",
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
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class Organisation(models.Model):
    organisation_id = models.BigAutoField(primary_key=True)
    organisation_name = models.CharField(max_length=255)
    organisation_website = models.CharField(max_length=50)
    organisation_email = models.CharField(max_length=100)
    organisation_profile_picture = models.ForeignKey(
        "document",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.organisation_name)


class PermissionSet(models.Model):
    permission_set_id = models.BigAutoField(primary_key=True)
    permission_set_name = models.CharField(
        max_length=255,
    )
    # ADMINISTRATION PERMISSIONS
    administration_assign_user_to_group = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_group = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_permission_set = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_user = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    bug_client = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    customer = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    kanban_board = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    kanban_card = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    organisation = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    project = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    request_for_change = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    requirement = models.IntegerField(choices=PERMISSION_LEVEL, default=0)
    task = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    tag = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    """
    ADDITIVE permission
    ~~~~~~~~~~~~~~~~~~~~
    Designed to add on extra abilities to those user who have "READ ONLY" for certain modules.
    If a user has the ability to "EDIT" for any of these modules, then this section does not
    need to be populated with data.
    """
    document = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    kanban_comment = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    project_history = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    task_history = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.permission_set_name)


class Project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField("project_description")
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # Only fill this field out if there are no organisation
    customer = models.ForeignKey(
        "customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project_start_date = models.DateTimeField()
    project_end_date = models.DateTimeField()
    project_status = models.ForeignKey(
        "ListOfProjectStatus",
        on_delete=models.CASCADE,
    )
    project_story_point_min = models.IntegerField(default=1)
    project_story_point_max = models.IntegerField(default=4)
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
        return str(self.project_name)


class PublicLink(models.Model):
    public_link_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    public_link_is_active = models.BooleanField(
        default=True,
    )
    requirement = models.ForeignKey(
        "requirement",
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
        "project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "task",
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


class RequestForChange(models.Model):
    """
    Due to the long and complicated name,
    request for change will be shortened to rfc for ALL fields.
    """

    rfc_id = models.BigAutoField(primary_key=True)
    rfc_title = models.CharField(
        max_length=255,
    )
    rfc_summary = models.TextField("rfc_summary")
    rfc_type = models.IntegerField(
        choices=RFC_TYPE,
    )
    rfc_implementation_start_date = models.DateTimeField()
    rfc_implementation_end_date = models.DateTimeField()
    rfc_implementation_release_date = models.DateTimeField()
    rfc_version_number = models.CharField(
        max_length=25,
        blank=True,
        default='',
    )
    rfc_status = models.ForeignKey(
        "ListOfRfcStatus",
        on_delete=models.CASCADE,
    )
    rfc_lead = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name="RfcLead",
    )
    rfc_priority = models.IntegerField(
        choices=RFC_PRIORITY,
        default=1,
    )
    rfc_risk = models.IntegerField(
        choices=RFC_RISK,
        default=1,
    )
    rfc_impact = models.IntegerField(
        choices=RFC_IMPACT,
        default=1,
    )
    rfc_risk_and_impact_analysis = models.TextField(
        "rfc_risk_and_impact_analysis",
    )
    rfc_implementation_plan = models.TextField(
        "rfc_implementation_plan",
    )
    rfc_backout_plan = models.TextField(
        "rfc_backout_plan",
    )
    rfc_test_plan = models.TextField(
        "rfc_test_plan",
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
        return str(self.rfc_title)


class RequestForChangeGroupApproval(models.Model):
    rfc_group_approval_id = models.BigAutoField(primary_key=True)
    rfc = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "group",
        on_delete=models.CASCADE,
    )
    approval = models.IntegerField(
        choices=RFC_APPROVAL,
        default=1,  # Waiting
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.approval)


class Requirement(models.Model):
    requirement_id = models.BigAutoField(primary_key=True)
    requirement_title = models.CharField(
        max_length=255,
    )
    requirement_scope = models.TextField(
        blank=True,
        default="",
    )
    requirement_type = models.ForeignKey(
        "ListOfRequirementType",
        on_delete=models.CASCADE,
    )
    requirement_status = models.ForeignKey(
        "ListOfRequirementStatus",
        on_delete=models.CASCADE,
    )
    requirement_story_point_min = models.IntegerField(default=1)
    requirement_story_point_max = models.IntegerField(default=4)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
        return str(self.requirement_title)


class RequirementItem(models.Model):
    requirement_item_id = models.BigAutoField(primary_key=True)
    requirement = models.ForeignKey(
        "requirement",
        on_delete=models.CASCADE,
    )
    requirement_item_title = models.CharField(max_length=255)
    requirement_item_scope = models.TextField(
        blank=True,
        default="",
    )
    requirement_item_status = models.ForeignKey(
        "ListOfRequirementItemStatus",
        on_delete=models.CASCADE,
    )
    requirement_item_type = models.ForeignKey(
        "ListOfRequirementItemType",
        on_delete=models.CASCADE,
    )
    ri_story_point_min = models.IntegerField(default=4)
    ri_story_point_max = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_title)


class Sprint(models.Model):
    sprint_id = models.BigAutoField(primary_key=True)
    sprint_name = models.CharField(
        max_length=100,
        null=False,
        default="empty sprint",
    )
    requirement = models.ForeignKey(
        "Requirement",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    total_story_points = models.IntegerField(
        default=0,
    )
    completed_story_points = models.IntegerField(
        default=0,
    )
    sprint_status = models.CharField(
        max_length=10,
        choices=SPRINT_STATUS,
        blank=True,
        default="Draft",
    )
    sprint_start_date = models.DateTimeField()
    sprint_end_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.sprint_name)


class SprintAuditTable(models.Model):
    sprint_audit_table_id = models.BigAutoField(primary_key=True)
    sprint_id = models.ForeignKey(
        "Sprint",
        on_delete=models.CASCADE,
    )
    story_point_cost = models.IntegerField(
        default=0,
    )
    higher_order_status = models.CharField(
        max_length=10,
        choices=OBJECT_HIGHER_ORDER_STATUS,
        default="Normal",
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class SprintObjectAssignment(models.Model):
    sprint_object_assignment_id = models.BigAutoField(primary_key=True)
    sprint_id = models.ForeignKey(
        "Sprint",
        on_delete=models.CASCADE,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class Tag(models.Model):
    tag_id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(
        max_length=50,
    )
    tag_colour = models.CharField(
        max_length=7,
        default="#651794",
    )
    tag_text_colour = models.CharField(
        max_length=7,
        default="#ffffff",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.tag_name)


class TagAssignment(models.Model):
    class ObjectEnum(models.TextChoices):
        REQUIREMENT = "requirement", _("Requirement")
        REQUIREMENT_ITEM = "RequirementItem", _("Requirement Item")
        PROJECT = "project", _("Project")
        TASK = "task", _("Task")
        KANBAN = "KanbanBoard", _("Kanban Board")
        CARD = "KanbanCard", _("Kanban Card")
        REQUEST_FOR_CHANGE = "RequestForChange", _("Request for Change")
        CUSTOMER = "customer", _("Customer")
        ORGANISATION = "organisation", _("Organisation")

    tag_assignment_id = models.BigAutoField(primary_key=True)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    object_enum = models.CharField(
        max_length=40,
        choices=ObjectEnum.choices,
        default=ObjectEnum.REQUIREMENT,
    )
    object_id = models.IntegerField(
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    task_short_description = models.CharField(max_length=255)
    task_long_description = models.TextField()
    organisation = models.ForeignKey(
        "organisation",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task_start_date = models.DateTimeField()
    task_end_date = models.DateTimeField()
    task_assigned_to = models.ForeignKey(
        USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    task_status = models.ForeignKey(
        "ListOfTaskStatus",
        on_delete=models.CASCADE,
    )
    task_story_point_min = models.IntegerField(default=4)
    task_story_point_max = models.IntegerField(default=10)
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
        return str(self.task_short_description)


class UserGroup(models.Model):
    user_group_id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "group",
        on_delete=models.CASCADE,
    )
    permission_set = models.ForeignKey(
        "PermissionSet",
        on_delete=models.CASCADE,
    )
    report_to = models.ForeignKey(
        USER_MODEL,
        related_name="report_to",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    group_leader = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class UserProfilePicture(models.Model):
    username = models.OneToOneField(
        USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    document = models.ForeignKey(
        Document,
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

    def __str__(self):
        # Return the document key
        return self.document.document_key


class UserSetting(models.Model):
    class SettingType(models.TextChoices):
        DASHBOARD = "DASHBOARD", _("Dashboard")
        EDIT_KANBAN_BOARD = "EDIT_KANBAN_BOARD", _("Edit Kanban Board")
        KANBAN_BOARD = "KANBAN_BOARD", _("Kanban Board")
        SEARCH = "SEARCH", _("Search")
        THEME = "THEME", _("NearBeach Theme")

    user_setting_id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
    )
    setting_type = models.CharField(
        max_length=30,
        choices=SettingType.choices,
        default=SettingType.THEME
    )
    setting_data = models.JSONField()
