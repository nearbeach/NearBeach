"""Module provides Tag tables for NearBeach"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from NearBeach.models.abstraction.common_abstractions import CommonInfo


class Tag(CommonInfo):
    """Class contains fields for Tag table"""

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

    def __str__(self):
        return str(self.tag_name)

    class Meta:
        """Meta definition for Tag table."""

        verbose_name_plural = "Tags"


class TagAssignment(CommonInfo):
    """Class contains fields for Tag Assignment table"""

    class ObjectEnum(models.TextChoices):
        """Class contains enum choices for object enum."""

        REQUIREMENT = "requirement", _("Requirement")
        REQUIREMENT_ITEM = "requirement_item", _("Requirement Item")
        PROJECT = "project", _("Project")
        TASK = "task", _("Task")
        KANBAN = "kanban_board", _("Kanban Board")
        CARD = "kanban_card", _("Kanban Card")
        REQUEST_FOR_CHANGE = "request_for_change", _("Request for Change")
        CUSTOMER = "customer", _("Customer")
        ORGANISATION = "organisation", _("Organisation")

    id = models.BigAutoField(primary_key=True)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    object_enum = models.CharField(
        max_length=40,
        choices=ObjectEnum,
        default=ObjectEnum.REQUIREMENT,
    )
    object_id = models.IntegerField(
        default=0,
    )

    class Meta:
        """Meta definition for TagAssignment table."""

        verbose_name_plural = "Tag Assignments"
