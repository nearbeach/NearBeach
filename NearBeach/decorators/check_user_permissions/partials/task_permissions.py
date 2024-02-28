from NearBeach.models import ObjectAssignment, Task, UserGroup
from django.db.models import Max, Q


def task_permissions(request, kwargs):
    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # Check to see if we are passing the task id.
    if len(kwargs) > 0:
        # Get the requirement groups
        user_group_results = user_group_results.filter(
            Q(
                is_deleted=False,
                group_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    group_id__isnull=False,
                    task_id=kwargs["task_id"],
                ).values("group_id"),
            )
            & Q(
                username=request.user,
            )
        )

        # Check to see if there are any groups associated
        if len(user_group_results) == 0:
            # No groups - meaning no permissions
            return False, 0

    # Get the max permission value from user_group_results
    user_level = user_group_results.aggregate(
        Max("permission_set__task")
    )["permission_set__task__max"]

    return True, user_level
