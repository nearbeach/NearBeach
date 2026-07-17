from NearBeach.models import (
    ChangeTask,
    Customer,
    KanbanBoard,
    KanbanCard,
    RequestForChange,
    Requirement,
    RequirementItem,
    Organisation,
    Project,
    Task,
)

OBJECT_DICT = {
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