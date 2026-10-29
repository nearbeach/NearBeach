import logging

_logger = logging.getLogger(__name__)

def get_destination_from_url(url : str) -> str | None:
    """
    Utility function get the destination from the url

    Notes
    ~~~~~
    Assuming the url will be in the following patterns;
    /api/v1/<destination>/
    /api/v1/<destination>/<location_id>/
    /api/v1/<destination>/<location_id/<child_destination>/
    /api/v1/<destination>/<location_id/<child_destination>/<child_location_id>/

    Method
    ~~~~~~
    1. Trim '/' character from the start of the url
    2. Split url by '/' character
    3. Return the 3rd position which will be the destination
    """
    try:
        parts = url.lstrip('/').rstrip('/').split('/')

        # Check to make sure we are correct
        if len(parts) < 3:
            return None

        # Destination only
        return parts[2]
    except ValueError:
        _logger.error("get_destination_from_url: %s | ValueError: %s", url, ValueError)
        return None

def get_object_from_url(url: str) -> tuple[None, None] | tuple[str, str]:
    """
    Utility function to object from the url

    Notes
    ~~~~~
    Assuming the url will be in the following patterns;
    /api/v1/<destination>/
    /api/v1/<destination>/<location_id>/
    /api/v1/<destination>/<location_id/<child_destination>/
    /api/v1/<destination>/<location_id/<child_destination>/<child_location_id>/

    Method
    ~~~~~~
    1. Trim '/' character from the start of the url
    2. Split url by '/' character
    3. Return the 3rd and 4th positions which will be the destination and location id
    """
    try:
        parts = url.lstrip('/').rstrip('/').split('/')

        # Check to make sure we are correct
        if len(parts) < 4:
            return None, None

        # Destination only
        return parts[2], parts[3]
    except ValueError:
        _logger.error("get_object_from_url: %s | ValueError: %s", url, ValueError)
        return None, None

