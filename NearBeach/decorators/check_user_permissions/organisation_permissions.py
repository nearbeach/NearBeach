from django.core.exceptions import PermissionDenied
from django.db.models import Max
from functools import wraps

from NearBeach.models import UserGroup


def check_user_organisation_permissions(min_permission_level):
    """
    Function is only used when checking user permissions against
    organisations. Min Permission Level determines if the user
    will have enough permission to proceed.
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # Need to update request if we are using API
            _request = request.request if hasattr(request, "request") else request

            # if user is admin -grant them all permissions
            if _request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=_request.user,
            )

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max("permission_set__organisation")
            )["permission_set__organisation__max"]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_user_organisation_note_permissions():
    """
    Function is only used when checking user permissions against
    organisations. Min Permission Level determines if the user
    will have enough permission to proceed.
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # if user is admin -grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max("permission_set__organisation")
            )["permission_set__organisation__max"]

            extra_level = user_group_results.aggregate(
                Max("permission_set__organisation_note"),
            )["permission_set__organisation_note__max"]

            if user_level >= 2 or extra_level > 0:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator