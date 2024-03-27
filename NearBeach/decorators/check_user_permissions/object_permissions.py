from django.core.exceptions import PermissionDenied
from django.db.models import Max, Q
from functools import wraps
from .partials.change_task_permissions import change_task_permissions
from .partials.generic_permissions import generic_permissions
from .partials.kanban_board_permissions import kanban_board_permissions
from .partials.kanban_card_permissions import kanban_card_permissions
from .partials.kanban_column_permissions import kanban_column_permissions
from .partials.kanban_level_permissions import kanban_level_permissions
from .partials.request_for_change_permissions import request_for_change_permissions
from .partials.requirement_permissions import requirement_permissions
from .partials.requirement_item_permissions import requirement_item_permissions
from .partials.object_note_permissions import object_note_permissions
from .partials.organisation_permissions import organisation_permissions
from .partials.project_permissions import project_permissions
from .partials.tag_permissions import tag_permissions
from .partials.task_permissions import task_permissions

from NearBeach.views.error_views import error_403


FUNCTION_DICT = {
    "change_task": change_task_permissions,
    # "customer",
    "kanban": kanban_board_permissions,
    "kanban_board": kanban_board_permissions,
    "kanban_card": kanban_card_permissions,
    "kanban_column": kanban_column_permissions,
    "kanban_level": kanban_level_permissions,
    "request_for_change": request_for_change_permissions,
    "requirement": requirement_permissions,
    "requirement_item": requirement_item_permissions,
    "organisation": organisation_permissions,
    "object_note": object_note_permissions,
    "project": project_permissions,
    "tag": tag_permissions,
    "task": task_permissions,
}


def check_user_generic_permissions(min_permission_level):
    """
    Checks the user's generic permissions. It will gather both the
    - destination
    - location id
    from the *args and **kwargs.
    From here it will determine which partial permission it should
    be checking against. The result from the partial will determine
    if the user is granted permission or denied.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Obtain destination from args
            # Due to weird issue - we check the args length
            if len(args) == 0:
                destination = kwargs['destination']
            else:
                destination = args[0]

            # If sub object, use partials
            if destination == "kanban_card":
                # Setup kwargs to have kanban_card_id
                kwargs["kanban_card_id"] = kwargs["location_id"]
                passes, user_level = kanban_card_permissions(request, kwargs)
            elif destination == "requirement_item":
                # Setup kwargs to have requirement item id
                kwargs["requirement_item_id"] = kwargs["location_id"]
                passes, user_level = requirement_item_permissions(request, kwargs)
            elif destination == "change_task":
                # Setup kwargs to have change task id
                kwargs["change_task_id"] = kwargs["location_id"]
                passes, user_level = change_task_permissions(request, kwargs)
            elif destination == "organisation":
                passes, user_level = organisation_permissions(request, kwargs)
            else:
                passes, user_level = generic_permissions(request, destination, kwargs)

            if not passes:
                raise PermissionDenied

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_specific_object_permissions(min_permission_level, object_lookup):
    """
    Checks the user's permissions against the provided object_lookup.
    From here it will determine which partial permission it should
    be checking against. The result from the partial will determine
    if the user is granted permission or denied.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            if object_lookup == "":
                raise PermissionDenied

            # Use the FUNCTION_DICT to determine which partial permissions we need to
            # reference
            passes, user_level = FUNCTION_DICT[object_lookup](request, kwargs)

            if not passes:
                raise PermissionDenied
                raise error_403
                # HttpResponseRedirect()HttpResponseRedirect

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator
