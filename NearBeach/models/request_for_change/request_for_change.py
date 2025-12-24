"""Module providing Request for change tables for NearBeach."""

from django.db import models
from django.conf import settings

from NearBeach.models.field.common_info import CommonInfo
from NearBeach.utils.enums.request_for_change_enums import (
    RequestForChangeApproval,
    RequestForChangeStatus,
    RequestForChangeType,
    RequestForChangePriority,
    RequestForChangeRisk,
    RequestForChangeImpact,
)


class RequestForChange(CommonInfo):
    """Class containing fields for Request for change tables."""

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    type = models.IntegerField(
        choices=RequestForChangeType,
    )
    implementation_start_date = models.DateTimeField()
    implementation_end_date = models.DateTimeField()
    implementation_release_date = models.DateTimeField()
    version_number = models.CharField(
        max_length=25,
        blank=True,
        default="",
    )
    status = models.IntegerField(
        choices=RequestForChangeStatus,
    )
    lead = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="RfcLead",
    )
    priority = models.IntegerField(
        choices=RequestForChangePriority,
        default=1,
    )
    risk = models.IntegerField(
        choices=RequestForChangeRisk,
        default=1,
    )
    impact = models.IntegerField(
        choices=RequestForChangeImpact,
        default=1,
    )
    risk_and_impact_analysis = models.TextField(
        "risk_and_impact_analysis",
    )
    implementation_plan = models.TextField(
        "implementation_plan",
    )
    backout_plan = models.TextField(
        "backout_plan",
    )
    test_plan = models.TextField(
        "test_plan",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        """Meta definition for RequestForChange."""

        verbose_name_plural = "Request for changes"
        ordering = ["-id"]


class RequestForChangeGroupApproval(CommonInfo):
    """Class containing fields for Request for change group-approval tables."""

    group_approval_id = models.BigAutoField(primary_key=True)
    request_for_change = models.ForeignKey(
        RequestForChange,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
    )
    approval = models.IntegerField(
        choices=RequestForChangeApproval,
        default=RequestForChangeApproval.WAITING,
    )

    def __str__(self):
        return str(self.approval)

    class Meta:
        """Meta definition for RequestForChangeGroupApproval."""

        verbose_name_plural = "Request for change group approvals"
