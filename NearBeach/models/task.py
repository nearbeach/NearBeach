"""Module providing Task tables for NearBeach."""

from django.db import models
from django.conf import settings

from NearBeach.models.common_info import CommonInfo
from NearBeach.models.organisation import Organisation
from NearBeach.utils.enums.object_enums import ObjectPriority
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class ListOfTaskStatus(CommonInfo):
    """Class containing fields for List of Task Status."""
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
        """Meta definition for ListOfTaskStatus."""
        verbose_name_plural = "List Of Task Status"
        ordering = ["sort_order"]


class Task(CommonInfo):
    """Class containing fields for Task."""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        ListOfTaskStatus,
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
        verbose_name_plural = "Tasks"
        ordering = ["-id"]
