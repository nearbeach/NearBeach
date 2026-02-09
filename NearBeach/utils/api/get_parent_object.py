from NearBeach.models import (
    ChangeTask,
    KanbanCard,
    RequirementItem,
)
from NearBeach.utils.api.object_to_permission_set_mapping import get_object_permission_set
import logging

_logger = logging.getLogger(__name__)
_object_mapping = {
    'ChangeTask': ChangeTask.objects,
    'KanbanCard': KanbanCard.objects,
    'RequirementItem': RequirementItem.objects,
}


def _is_child_object(object_type: str) -> bool:
    return object_type in [
        "change_task",
        "kanban_card",
        "requirement_item",
    ]
def get_parent_object(destination: str, location_id: int) -> tuple[str | None, int | None]:
    """Get parent object from the destination and location id

    Method
    ~~~~~~
    1. Check if destination is a child object -> if it is not return destination and location back
    2. Fetch the object
    3. Get the parent object
    4. Return the destination and location id of the parent
    """
    try:
        if not _is_child_object(destination):
            return destination, location_id

        # Get child object and parent destination
        child_object = _object_mapping[destination].get(
            is_deleted=False,
            pk=location_id,
        )
        parent_destination = get_object_permission_set(destination)
        if child_object is None or parent_destination is None:
            return None, None

        # Get the location id
        parent_object = getattr(child_object, parent_destination)
        if parent_object is None:
            return None, None

        # Return the parent destination and parent id
        return parent_destination, parent_object.pk
    except ImportError:
        _logger.error(F"get_parent_object: Destination {destination} | Location Id: {location_id} | ImportError: {ImportError}")
        return None, None
