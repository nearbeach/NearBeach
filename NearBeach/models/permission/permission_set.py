"""Model providing Permission Set tables for NearBeach."""

from django.db import models

from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.utils.enums.permission_enums import PermissionLevel, PermissionBoolean


class PermissionSet(CommonInfo):
    """Class containing fields for Permission set table"""

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
    )
    # ADMINISTRATION PERMISSIONS
    administration_assign_user_to_group = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    administration_create_group = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    administration_create_permission_set = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    administration_create_user = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    bug_client = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    customer = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    kanban_board = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    kanban_card = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    organisation = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    project = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    request_for_change = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    requirement = models.IntegerField(choices=PermissionLevel, default=0)
    schedule_object = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    task = models.IntegerField(
        choices=PermissionLevel,
        default=0,
    )
    tag = models.IntegerField(
        choices=PermissionLevel,
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
        choices=PermissionBoolean,
        default=0,
    )
    kanban_note = models.IntegerField(
        choices=PermissionBoolean,
        default=0,
    )
    project_note = models.IntegerField(
        choices=PermissionBoolean,
        default=0,
    )
    task_note = models.IntegerField(
        choices=PermissionBoolean,
        default=0,
    )
    requirement_note = models.IntegerField(
        choices=PermissionBoolean,
        default=0,
    )
    requirement_item_note = models.IntegerField(
        choices=PermissionBoolean,
        default=0,
    )
    organisation_note = models.IntegerField(
        choices=PermissionBoolean,
        default=0,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        """Meta definition for permission set."""

        verbose_name_plural = "Permission Sets"
        ordering = ["name"]
