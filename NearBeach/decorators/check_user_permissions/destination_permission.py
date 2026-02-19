from functools import wraps

from django.db.models import Max
from rest_framework.exceptions import PermissionDenied

from NearBeach.models import UserGroup
from NearBeach.utils.api.get_destination import get_destination_from_url
from NearBeach.utils.api.object_to_permission_set_mapping import get_object_permission_set



def destination_permission(min_permission_level):
    """
    Decorator for checking the user's permission when no location_id is supplied

    Method
    1. Obtain the destination from the URL
    2. Check destination to see if it is a child object
    3. If child object - get parent and use that as destination
    4. Check user's permissions against said destination
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # Get the destination
            destination = get_destination_from_url(request.request.path)
            if destination is None:
                raise PermissionDenied

            # Get parent destination
            destination = get_object_permission_set(destination)
            if destination is None:
                raise PermissionDenied

            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.request.user,
            ).aggregate(
                Max(f"permission_set__{destination}")
            )[f"permission_set__{destination}__max"]

            # Check the user permissions
            if user_group_results < min_permission_level:
                raise PermissionDenied

            return func(request, *args, **kwargs, user_level=user_group_results)
        return inner
    return decorator
