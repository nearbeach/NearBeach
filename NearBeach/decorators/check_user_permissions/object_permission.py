from functools import wraps

from rest_framework.exceptions import PermissionDenied, NotFound

from NearBeach.utils.api.check_object_exists import check_object_exists
from NearBeach.utils.api.get_destination import get_object_from_url
from NearBeach.utils.api.get_parent_object import get_parent_object
from NearBeach.utils.permission_cache import get_object_permission


def object_permission(min_permission_level, additive_permission=None):
    """
    Decorator for checking the user's permission on an object where location id is known

    Method
    1. Obtain the destination and location id from the URL
    2. Check destination to see if it is a child object
    3. If child object - get the parent's destination and location id
    4. Check user's permissions against the object

    additive_permission is the name of an additive permission-set field (e.g. "project_note" or "document"). Those
    exist for users who only have READ ONLY on an object: a read-only user whose permission set also has that
    field switched on is let in even though their level is below min_permission_level. They still need level 1 -
    the extra permission adds an ability, it does not replace being able to see the object.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # Get the path
            path = getattr(request, "path", None)
            path = request.request.path if path is None else path

            # Get the username
            username = getattr(request, "user", None)
            username = request.request.user if username is None else username

            # Get the destination and location id
            url_destination, url_location_id = get_object_from_url(path)
            if url_destination is None or url_location_id is None:
                raise PermissionDenied

            # Check to make sure the location id is a number
            if not url_location_id.isnumeric():
                raise NotFound

            # Get parent destination if required
            destination, location_id = get_parent_object(url_destination, int(url_location_id))
            if destination is None or location_id is None:
                raise PermissionDenied

            # Check to see if the object exists
            object_exists = check_object_exists(destination, location_id)
            if not object_exists:
                raise NotFound

            # Level (and additive permission) for this user on the object - cached, see utils/permission_cache.py
            user_level, has_additive_permission = get_object_permission(
                username,
                destination,
                location_id,
                additive_permission,
            )
            if user_level is None:
                raise PermissionDenied

            if user_level < min_permission_level:
                # Below the level needed - the additive permission can still let a read-only user in
                if not has_additive_permission:
                    raise PermissionDenied

            return func(request, *args, **kwargs, user_level=user_level)
        return inner
    return decorator
