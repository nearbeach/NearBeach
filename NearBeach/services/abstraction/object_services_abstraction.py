from abc import ABC, abstractmethod
from typing import Any, Dict, List, NamedTuple, Tuple, Union

from django.contrib.auth.models import User
from django.db.models import Manager
from rest_framework.request import Request

from NearBeach.models.request_for_change.change_task import ChangeTask
from NearBeach.models.project import Project
from NearBeach.models.task import Task
from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.requirement.requirement_item import RequirementItem

# Ids arrive from the URL as strings, but services are also called with ints
ObjectId = Union[int, str]

# What each service method hands back to the view - (data, http status)
ServiceResponse = Tuple[Union[Dict, List, str], int]


class AuthenticatedRequest(Request):
    """Type-only view of a Request - the permission decorators guarantee a logged-in user"""
    user: User


# OBJECT STRUCTURE TYPE
class OBJECT_STRUCTURE(NamedTuple):
    object_id: str
    object_title: str
    object_status: str
    object_type: str
    non_null_field: str


class ObjectServiceAbstraction(ABC):
    """Service to help list/add/delete object links"""
    object_dict: Dict[str, Manager[Any]] = {
        "change_task": ChangeTask.objects,
        "project": Project.objects,
        "task": Task.objects,
        "requirement": Requirement.objects,
        "requirement_item": RequirementItem.objects,
    }

    def __init__(self, destination: str, location_id: ObjectId):
        """Initialize the class"""
        self.destination = destination
        self.location_id = location_id

    @abstractmethod
    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        pass # Method not required in current class

    @abstractmethod
    def delete(self, request: AuthenticatedRequest, object_id: Any) -> ServiceResponse:
        pass # Method not required in current class

    @abstractmethod
    def get_list(self, request: AuthenticatedRequest) -> ServiceResponse:
        pass # Method not required in current class

    @abstractmethod
    def update(self, request: AuthenticatedRequest, object_id: Any) -> ServiceResponse:
        pass # Method not required in current class
