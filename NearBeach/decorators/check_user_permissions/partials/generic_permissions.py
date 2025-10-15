from django.db.models import Max, Q
from django.http import HttpResponseBadRequest

from NearBeach.models import (
    ChangeTask,
    Group,
    KanbanBoard,
    ObjectAssignment,
    Requirement,
    Sprint,
    UserGroup,
)
from NearBeach.utils.api.is_child_object import is_child_object


def generic_permissions(request, object_lookup, kwargs):
    user = request.user if hasattr(request, "user") else request.request.user

    # Extra Permissions
    extra_permissions = ""
    if "extra_permissions" in kwargs:
        extra_permissions = kwargs.get("extra_permissions")

    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=user,
    )

    # If we are passing the object_lookup through, we will use a different function
    if "location_id" in kwargs and not object_lookup == "organisation":
        # If object is a child object, we want to look at the parent object's permission
        location_id, object_lookup = _fetch_parent_details(kwargs, object_lookup)

        # Determine if there are any cross over with user groups and object_lookup groups
        group_results = Group.objects.filter(
            Q(
                is_deleted=False,
                # The object_lookup groups
                group_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    **{object_lookup: location_id},
                ).values("group_id"),
            )
            & Q(group_id__in=user_group_results.values("group_id"))
        )

        # Check to make sure the user groups intersect
        if len(group_results) == 0:
            # There are no matching groups - i.e. the user does not have any permission
            return False, 0, False

    # Get the max permission value from user_group_results
    user_level = user_group_results.aggregate(
        Max(f"permission_set__{object_lookup.replace('_id', '')}")
    )[f"permission_set__{object_lookup.replace('_id', '')}__max"]

    extra_level = False
    if extra_permissions == "document":
        extra_level = user_group_results.filter(
            permission_set__document=1,
        ).count() > 0

    if extra_permissions == "note":
        extra_level = user_group_results.filter(
            **{F"permission_set__{object_lookup}_note": 1}
        ).count() > 0

    return True, user_level, extra_level


def _fetch_parent_details(kwargs, object_lookup):
    # Set the default location id
    location_id = kwargs["location_id"]

    # If the object is NOT a child object - we'll pass back the results
    if not is_child_object(object_lookup):
        return location_id, object_lookup

    match object_lookup:
        case "change_task":
            object_lookup = "request_for_change"
            object_results = ChangeTask.objects.get(pk=location_id)
            location_id = object_results.request_for_change_id
        case "kanban_card":
            object_lookup = "kanban_board"
            object_results = KanbanBoard.objects.get(pk=location_id)
            location_id = object_results.kanban_board_id
        case "requirement_item":
            object_lookup = "requirement"
            object_results = Requirement.objects.get(pk=location_id)
            location_id = object_results.requirement_id
        case "sprint":
            object_results = Sprint.objects.get(pk=location_id)
            object_lookup = "requirement" if object_results.project is None else "project"
            location_id = object_results.requirement_id if object_results.project is None else object_results.project_id
        case _:
            raise HttpResponseBadRequest("Invalid child object")

    return location_id, object_lookup
