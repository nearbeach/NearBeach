"""Module proves Object Note tables for NearBeach"""

from django.db import models

from NearBeach.models.common_info import CommonInfo


class ObjectNote(CommonInfo):
    """Class contains fields for Object Note table"""

    id = models.BigAutoField(primary_key=True)
    note = models.TextField(
        blank=False,
        default="",
    )
    kanban_card = models.ForeignKey(
        "KanbanCard",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        "Requirement",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for ObjectNote"""

        verbose_name_plural = "Object Notes"
