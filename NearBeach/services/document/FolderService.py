from django.utils import timezone

from rest_framework import status
from NearBeach.models.document.folder import Folder
from NearBeach.serializers.documentation.folder_serializer import FolderSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectId,
    ObjectServiceAbstraction,
    ServiceResponse,
)


class FolderService(ObjectServiceAbstraction):
    """Class for handling folder crud operations"""

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        serializer = FolderSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Save the form information
        folder_submit = Folder(
            change_user=request.user,
            creation_user=request.user,
            description=serializer.validated_data['description'],
            **{F"{self.destination}_id": self.location_id},
        )

        # If there is a parent folder - attach to record
        if "parent_folder_id" in serializer.validated_data:
            folder_submit.parent_folder_id = serializer.validated_data['parent_folder_id']

        # Check parent folder
        folder_submit.save()

        serializer = FolderSerializer(
            folder_submit,
        )

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, folder_id: ObjectId) -> ServiceResponse:
        """Method to delete a folder"""
        folder = Folder.objects.filter(
            is_deleted=False,
            pk=folder_id,
            **{F"{self.destination}_id": self.location_id},
        )

        # If there are no values to update - notify the user
        if len(folder) == 0:
            return "Folder does not exist", status.HTTP_400_BAD_REQUEST

        # Soft delete the data
        folder.update(
            change_user=request.user,
            is_deleted=True,
            date_modified=timezone.now(),
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def update(self, request: AuthenticatedRequest, folder_id: ObjectId) -> ServiceResponse:
        """Method to update a folder"""
        serializer = FolderSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Check folder exists
        folder = Folder.objects.filter(
            is_deleted=False,
            pk=folder_id,
            **{F"{self.destination}_id": self.location_id},
        )
        if len(folder) == 0:
            return "Folder object does not exist", status.HTTP_400_BAD_REQUEST

        # Update
        folder.update(
            change_user = request.user,
            date_modified = timezone.now(),
        )

        if "parent_folder" in serializer.validated_data:
            folder.update(parent_folder=serializer.validated_data["parent_folder"])

        if "description" in serializer.validated_data:
            folder.update(description = serializer.validated_data['description'])

        # Serialize
        serializer = FolderSerializer(folder)

        return serializer.data, status.HTTP_200_OK
