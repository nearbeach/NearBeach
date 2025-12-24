"""Module provides Sprint tables for NearBeach"""
from django.db import models

from NearBeach.models.project import Project
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.common_info import CommonInfo
from NearBeach.utils.enums.status_enums import SprintStatus


class Sprint(CommonInfo):
    """Class contains fields for Sprint table"""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        max_length=100,
        null=False,
        default="empty sprint",
    )
    requirement = models.ForeignKey(
        Requirement,
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
    total_story_points = models.IntegerField(
        default=0,
    )
    completed_story_points = models.IntegerField(
        default=0,
    )
    sprint_status = models.CharField(
        max_length=10,
        choices=SprintStatus,
        blank=True,
        default=SprintStatus.DRAFT,
    )
    sprint_start_date = models.DateTimeField()
    sprint_end_date = models.DateTimeField()

    def __str__(self):
        return str(self.title)

    class Meta:
        """Meta definition for Sprint"""
        verbose_name_plural = "Sprints"
        ordering = ["-id"]
