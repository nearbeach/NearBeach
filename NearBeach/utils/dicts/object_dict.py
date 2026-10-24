from typing import Any, Dict

from django.db.models import Manager

from NearBeach.models.request_for_change.change_task import ChangeTask
from NearBeach.models.customer import Customer
from NearBeach.models.kanban_board.kanban_board import KanbanBoard
from NearBeach.models.kanban_board.kanban_card import KanbanCard
from NearBeach.models.organisation import Organisation
from NearBeach.models.project import Project
from NearBeach.models.request_for_change.request_for_change import RequestForChange
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.task import Task

OBJECT_DICT: Dict[str, Manager[Any]] = {
    "change_task": ChangeTask.objects,
    "customer": Customer.objects,
    "kanban_board": KanbanBoard.objects,
    "kanban_card": KanbanCard.objects,
    "request_for_change": RequestForChange.objects,
    "requirement": Requirement.objects,
    "requirement_item": RequirementItem.objects,
    "organisation": Organisation.objects,
    "project": Project.objects,
    "task": Task.objects,
}