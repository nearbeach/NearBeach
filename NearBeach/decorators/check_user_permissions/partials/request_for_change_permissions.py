from NearBeach.models import Group, ObjectAssignment, UserGroup
from django.db.models import Max, Q


# Internal Function
def request_for_change_permissions(request, kwargs):
    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # If we are passing the object_lookup through, we will use a different function
    if len(kwargs) > 0:
        # Determine if there are any cross over with user groups and object_lookup groups
        group_results = Group.objects.filter(
            Q(
                is_deleted=False,
                # The object_lookup groups
                group_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    # **{object_lookup: kwargs[object_lookup]},
                    request_for_change_id=kwargs["rfc_id"],
                ).values("group_id"),
            )
            & Q(group_id__in=user_group_results.values("group_id"))
        )

        # Check to make sure the user groups intersect
        if len(group_results) == 0:
            return False, 0, False

    # Get the max permission value from user_group_results
    user_level = user_group_results.aggregate(
        Max("permission_set__request_for_change")
    )["permission_set__request_for_change__max"]

    return True, user_level, False
