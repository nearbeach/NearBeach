from functools import wraps

from django.db.models import Max
from rest_framework.exceptions import PermissionDenied

from NearBeach.models import UserGroup, ObjectAssignment
from NearBeach.utils.api.get_destination import get_destination_from_url, get_object_from_url
from NearBeach.utils.api.get_parent_object import get_parent_object


def object_permission(min_permission_level):
    """
    Decorator for checking the user's permission on an object where location id is known

    Method
    1. Obtain the destination and location id from the URL
    2. Check destination to see if it is a child object
    3. If child object - get the parent's destination and location id
    4. Check user's permissions against the object
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # Get the destination and location id
            destination, location_id = get_object_from_url(request.path)

            # Get parent destination if required
            destination, location_id = get_parent_object(destination, location_id)

            # Check the destination and location id
            if destination is None or location_id is None:
                raise PermissionDenied

            # All user group results
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # Exclude organisation
            if destination is not "organisation":
                # Apply the location_id grouping
                user_group_results = user_group_results.filter(
                    group_id__in=ObjectAssignment.objects.filter(
                        is_deleted=False,
                        group_id__isnull=False,
                        **{destination: location_id},
                    ).values("group_id")
                )

            # Check user group results for any results
            if len(user_group_results) == 0:
                raise PermissionDenied

            # Check the user permissions
            user_group_results = user_group_results.aggregate(
                Max(f"permission_set__{destination}")
            )[f"permission_set__{destination}__max"]

            # Check the user permissions
            if user_group_results < min_permission_level:
                raise PermissionDenied

            return func(request, *args, **kwargs, user_level=user_group_results)
        return inner
    return decorator
