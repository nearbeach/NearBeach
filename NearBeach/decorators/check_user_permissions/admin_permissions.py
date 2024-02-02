from django.core.exceptions import PermissionDenied
from django.db.models import Max
from functools import wraps

from NearBeach.models import PermissionSet, UserGroup


def check_user_admin_permissions(min_permission_level, permission_lookup=""):
    """
    Function is only used in the administration views. It is designed to make sure that
    the user either;
    1. Is an admin or
    2. Has some administration permissions attributes associated with them.

    Permission Lookup is the field we are looking up in the PermissionSet table
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - full permission
            if request.user.is_superuser:
                return func(request, *args, **kwargs, user_level=4)

            # At this point - if permission lookup is an empty string - escape
            if permission_lookup == "":
                raise PermissionDenied

            # Look at the user's permission set table
            permission_set_results = PermissionSet.objects.filter(
                is_deleted=False,
                permission_set_id__in=UserGroup.objects.filter(
                    is_deleted=False, username=request.user
                ).values("permission_set_id"),
            )

            user_level = permission_set_results.aggregate(Max(permission_lookup))[
                f"{permission_lookup}__max"
            ]

            if user_level >= min_permission_level:
                # Everything is fine - move on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator
