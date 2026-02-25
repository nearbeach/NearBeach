from typing import List
from NearBeach.models import UserGroup
import logging

_logger = logging.getLogger(__name__)

def check_group_list(username: str, group_list: List[str] | None) -> bool:
    """
    Utility function to check if user has access to all groups in the list

    Method
    ~~~~~~
    1. Run query on UserGroup and select distinct by username & group name
    2. If the results are greater than 0, then user has permission
    """
    try:
        # Deduplicate group_list
        group_list = list(set(group_list))

        # Filter for these groups
        user_group_results = UserGroup.objects.filter(
            is_deleted=False,
            username=username,
            group_id__in=group_list,
        ).values(
            'username',
            'group',
        ).distinct().count()

        # Return results
        return user_group_results > 0
    except ValueError:
        _logger.error(F"check_group_list - username: {username} | group_list: {group_list} | ValueError: {ValueError}")
        return False
