import logging

_logger = logging.getLogger(__name__)
_mapping = {
    'change_task': 'request_for_change',
    'customer': 'customer',
    'kanban_board': 'kanban_board',
    'kanban_card': 'kanban_board',
    'organisation': 'organisation',
    'project': 'project',
    'request_for_change': 'request_for_change',
    'requirement': 'requirement',
    'requirement_item': 'requirement',
    'sprint': 'sprint',
    'task': 'task',
}

def get_object_permission_set(destination: str) -> str | None:
    try:
        return _mapping[destination]
    except KeyError:
        _logger.error(F"get_object_permission_set: unknown destination: {destination} | KeyError: {KeyError}")
        return None
