from NearBeach.models import (
    ListOfProjectStatus,
    ListOfRequirementItemStatus,
    ListOfRequirementStatus,
    ListOfTaskStatus,
)

OBJECT_DICT = {
    "project": ListOfProjectStatus.objects,
    "requirement_item": ListOfRequirementItemStatus.objects,
    "requirement": ListOfRequirementStatus.objects,
    "task": ListOfTaskStatus.objects,
}

def get_object_status_from_destination(destination):
    return OBJECT_DICT[destination]
