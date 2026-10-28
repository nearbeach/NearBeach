from rest_framework import status
from django.utils import timezone

from NearBeach.serializers.public_link_serializer import PublicLinkSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse,
)
from NearBeach.models.misc.misc import PublicLink


class PublicLinkService(ObjectServiceAbstraction):
    """Class for creating, reading, updating, and deleting public links"""

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
