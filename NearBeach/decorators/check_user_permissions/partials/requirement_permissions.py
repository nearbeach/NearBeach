from NearBeach.models import ObjectAssignment, UserGroup
from django.db.models import Max


def requirement_permissions(request, kwargs):
    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    if len(kwargs) > 0:
        # Get the requirement groups
        user_group_results = user_group_results.filter(
            is_deleted=False,
            group_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                group_id__isnull=False,
                requirement_id=kwargs["requirement_id"],
            ).values("group_id"),
        )

        # Check to see if there are any groups associated
        if len(user_group_results) == 0:
            # No groups - meaning no permissions
            return False, 0, False

    # Get the max permission value from user_group_results
    user_level = user_group_results.aggregate(
        Max("permission_set__requirement")
    )["permission_set__requirement__max"]

    return True, user_level, False
