from django.db.models import Q

from NearBeach.models import (
    ListOfRequirementItemStatus,
    ListOfRequirementStatus,
    ObjectAssignment,
    Project,
    Requirement,
    RequirementItem,
    Task,
)

# Internal function
def lookup_project(user_group_results, destination, location_id):
    return Project.objects.filter(
        is_deleted=False,
        project_id__in=ObjectAssignment.objects.filter(
            is_deleted=False,
            project_id__isnull=False,
            group_id__in=user_group_results,
        ).values("project_id"),
    ).exclude(
        Q(
            project_status="Closed",
        )
        | Q(
            project_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                project_id__isnull=False,
                **{destination: location_id},
            ).values("project_id")
        )
    )


def lookup_task(user_group_results, destination, location_id):
    return Task.objects.filter(
        is_deleted=False,
        task_id__in=ObjectAssignment.objects.filter(
            is_deleted=False,
            task_id__isnull=False,
            group_id__in=user_group_results,
        ).values("task_id"),
    ).exclude(
        Q(
            task_status="Closed",
        )
        | Q(
            task_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                task_id__isnull=False,
                **{destination: location_id},
            ).values("task_id")
        )
    )


def lookup_requirement(user_group_results, *args, **kwargs):
    return Requirement.objects.filter(
        is_deleted=False,
        requirement_status_id__in=ListOfRequirementStatus.objects.filter(
            is_deleted=False,
            requirement_status_is_closed=False,
        ).values("requirement_status_id"),
        requirement_id__in=ObjectAssignment.objects.filter(
            is_deleted=False,
            requirement_id__isnull=False,
            group_id__in=user_group_results,
        ).values('requirement_id'),
    )


def lookup_requirement_item(user_group_results, *args, **kwargs):
    return RequirementItem.objects.filter(
        is_deleted=False,
        requirement_item_status_id__in=ListOfRequirementItemStatus.objects.filter(
            is_deleted=False,
            status_is_closed=False,
        ).values("requirement_item_status_id"),
        requirement_id__in=Requirement.objects.filter(
            is_deleted=False,
            requirement_status_id__in=ListOfRequirementStatus.objects.filter(
                is_deleted=False,
                requirement_status_is_closed=False,
            ).values("requirement_status_id"),
            requirement_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                requirement_id__isnull=False,
                group_id__in=user_group_results,
            ).values('requirement_id'),
        ).values("requirement_id"),
    )
