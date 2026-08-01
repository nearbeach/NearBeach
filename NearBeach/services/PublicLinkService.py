from typing import Tuple, Union, Dict
from rest_framework import status

from NearBeach.serializers.public_link_serializer import PublicLinkSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.models import PublicLink


class PublicLinkService(ObjectServiceAbstraction):
    """Class for creating, reading, updating, and deleting public links"""

    def create(self, request) -> Tuple[Union[Dict, str], int]:
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

    def delete(self, request, object_id) -> Tuple[Union[Dict, str], int]:
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
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request) -> Tuple[Union[Dict, str], int]:
        public_links = PublicLink.objects.filter(
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        )

        serializer = PublicLinkSerializer(
            public_links,
            many=True,
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request, object_id) -> Tuple[Union[Dict, str], int]:
        serializer = PublicLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

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
        )

        return serializer.data, status.HTTP_200_OK
