"""Module provides Sprint object assignment tables for NearBeach"""

from django.db import models

from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.project import Project
from NearBeach.models.task import Task
from NearBeach.models.sprint.sprint import Sprint
from NearBeach.models.abstraction.common_abstractions import CommonInfo


class SprintObjectAssignment(CommonInfo):
    """Class contains fields for Sprint Object Assignment table"""

    id = models.BigAutoField(primary_key=True)
    sprint_id = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
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
        """Meta definition for SprintObjectAssignment table"""

        verbose_name_plural = "Sprint Object Assignments"
