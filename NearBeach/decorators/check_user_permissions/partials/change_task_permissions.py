from NearBeach.models import ChangeTask, Group, ObjectAssignment, UserGroup
from django.db.models import Max, Q


def change_task_permissions(request, kwargs):
    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # If we are passing in any args like change_task_id, we want to do the following
    if len(kwargs) > 0:
        # Get the rfc id
        rfc_id = ChangeTask.objects.get(
            change_task_id=kwargs["change_task_id"]
        ).request_for_change_id

        # Determine if there are any cross over change tasks
        group_results = Group.objects.filter(
            Q(
                is_deleted=False,
                # The object_lookup groups
                group_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    # **{object_lookup: kwargs[object_lookup]},
                    request_for_change_id=rfc_id,
                ).values("group_id"),
            )
            & Q(group_id__in=user_group_results.values("group_id"))
        )

        # Check to make sure the user groups intersect
        if len(group_results) == 0:
            # There are no matching groups - i.e. the user does not have any permission
            return False, 0

    # Get the max permission value from user_group_results
    user_level = user_group_results.aggregate(
        Max("permission_set__request_for_change")
    )["permission_set__request_for_change__max"]

    # Return
    return True, user_level
