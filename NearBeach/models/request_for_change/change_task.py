"""Module providing Change Task tables for NearBeach"""

from django.db import models
from django.conf import settings

from NearBeach.utils.enums.request_for_change_enums import RequestForChangeStatus
from NearBeach.models.common_info import CommonInfo
from NearBeach.models.request_for_change.request_for_change import RequestForChange


class ChangeTask(CommonInfo):
    """Class containing ChangeTask fields"""

    id = models.BigAutoField(primary_key=True)
    request_for_change = models.ForeignKey(
        RequestForChange,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        default="",
        blank=True,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    seconds = models.BigIntegerField(
        default=0,
    )
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="change_assigned_user",
    )
    qa_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="change_qa_user",
    )
    required_by = models.CharField(
        max_length=255,
        default="Stakeholder(s)",
    )
    status = models.IntegerField(
        choices=RequestForChangeStatus,  # Similar FLOW to RFC
    )
    is_downtime = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str("$" + str(self.title))

    class Meta:
        """Meta information for Change Tasks model"""

        verbose_name_plural = "Change Tasks"


class ChangeTaskBlock(CommonInfo):
    """Class containing ChangeTaskBlock fields"""

    block_id = models.BigAutoField(primary_key=True)
    blocks = models.ForeignKey(
        ChangeTask,
        on_delete=models.CASCADE,
        related_name="blocks",
    )
    blocked_change_task = models.ForeignKey(
        ChangeTask,
        on_delete=models.CASCADE,
        related_name="blocked_change_task",
    )

    class Meta:
        """Meta information for ChangeTaskBlock model"""

        verbose_name_plural = "Change Task Blocks"
