from django.db.models import Manager

from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.utils.api.get_destination import get_child_object_from_url

# child destination -> (parent destination, child objects, name of the field holding the parent's id)
_CHILD_OBJECTS: dict[str, tuple[str, Manager, str]] = {
    "requirement_item": ("requirement", RequirementItem.objects, "requirement_id"),
}


def check_child_belongs_to_parent(url: str, parent_destination: str, parent_location_id: int) -> bool:
    """Make sure a child object in the url (e.g. a requirement item) belongs to the parent in the url

    The permission decorators check the user's access to the first object in the url - the parent. Without this check
    anyone who can reach one parent could reach the child of any other parent by putting its id in the url.

    Urls without a child object (including sub-resources such as notes) are fine. A child that does not exist, or that
    belongs to another parent, is not.
    """
    child_destination, child_location_id = get_child_object_from_url(url)
    if child_destination not in _CHILD_OBJECTS or child_location_id is None:
        return True

    expected_parent, child_objects, parent_field = _CHILD_OBJECTS[child_destination]
    if parent_destination != expected_parent or not child_location_id.isnumeric():
        return False

    return child_objects.filter(
        pk=int(child_location_id),
        is_deleted=False,
        **{parent_field: parent_location_id},
    ).exists()
