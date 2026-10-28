from functools import wraps

from django.db.models import Max
from rest_framework.exceptions import PermissionDenied, NotFound

from NearBeach.models.user import UserGroup
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.utils.api.check_object_exists import check_object_exists
from NearBeach.utils.api.get_destination import get_object_from_url
from NearBeach.utils.api.get_parent_object import get_parent_object


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
            destination, location_id = get_object_from_url(path)

            # Get parent destination if required
            destination, location_id = get_parent_object(destination, location_id)
            location_id = None if location_id is None else str(location_id)  # a parent's id comes back as an int

            # Check the destination and location id
            if destination is None or location_id is None:
                raise PermissionDenied

            # Check to make sure the location id is a number
            if not location_id.isnumeric():
                raise NotFound

            # Check to see if the object exists
            object_exists = check_object_exists(destination, location_id)
            if not object_exists:
                raise NotFound

            # All user group results
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=username,
            )

            # Exclude organisation
            if destination != "organisation":
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
            user_level = user_group_results.aggregate(
                Max(f"permission_set__{destination}")
            )[f"permission_set__{destination}__max"]
            if user_level is None:
                raise PermissionDenied

            if user_level < min_permission_level:
                # Below the level needed - the additive permission can still let a read-only user in, but it has to
                # come from the same permission set that lets them read the object
                has_additive_permission = additive_permission is not None and user_group_results.filter(
                    permission_set__is_deleted=False,
                    **{
                        f"permission_set__{destination}__gte": 1,
                        f"permission_set__{additive_permission}__gte": 1,
                    },
                ).exists()
                if not has_additive_permission:
                    raise PermissionDenied

            return func(request, *args, **kwargs, user_level=user_level)
        return inner
    return decorator
