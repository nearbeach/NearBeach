from abc import ABC

from rest_framework import status
from rest_framework.response import Response
from NearBeach.models import Folder
from NearBeach.serializers.documentation.folder_serializer import FolderSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class FolderService(ObjectServiceAbstraction):
    """Class for handling folder crud operations"""

    def create(self, request):
        serializer = FolderSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

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

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        ), True

    def delete(self, request, folder_id):
        """Method to delete a folder"""
        folder = Folder.objects.filter(
            is_deleted=False,
            pk=folder_id,
            **{F"{self.destination}_id": self.location_id},
        )

        # If there are no values to update - notify the user
        if len(folder) == 0:
            return False

        # Soft delete the data
        folder.update(
            change_user=request.user,
            is_deleted=True,
        )

        return True

    def get_list(self, request):
        pass

    def update(self, request, folder_id):
        """Method to update a folder"""
        serializer = FolderSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Check folder exists
        folder = Folder.objects.get(
            is_deleted=False,
            pk=folder_id,
            **{F"{self.destination}_id": self.location_id},
        )
        if folder is None:
            return {"Folder object does not exist"}, False

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

        return serializer, True
