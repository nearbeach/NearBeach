from rest_framework import status
from django.utils import timezone
from django.db.models import Value

from NearBeach.serializers.public_link_serializer import PublicLinkSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse, )
from NearBeach.models.misc.misc import PublicLink
from NearBeach.models import Project
from NearBeach.serializers.public_link_data_serializer import PublicLinkDataSerializer


class PublicLinkService(ObjectServiceAbstraction):
    """Class for creating, reading, updating, and deleting public links"""

    @staticmethod
    def _fetch_kanban_board_data(pk: int) -> ServiceResponse:
        # TODO - Implement
        return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def _fetch_kanban_card_data(pk: int) -> ServiceResponse:
        # TODO - Implement
        return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def _fetch_project_data(pk: int) -> ServiceResponse:
        project_results = Project.objects.filter(
            pk=pk,
            is_deleted=False,
        ).annotate(
            object_type=Value("project"),
        ).first()

        if project_results is None:
            return "Project does not exist", status.HTTP_404_NOT_FOUND

        serializer = PublicLinkDataSerializer(
            project_results,
            many=False
        )

        return serializer.data, status.HTTP_200_OK

    @staticmethod
    def _fetch_request_for_change_data(pk: int) -> ServiceResponse:
        # TODO - Implement
        return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def _fetch_requirement_data(pk: int) -> ServiceResponse:
        # TODO - Implement
        return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def _fetch_requirement_item_data(pk: int) -> ServiceResponse:
        # TODO - Implement
        return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def _fetch_task_data(pk: int) -> ServiceResponse:
        # TODO - Implement
        return {}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        # Create the public link
        # TODO - Move this creation step into the serializer?
        new_public_link = PublicLink(
            **{F"{self.destination}_id": self.location_id},
            creation_user=request.user,
            change_user=request.user,
        )
        new_public_link.save()

        # Serializer
        serializer = PublicLinkSerializer(new_public_link)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, object_id: str) -> ServiceResponse:
        delete_public_link = PublicLink.objects.filter(
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
            pk=object_id,
        )

        # If it does not exist - send back to user
        if len(delete_public_link) == 0:
            return "Public Link does not exist", status.HTTP_400_BAD_REQUEST

        delete_public_link.update(
            is_deleted=True,
            change_user=request.user,
            date_modified=timezone.now(),
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request: AuthenticatedRequest) -> ServiceResponse:
        public_links = PublicLink.objects.filter(
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        )

        serializer = PublicLinkSerializer(
            public_links,
            many=True,
        )

        return serializer.data, status.HTTP_200_OK

    def retrieve(self, request: AuthenticatedRequest) -> ServiceResponse:
        # Get object
        public_link_results = PublicLink.objects.filter(
            is_deleted=False,
            id=str(self.location_id),
        )

        public_link = public_link_results.first()
        if public_link is None:
            return "Public Link does not exist", status.HTTP_404_NOT_FOUND

        # Fetch the data depending on the field connection
        if public_link.kanban_board_id is not None:
            return self._fetch_kanban_board_data(public_link.kanban_board_id)
        elif public_link.kanban_card_id is not None:
            return self._fetch_kanban_card_data(public_link.kanban_card_id)
        elif public_link.project_id is not None:
            return self._fetch_project_data(public_link.project_id)
        elif public_link.request_for_change_id is not None:
            return self._fetch_request_for_change_data(public_link.request_for_change_id)
        elif public_link.requirement_id is not None:
            return self._fetch_requirement_data(public_link.requirement_id)
        elif public_link.requirement_item_id is not None:
            return self._fetch_requirement_item_data(public_link.requirement_item_id)
        elif public_link.task_id is not None:
            return self._fetch_task_data(public_link.task_id)

        # Error - there is an issue with the link
        return "Public link not setup correctly", status.HTTP_400_BAD_REQUEST

    def update(self, request: AuthenticatedRequest, object_id: str) -> ServiceResponse:
        serializer = PublicLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # The serializer keeps this optional (it is read-only on create) - but an update needs it
        if "is_active" not in serializer.validated_data:
            return {"is_active": ["This field is required."]}, status.HTTP_400_BAD_REQUEST

        update_public_link = PublicLink.objects.filter(
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
            pk=object_id,
        )

        if len(update_public_link) == 0:
            return "Public Link does not exist", status.HTTP_400_BAD_REQUEST

        update_public_link.update(
            change_user=request.user,
            is_active=serializer.validated_data["is_active"],
            date_modified=timezone.now(),
        )

        return serializer.data, status.HTTP_200_OK
