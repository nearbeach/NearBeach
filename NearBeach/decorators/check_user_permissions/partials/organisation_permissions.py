from django.db.models import Max, Q
from NearBeach.models import UserGroup


def organisation_permissions(request, kwargs):
    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # Get the max permission value from user_group_results
    user_level = user_group_results.aggregate(
        Max("permission_set__organisation")
    )["permission_set__organisation__max"]

    return True, user_level
