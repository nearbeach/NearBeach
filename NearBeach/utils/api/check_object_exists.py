from NearBeach.models import (
    ChangeTask,
    Customer,
    KanbanBoard,
    KanbanCard,
    Organisation,
    Project,
    RequestForChange,
    Requirement,
    RequirementItem,
    Sprint,
    Task,
)

import logging

_logger = logging.getLogger(__name__)
_mapping = {
    'change_task': ChangeTask.objects,
    'customer': Customer.objects,
    'kanban_board': KanbanBoard.objects,
    'kanban_card': KanbanCard,
    'organisation': Organisation.objects,
    'project': Project.objects,
    'request_for_change': RequestForChange.objects,
    'requirement': Requirement.objects,
    'requirement_item': RequirementItem.objects,
    'sprint': Sprint.objects,
    'task': Task.objects,
}

def check_object_exists(destination: str, location_id: int) -> bool:
    """Function to check to make sure a NearBeach object exists"""
    try:
        nb_object = _mapping[destination]
        nb_object = nb_object.filter(
            pk=location_id,
            is_deleted=False,    
        )

        # If there is exactly one object, the object exists
        return len(nb_object) == 1
    except KeyError:
        _logger.error(F"check_object_exists: unknown destination: {destination} | unknown location {location_id} | KeyError: {KeyError}")
        return False
