from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectId,
    ObjectServiceAbstraction,
    ServiceResponse,
)


class SprintObjectLinkService(ObjectServiceAbstraction):
    """Service to help create, read, update, delete sprint object links"""

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def delete(self, request: AuthenticatedRequest, sprint_object_link_id: ObjectId) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def get_list(self, request: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def update(self, request: AuthenticatedRequest, sprint_object_link_id: ObjectId) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class