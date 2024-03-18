from django.db.models import Q, F

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
            project_status__project_higher_order_status="Closed",
        )
        | Q(
            project_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                project_id__isnull=False,
                **{destination: location_id},
            ).values("project_id")
        )
    ).annotate(
        id = F('project_id'),
        description = F('project_name'),
        status = F('project_status__project_status'),
    ).values(
        'id',
        'description',
        'status',
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
            task_status__task_higher_order_status="Closed",
        )
        | Q(
            task_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                task_id__isnull=False,
                **{destination: location_id},
            ).values("task_id")
        )
    ).annotate(
        id = F('task_id'),
        description = F('task_short_description'),
        status = F('task_status__task_status'),
    ).values(
        'id',
        'description',
        'status',
    )


def lookup_requirement(user_group_results, *args, **kwargs):
    return Requirement.objects.filter(
        is_deleted=False,
        requirement_id__in=ObjectAssignment.objects.filter(
            is_deleted=False,
            requirement_id__isnull=False,
            group_id__in=user_group_results,
        ).values('requirement_id'),
    ).annotate(
        id = F('requirement_id'),
        description = F('requirement_title'),
        status=F('requirement_status__requirement_status'),
    ).exclude(
        requirement_status__requirement_higher_order_status="Closed",
    ).values(
        'id',
        'description',
        'status',
    )


def lookup_requirement_item(user_group_results, *args, **kwargs):
    return RequirementItem.objects.filter(
        is_deleted=False,
        # requirement_item_status_id__in=ListOfRequirementItemStatus.objects.filter(
        #     is_deleted=False,
        #     status_is_closed=False,
        # ).values("requirement_item_status_id"),
        requirement_id__in=Requirement.objects.filter(
            is_deleted=False,
            # requirement_status_id__in=ListOfRequirementStatus.objects.filter(
            #     is_deleted=False,
            #     requirement_status_is_closed=False,
            # ).values("requirement_status_id"),
            requirement_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                requirement_id__isnull=False,
                group_id__in=user_group_results,
            ).exclude(
                requirement__requirement_status__requirement_higher_order_status="Closed",
            ).values('requirement_id'),
        ).values("requirement_id"),
    ).exclude(
        requirement_item_status__requirement_item_higher_order_status="Closed",
    ).annotate(
        id = F('requirement_item_id'),
        description = F('requirement_item_title'),
        status = F('requirement_item_status__requirement_item_status'),
    ).values(
        'id',
        'description',
        'status',
    )
