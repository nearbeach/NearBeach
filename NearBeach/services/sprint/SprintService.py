from rest_framework import status

from NearBeach.models.sprint.sprint import Sprint
from NearBeach.serializers.sprint_serializer import SprintSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectId,
    ObjectServiceAbstraction,
    ServiceResponse,
)


class SprintService(ObjectServiceAbstraction):
    """Service to help create, read, update, delete sprint objects"""
    # TODO - actually implement this functionality

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def delete(self, request: AuthenticatedRequest, sprint_id: ObjectId) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def get_list(self, request: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def retrieve(self, request: AuthenticatedRequest) -> ServiceResponse:
        # Get object
        sprint_results = Sprint.objects.get(pk=self.location_id)

        # Get assigned object
        # object_assignments = ObjectAssignment.objects.filter(
        #     is_deleted=False,
        #     project_id=self.location_id,
        # )

        # Define groups list
        # sprint_results.group_list = Group.objects.filter(
        #     is_deleted=False,
        #     id__in=object_assignments.filter(
        #         group_id__isnull=False,
        #     ).values("group_id"),
        # )

        # Define user list
        # project_results.user_list = User.objects.filter(
        #     pk__in=object_assignments.filter(
        #         assigned_user__isnull=False,
        #     ).values("assigned_user_id"),
        # ).annotate(profile_picture=F("userprofilepicture__document_id__key"))

        # Append extra data

        # Create the serializer
        serializer = SprintSerializer(
            sprint_results,
            context={
                "request": request,
                "method": "GET",
            },
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, sprint_id: ObjectId) -> ServiceResponse:
        # Get project
        sprint = Sprint.objects.get(pk=self.location_id)

        # Setup serializer
        serializer = SprintSerializer(
            sprint,
            data=request.data,
            context={
                "request": request,
                "method": "PATCH",
            },
            partial=True,
        )
        if not serializer.is_valid():
            return serializer.errors, False

        # Make sure we update the change user
        # TODO - this sets an attribute on the serializer, so change_user is never saved (class is not used by any view yet)
        serializer.change_user = request.user  # type: ignore[attr-defined]
        serializer.save()

        return serializer.data, status.HTTP_200_OK
