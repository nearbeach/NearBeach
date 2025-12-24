"""Module providing Requirement Item tables for NearBeach."""

from django.db import models

from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.common_info import CommonInfo
from NearBeach.utils.enums.object_enums import ObjectPriority
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class ListOfRequirementItemStatus(CommonInfo):
    """Class containing fields for the List of requirement item status table."""

    id = models.BigAutoField(primary_key=True)
    status = models.CharField(
        max_length=99,
    )
    higher_order_status = models.CharField(
        max_length=9,
        choices=ObjectHigherOrderStatus,
        default=ObjectHigherOrderStatus.NORMAL,
    )
    sort_order = models.PositiveIntegerField(
        default=-1,
    )

    def __str__(self):
        return str(self.status)

    class Meta:
        """Meta definition for ListOfRequirementItemStatus table."""

        verbose_name_plural = "List Of Requirement Item Statuses"
        ordering = ["sort_order"]


class ListOfRequirementItemType(CommonInfo):
    """Class containing fields for the List of requirement item type table."""

    id = models.BigAutoField(primary_key=True)
    type = models.CharField(
        max_length=99,
    )

    def __str__(self):
        return str(self.type)

    class Meta:
        """Meta definition for ListOfRequirementItemType table."""

        verbose_name_plural = "List Of Requirement Item Types"


class RequirementItem(CommonInfo):
    """Class containing fields for the Requirement item table."""

    id = models.BigAutoField(primary_key=True)
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        default="",
    )
    status = models.ForeignKey(
        ListOfRequirementItemStatus,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        ListOfRequirementItemType,
        on_delete=models.CASCADE,
    )
    story_point = models.IntegerField(default=1)
    priority = models.IntegerField(
        choices=ObjectPriority,
        default=ObjectPriority.NORMAL,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "Requirement Items"
        ordering = ["-id"]
