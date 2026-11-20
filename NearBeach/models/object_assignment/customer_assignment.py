from django.db import models
from django.db.models import Q

from NearBeach.models.abstraction.common_abstractions import CommonInfo


class CustomerAssignment(CommonInfo):
    """A customer associated with one project, task, or requirement."""

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", null=True, blank=True, on_delete=models.CASCADE)
    task = models.ForeignKey("Task", null=True, blank=True, on_delete=models.CASCADE)
    requirement = models.ForeignKey(
        "Requirement", null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(project__isnull=False, task__isnull=True, requirement__isnull=True)
                    | Q(project__isnull=True, task__isnull=False, requirement__isnull=True)
                    | Q(project__isnull=True, task__isnull=True, requirement__isnull=False)
                ),
                name="customer_assignment_one_object",
            ),
        ]
