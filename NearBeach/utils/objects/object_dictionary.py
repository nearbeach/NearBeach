from django.contrib.auth import get_user_model
from NearBeach.models import (
    ChangeTask,
    Customer,
    Project,
    Task,
    Requirement,
    RequirementItem,
    KanbanBoard,
    KanbanCard,
    Organisation,
    RequestForChange,
)


class ObjectDictionary:
    _object_dictionary = {
        "change_task": {
            "fields": {
                "id": "change_task_id",
                "description": "change_task_description",
                "title": "change_task_title",
                "status": "change_task_status",
                "higher_order_status": None,
                "start_date": None,
            },
            "object": ChangeTask.objects,
        },
        "customer": {
            "fields": {
                "id": "customer_id",
                "description": None,
                "title": None,
                "status": None,
                "higher_order_status": None,
                "start_date": None,
            },
            "object": Customer.objects,
        },
        "project": {
            "fields": {
                "id": "project_id",
                "description": "project_description",
                "title": "project_name",
                "status": "project_status",
                "higher_order_status": "project_status__project_higher_order_status",
                "start_date": "project_start_date",
            },
            "object": Project.objects,
        },
        "task": {
            "fields": {
                "id": "task_id",
                "description": "task_long_description",
                "title": "task_short_description",
                "status": "task_status",
                "higher_order_status": "task_status__task_higher_order_status",
                "start_date": "task_start_date",
            },
            "object": Task.objects,
        },
        "requirement": {
            "fields": {
                "id": "requirement_id",
                "description": "requirement_scope",
                "title": "requirement_title",
                "status": "requirement_status",
                "higher_order_status": "requirement_status__requirement_higher_order_status",
                "start_date": None,
            },
            "object": Requirement.objects,
        },
        "requirement_item": {
            "fields": {
                "id": "requirement_item_id",
                "description": "requirement_item_scope",
                "title": "requirement_item_title",
                "status": "requirement_item_status",
                "higher_order_status": "requirement_item_status__requirement_item_higher_order_status",
                "start_date": None,
            },
            "object": RequirementItem.objects,
        },
        "kanban_board": {
            "fields": {
                "id": "kanban_board_id",
                "description": None,
                "title": "kanban_board_name",
                "status": "kanban_board_status",
                "higher_order_status": None,
                "start_date": None,
            },
            "object": KanbanBoard.objects,
        },
        "kanban_card": {
            "fields": {
                "id": "kanban_card_id",
                "description": None,
                "title": "kanban_card_text",
                "status": None,
                "higher_order_status": None,
                "start_date": None,
            },
            "object": KanbanCard.objects,
        },
        "organisation": {
            "fields": {
                "id": "organisation_id",
                "description": "kanban_card_description",
                "title": "kanban_card_text",
                "status": None,
                "higher_order_status": None,
                "start_date": None,
            },
            "object": Organisation.objects,
        },
        "request_for_change": {
            "fields": {
                "id": "rfc_id",
                "description": "rfc_summary",
                "title": "rfc_title",
                "status": "rfc_status",
                "higher_order_status": None,
                "start_date": "rfc_implementation_start_date",
            },
            "object": RequestForChange.objects,
        },
        "user": {
            "fields": {
                "id": "",
                "description": None,
                "title": None,
                "status": None,
                "higher_order_status": None,
                "start_date": None,
            },
            "object": get_user_model().objects,
        }
    }
    objects = None
    id = None
    title = None
    status = None
    higher_order_status = None
    start_date = None
    description = None

    def __init__(self, destination, **kwargs):
        super().__init__()
        reference = self._object_dictionary[destination]
        self.objects = reference["object"]
        self.title = reference["fields"]["title"]
        self.status = reference["fields"]["status"]
        self.higher_order_status = reference["fields"]["higher_order_status"]
        self.start_date = reference["fields"]["start_date"]
        self.description = reference["fields"]["description"]
        self.id = reference["fields"]["id"]
