"""Module providing Project tables for NearBeach."""

from django.db import models

from NearBeach.models.abstraction.common_abstractions import CommonInfo
from NearBeach.models.organisation import Organisation
from NearBeach.utils.enums.object_enums import ObjectPriority
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class ListOfProjectStatus(CommonInfo):
    """Class containing fields for List of Project Status."""

    id = models.BigAutoField(primary_key=True)
    status = models.CharField(
        max_length=100,
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
        """Meta definition for ListOfProjectStatus."""

        verbose_name_plural = "List of Project Status"
        ordering = ["sort_order"]


class Project(CommonInfo):
    """Class containing fields for Project model."""

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.ForeignKey(
        ListOfProjectStatus,
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
        """Meta definition for Project model."""

        verbose_name_plural = "Projects"
        ordering = ["-id"]


# ABSTRACTION
class ProjectForeignKey(models.Model):
    """Class containing abstraction for Project"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta information for Project model"""

        abstract = True
