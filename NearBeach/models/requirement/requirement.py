"""Module providing Requirement tables for NearBeach."""

from django.db import models

from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.organisation import Organisation
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class ListOfRequirementStatus(CommonInfo):
    """Class containing fields for ListOfRequirement table."""

    id = models.BigAutoField(primary_key=True)
    status = models.CharField(
        max_length=50,
    )
    higher_order_status = models.CharField(
        max_length=10,
        choices=ObjectHigherOrderStatus,
        default=ObjectHigherOrderStatus.NORMAL,
    )
    sort_order = models.PositiveIntegerField(
        default=0,
    )

    def __str__(self):
        return str(self.status)

    class Meta:
        """Meta definition for ListOfRequirement table."""

        verbose_name_plural = "List Of Requirement Statuses"
        ordering = ["sort_order"]


class ListOfRequirementType(CommonInfo):
    """Class containing fields for ListOfRequirementType table."""

    id = models.BigAutoField(primary_key=True)
    type = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return str(self.type)

    class Meta:
        """Meta definition for ListOfRequirementType table."""

        verbose_name_plural = "List Of Requirement Types"


class Requirement(CommonInfo):
    """Class containing fields for Requirement table."""

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,
        default="",
    )
    type = models.ForeignKey(
        ListOfRequirementType,
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        ListOfRequirementStatus,
        on_delete=models.CASCADE,
    )
    story_point_min = models.IntegerField(default=1)
    story_point_max = models.IntegerField(default=4)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        """Meta definition for Requirement table."""

        verbose_name_plural = "Requirements"
        ordering = ["-id"]


# ABSTRACTION
class RequirementForeignKey(models.Model):
    """Class containing abstraction for Requirement"""

    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta information for Requirement model"""

        abstract = True
