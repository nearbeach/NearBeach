from django.db.models import F
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

        # Extract data before model - bug when not done like this
        description=serializer.validated_data['description']
        url_location=serializer.validated_data['url_location']

        # Save the document link
        document_submit = Document(
            change_user=request.user,
            creation_user=request.user,
            description=description,
            url_location=url_location,
            upload_successfully=True,
        )
        document_submit.save()

        # Save the document permissions
        document_permission_submit = DocumentPermission(
            change_user=request.user,
            creation_user=request.user,
            document=document_submit,
            **{F"{self.destination}_id": self.location_id},
        )

        # If parent folder exists
        if "parent_folder_id" in serializer.validated_data:
            document_permission_submit.folder_id = serializer.validated_data["parent_folder_id"]

        document_permission_submit.save()

        # Get current document results to send back
        document_results = DocumentPermission.objects.filter(
            is_deleted=False,
            document=document_submit,
        ).annotate(
            description=F("document__description"),
            url_location=F("document__url_location"),
            key=F("document__key"),
            parent_folder_id=F("folder_id"),
        ).values(
            "document",
            "description",
            "url_location",
            "key",
            "parent_folder_id",
        )

        # Serialize
        serializer = DocumentSerializer(document_results.first())

        # Return
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        ), True

    def delete(self, request, document_id):
        """Method to delete a link"""
        document = Document.objects.filter(
            is_deleted=False,
            pk=document_id,
        )

        document_permission = DocumentPermission.objects.filter(
            is_deleted=False,
            document=document_id,
            **{F"{self.destination}_id": self.location_id},
        )

        # If there are no values to update - notify the user
        if len(document) == 0 or len(document_permission) == 0:
            return False

        # Soft delete the data
        document.update(
            change_user=request.user,
            is_deleted=True,
        )

        document_permission.update(
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
