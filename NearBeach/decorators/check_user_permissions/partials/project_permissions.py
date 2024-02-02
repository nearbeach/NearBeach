from NearBeach.models import ObjectAssignment, Project, UserGroup
from django.db.models import Max, Q


def project_permissions(request, kwargs):
    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    if len(kwargs) > 0:
        # Get the requirement groups
        user_group_results = UserGroup.objects.filter(
            Q(
                is_deleted=False,
                group_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    group_id__isnull=False,
                    project_id=kwargs["project_id"],
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
        Max("permission_set__project")
    )["permission_set__project__max"]

    return True, user_level
