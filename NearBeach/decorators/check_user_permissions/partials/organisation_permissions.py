from django.db.models import Max
from NearBeach.models import UserGroup


def organisation_permissions(request, kwargs):
    # Extra Permissions
    extra_permissions = kwargs.get("extra_permissions", "")

    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # Get the max permission value from user_group_results
    user_level = user_group_results.aggregate(
        Max("permission_set__organisation")
    )["permission_set__organisation__max"]

    # Check all variations of the extra permissions
    extra_level = False
    if extra_permissions == "document":
        extra_level = user_group_results.filter(
            permission_set__document=1,
        ).count() > 0

    if extra_permissions == "organisation_note":
        extra_level = user_group_results.filter(
            permission_set__organisation_note=1,
        ).count() > 0

    return True, user_level, extra_level
