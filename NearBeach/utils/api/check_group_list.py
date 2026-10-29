from typing import List, Union
from django.contrib.auth.models import User
from NearBeach.models.user import Group, UserGroup
import logging

_logger = logging.getLogger(__name__)

def check_group_list(username: User, group_list: List[Union[Group, int]]) -> bool:
    """
    Utility function to check if user has access to all groups in the list

    Method
    ~~~~~~
    1. Run query on UserGroup and select distinct by username & group name
    2. If the results are greater than 0, then user has permission

    Users are only required to be in a minimum of 1 group to have permission.
    """
    try:
        # Deduplicate group_list
        group_ids = list({group.pk if isinstance(group, Group) else group for group in group_list})

        # Filter for these groups
        user_group_results = UserGroup.objects.filter(
            is_deleted=False,
            username=username,
            group_id__in=group_ids,
        ).values(
            'username',
            'group',
        ).distinct().count()

        # Return results
        return user_group_results > 0
    except ValueError:
        _logger.error(
            "check_group_list - username: %s | group_list: %s | ValueError: %s",
            username,
            group_list,
            ValueError
        )
        return False
