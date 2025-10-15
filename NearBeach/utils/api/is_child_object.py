def is_child_object(object_type):
    return object_type in [
        "change_task",
        "kanban_card",
        "requirement_item",
        "sprint",
    ]
