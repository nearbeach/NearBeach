from django.core.exceptions import PermissionDenied
from functools import wraps

from NearBeach.models import Sprint

from NearBeach.decorators.check_user_permissions.object_permissions import FUNCTION_DICT


def check_sprint_permissions_with_destination(min_permission_level):
    """
    Checks the user's permission for the sprint, using the destination as
    the object lookup. We will need to make sure the destination is either
    a project or requirement, otherwise they will get permission denied.
    We will then utilise the correct permission partials to determine if the
    user should have access.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # Obtain destination from args
            # due to weird issue - we check the args length
            if len(args) == 0:
                destination = kwargs["destination"]
            else:
                destination = args[0]

            # If destination is not project or requirement, send permission denied
            if destination not in ["project", "requirement"]:
                raise PermissionDenied

            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Fold the location id into the {destination}_id. This will be used in the partials
            kwargs[F"{destination}_id"] = kwargs["location_id"]

            # User the FUNCTION_DICT to determine which partial permissions we need
            # to reference
            passes, user_level, _ = FUNCTION_DICT[destination](request, kwargs)

            if not passes:
                raise PermissionDenied

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied
        return inner
    return decorator


def check_sprint_permission_with_sprint(min_permission_level):
    """
    Checks the user's permission for the sprint, using the sprint id as
    the object lookup. We will need to make sure the destination is either
    a project or requirement, otherwise they will get permission denied.
    We will then utilise the correct permission partials to determine if the
    user should have access.
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            _request = request.request if hasattr(request, "request") else request

            # If user is admin - grant them all permissions
            if _request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Get the sprint from the id
            if "sprint_id" in kwargs:
                sprint_id = kwargs["sprint_id"]
            elif "location_id" in kwargs:
                sprint_id = kwargs["location_id"]
            elif "pk" in kwargs:
                sprint_id = kwargs["pk"]
            else:
                sprint_id = args[0]

            sprint_results = Sprint.objects.get(sprint_id=sprint_id)

            if sprint_results.project is not None:
                # We can assume this is a project
                kwargs["project_id"] = sprint_results.project_id
                passes, user_level, _ = FUNCTION_DICT["project"](_request, kwargs)
            else:
                kwargs["requirement_id"] = sprint_results.requirement_id
                passes, user_level, _ = FUNCTION_DICT["requirement"](_request, kwargs)

            # Check to see if it passes
            if not passes:
                raise PermissionDenied

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator