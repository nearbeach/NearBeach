"""Module provides User tables for NearBeach"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.document.document import Document
from NearBeach.models.kanban_board.kanban_card import KanbanCardForeignKey
from NearBeach.models.permission.group import Group
from NearBeach.models.permission.permission_set import PermissionSet
from NearBeach.models.project import ProjectForeignKey
from NearBeach.models.task import TaskForeignKey


class UserGroup(CommonInfo):
    """Class contains fields for User Group table"""

    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )
    permission_set = models.ForeignKey(
        PermissionSet,
        on_delete=models.CASCADE,
    )
    report_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="report_to",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    group_leader = models.BooleanField(
        default=False,
    )

    class Meta:
        """Meta definition for UserGroup."""

        verbose_name_plural = "User Groups"


class UserJob(
    CommonInfo,
    KanbanCardForeignKey,
    ProjectForeignKey,
    TaskForeignKey,

):
    """Class contains fields for User Job table"""

    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    sort_number = models.IntegerField()

    class Meta:
        """Meta definition for UserJob."""

        verbose_name_plural = "User Jobs"


class UserProfilePicture(CommonInfo):
    """Class contains fields for User Profile Picture table"""

    username = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        # Return the document key
        return self.document.key

    class Meta:
        """Meta definition for UserProfilePicture."""

        verbose_name_plural = "User Profile Pictures"


class UserSetting(CommonInfo):
    """Class contains fields for User Setting table"""

    class SettingType(models.TextChoices):
        """Class containing the setting types for User Settings."""

        DASHBOARD = "DASHBOARD", _("Dashboard")
        EDIT_KANBAN_BOARD = "EDIT_KANBAN_BOARD", _("Edit Kanban Board")
        KANBAN_BOARD = "KANBAN_BOARD", _("Kanban Board")
        SEARCH = "SEARCH", _("Search")
        THEME = "THEME", _("NearBeach Theme")

    id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    setting_type = models.CharField(
        max_length=30,
        choices=SettingType,
        default=SettingType.THEME,
    )
    setting_data = models.JSONField()

    class Meta:
        """Meta definition for UserSetting."""

        verbose_name_plural = "User Settings"
