from rest_framework import status
from rest_framework.response import Response

from NearBeach.models import Folder, Document, DocumentPermission
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.serializers.documentation.folder_serializer import FolderSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction


class DocumentLinkService(ObjectServiceAbstraction):
    """Class for handling link crud operations"""
    def create(self, request):
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Save the document link
        document_submit = Document(
            change_user=request.user,
            creation_user=request.user,
            description=serializer.validated_data['description'],
            url_location=serializer.validated_data['url_location'],
            document_upload_successfully=True,
        )
        document_submit.save()

        # Save the document permissions
        document_permission_submit = DocumentPermission(
            change_user=request.user,
            creation_user=request.user,
            document_key=document_submit,
            folder=serializer.validated_data['parent_folder'],
            **{F"{self.destination}_id": self.location_id},
        )
        document_permission_submit.save()

        # Get current document results to send back
        document_results = DocumentPermission.objects.filter(
            is_deleted=False,
            document_key=document_submit,
        ).values(
            "document_key_id",
            "document_key__description",
            "document_key__url_location",
            "document_key__document",
            "folder",
        )

        # Serialize
        serializer = DocumentSerializer(document_results)

        # Return
        return serializer, True

    def delete(self, request, document_id):
        """Method to delete a link"""
        document = Document.objects.filter(
            is_deleted=False,
            pk=document_id,
            **{F"{self.destination}_id": self.location_id},
        )

        # If there are no values to update - notify the user
        if len(document) == 0:
            return False

        # Soft delete the data
        document.update(
            change_user=request.user,
            is_deleted=True,
        )

        return True

    def get_list(self, _):
        pass

    def update(self, request, document_id):
        """Method to update a link"""
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Check folder exists
        document = Document.objects.get(
            is_deleted=False,
            pk=document_id,
            **{F"{self.destination}_id": self.location_id},
        )
        if document is None:
            return {"Folder object does not exist"}, False

        # Update
        description = serializer.validated_data['description']
        folder = serializer.validated_data['folder']
        url_location = serializer.validated_data['url_location']

        document.description = document.description if description is None else description
        document.folder = document.folder if folder is None else folder
        document.url_location = document.url_location if url_location is None else url_location
        document.save()

        # Serialize
        serializer = FolderSerializer(folder)

        return serializer, True
