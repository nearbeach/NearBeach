from django.core.exceptions import PermissionDenied
from functools import wraps

from NearBeach.models import Sprint

from NearBeach.decorators.check_user_permissions.object_permissions import FUNCTION_DICT


def check_gantt_chart_permissions_with_destination(min_permission_level):
    """
    Checks the user's permission for the gantt chart, using the destination as
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
                location_id = kwargs["location_id"]
            else:
                destination = args[0]
                location_id = args[1]

            # TEMP FUNCTIONALITY -> At the moment, we are only focusing on sprint functionality
            # In the near future, we'll open this up to OTHER objects
            # For the initial proof of concept, we are only dealing with sprints
            if not destination == "sprint":
                raise PermissionDenied

            destination, location_id = get_sprint_parent_destination(location_id)

            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Fold the location id into the {destination}_id. This will be used in the partials
            kwargs[F"{destination}_id"] = location_id

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


def get_sprint_parent_destination(location_id):
    # Get the sprint information
    sprint_results = Sprint.objects.get(sprint_id=location_id)

    # If there is a project assigned to the sprint. The destination should be project
    if sprint_results.project is not None:
        return "project", sprint_results.project_id
    else:
        return "requirement", sprint_results.requirement_id
