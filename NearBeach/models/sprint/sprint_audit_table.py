"""Module provides Sprint audit tables for NearBeach"""

from django.db import models

from NearBeach.models import RequirementItem, Project, Task
from NearBeach.models.sprint.sprint import Sprint
from NearBeach.models.common_info import CommonInfo
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class SprintAuditTable(CommonInfo):
    """Class contains fields for Sprint Audit table"""

    id = models.BigAutoField(primary_key=True)
    sprint_id = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
    )
    story_point_cost = models.IntegerField(
        default=0,
    )
    higher_order_status = models.CharField(
        max_length=10,
        choices=ObjectHigherOrderStatus,
        default=ObjectHigherOrderStatus.NORMAL,
    )
    requirement_item = models.ForeignKey(
        RequirementItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for SprintAuditTable"""

        verbose_name_plural = "Sprint Audit Tables"
