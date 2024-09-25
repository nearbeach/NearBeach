from NearBeach.models import Group, KanbanCard, ObjectAssignment, UserGroup
from django.db.models import Max, Q


# Internal Function
def kanban_card_permissions(request, kwargs):
    # Extra Permissions
    extra_permissions = ""
    if "extra_permissions" in kwargs:
        extra_permissions = kwargs.get("extra_permissions")

    # Default user level is 0
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    if len(kwargs) > 0:
        # Determine if there are any cross over with user groups and object_lookup groups
        group_results = Group.objects.filter(
            Q(
                is_deleted=False,
                # The object_lookup groups
                group_id__in=ObjectAssignment.objects.filter(
                    is_deleted=False,
                    kanban_board_id__in=KanbanCard.objects.filter(
                        kanban_card_id=kwargs["kanban_card_id"],
                    ).values("kanban_board_id"),
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
        Max("permission_set__kanban_board")
    )["permission_set__kanban_board__max"]

    # Check all variations of the extra permissions
    extra_level = False
    if extra_permissions == "document":
        extra_level = user_group_results.filter(
            permission_set__document=1,
        ).count() > 0

    if extra_permissions == "note":
        extra_level = user_group_results.filter(
            permission_set__kanban_note=1,
        ).count() > 0

    return True, user_level, extra_level

