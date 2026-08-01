from typing import Dict, Tuple, Union

from rest_framework import status
from NearBeach.models import Folder
from NearBeach.serializers.documentation.folder_serializer import FolderSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class FolderService(ObjectServiceAbstraction):
    """Class for handling folder crud operations"""

    def create(self, request) -> Tuple[Union[Dict, str], int]:
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

        # return data
        serializer = FolderSerializer(
            folder_submit,
        )

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request, folder_id) -> Tuple[Union[Dict, str], int]:
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
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, request):
        pass

    def update(self, request, folder_id) -> Tuple[Union[Dict, str], int]:
        """Method to update a folder"""
        serializer = FolderSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Check folder exists
        folder = Folder.objects.get(
            is_deleted=False,
            pk=folder_id,
            **{F"{self.destination}_id": self.location_id},
        )
        if folder is None:
            return "Folder object does not exist", status.HTTP_400_BAD_REQUEST

        # Update
        description = serializer.validated_data['description']
        parent_folder = serializer.validated_data['parent_folder']

        # 'true' if True else 'false'
        folder.change_user = request.user
        folder.description = folder.description if description is None else description
        folder.parent_folder = folder.parent_folder if parent_folder is None else parent_folder
        folder.save()

        # Serialize
        serializer = FolderSerializer(folder)

        return serializer.data, status.HTTP_200_OK
