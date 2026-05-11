from abc import ABC, abstractmethod
from collections import namedtuple

from NearBeach.models import (
    ChangeTask,
    Project,
    Task,
    Requirement,
    RequirementItem,
)

# OBJECT STRUCTURE TYPE
OBJECT_STRUCTURE = namedtuple(
    "ObjectStructure",
    [
        "object_id",
        "object_title",
        "object_status",
        "object_type",
        "non_null_field"
    ]
)


class ObjectServiceAbstraction(ABC):
    """Service to help list/add/delete object links"""
    object_dict = {
        "change_task": ChangeTask.objects,
        "project": Project.objects,
        "task": Task.objects,
        "requirement": Requirement.objects,
        "requirement_item": RequirementItem.objects,
    }

    def __init__(self, destination: str, location_id: int):
        """Initialize the class"""
        self.destination = destination
        self.location_id = location_id

    @abstractmethod
    def create(self, request):
        pass

    @abstractmethod
    def delete(self, request, object_id):
        pass

    @abstractmethod
    def get_list(self, request):
        pass

    @abstractmethod
    def update(self, request, object_id):
        pass
