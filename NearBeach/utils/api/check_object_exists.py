from NearBeach.models.request_for_change.change_task import ChangeTask
from NearBeach.models.customer import Customer
from NearBeach.models.kanban_board.kanban_board import KanbanBoard
from NearBeach.models.kanban_board.kanban_card import KanbanCard
from NearBeach.models.organisation import Organisation
from NearBeach.models.project import Project
from NearBeach.models.request_for_change.request_for_change import RequestForChange
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.sprint.sprint import Sprint
from NearBeach.models.task import Task

import logging

_logger = logging.getLogger(__name__)
_mapping = {
    'change_task': ChangeTask.objects,
    'customer': Customer.objects,
    'kanban_board': KanbanBoard.objects,
    'kanban_card': KanbanCard.objects,
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
        nb_object = _mapping[destination].filter(
            pk=location_id,
            is_deleted=False,    
        )

        # pk is unique, so the object exists if any row comes back
        return nb_object.exists()
    except KeyError:
        _logger.error(
            "check_object_exists: unknown destination: %s | unknown location %s | KeyError: %s",
            destination,
            location_id,
            KeyError
        )
        return False
