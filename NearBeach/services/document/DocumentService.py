
from rest_framework import status
from rest_framework.serializers import Serializer
from django.db.models import F
from NearBeach.models.document.document import Document
from NearBeach.models.document.document_permission import DocumentPermission
from NearBeach.models.document.folder import Folder
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.serializers.documentation.file_system_serializer import FileSystemSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse,
)
from django.conf import settings
from django.utils import timezone

from NearBeach.services.document.file_handler.HandleDocumentPermissions import handle_document_permissions


class DocumentService(ObjectServiceAbstraction):
    """Class for handling document crud operations"""

    @staticmethod
    def _get_max_upload() -> int:
        """
        This function will query the settings file for the variable "max_upload_size".
        If it does not exist it will send back
        a simple 0. If it does exist it will send back itself
        """
        return getattr(settings, "MAX_UPLOAD_SIZE", 0)

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        """
        The following function will deal with the uploaded document. It will first;
        1. Check user's permission
        2. Place the request.POST values into a form for validation
        3. Create a new row in document and store the relevant data inside
        4. Create a new row in document permission and assign it to the appropriate object
        5. Send back the document information in JSON format
        """
        serializer: Serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Check file size upload
        file = serializer.validated_data["document"]
        if file.size > settings.MAX_FILE_SIZE_UPLOAD:
            return "File size too large", status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

        # Upload the document
        serializer = handle_document_permissions(
            request=request,
            destination=self.destination,
            location_id=self.location_id,
            file=file,
            serializer=serializer,
            is_profile_picture=False,
        )

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, document_id: str) -> ServiceResponse:
        """Method for removing document"""
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Check to make sure data exists
        # TODO - Document has no project_id (the link lives on DocumentPermission) and no document_id,
        #  so deleting an uploaded document raises a FieldError
        document = Document.objects.filter(
            is_deleted=False,
            pk=document_id,
            **{F"{self.destination}_id": self.location_id},
        )
        if len(document) == 0:
            return "Document object does not exist", status.HTTP_400_BAD_REQUEST

        document.update(
            change_user=request.user,
            date_modified=timezone.now(),
            is_deleted=True,
        )

        # Remove the document permission
        DocumentPermission.objects.filter(
            document_id__in=document.values("document_id"),  # type: ignore[misc]
            **{F"{self.destination}_id": self.location_id},
        ).update(
            is_deleted=True,
            date_modified=timezone.now(),
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, _: AuthenticatedRequest) -> ServiceResponse:
        # Fetch required data
        folder_results = Folder.objects.filter(
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        ).values(
            'id',
            'description',
            'parent_folder_id',
        )

        document_permission_results = DocumentPermission.objects.filter(
            is_deleted=False,
            document__upload_successfully=True,
            is_profile_picture=False,
            **{F"{self.destination}_id": self.location_id},
        )

        document_results = Document.objects.filter(
            is_deleted=False,
            key__in=document_permission_results.values("document_id"),
        ).annotate(
            parent_folder_id=F("documentpermission__folder"),
        ).values(
            "key",
            "description",
            "url_location",
            "document",
            "parent_folder_id",
        )

        serializer = FileSystemSerializer({
            "documents": document_results,
            "folders": folder_results,
            "max_upload_size": self._get_max_upload(),
        })

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, document_id: str) -> ServiceResponse:
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # TODO - DocumentPermission has no document_key or description, so updating an uploaded document
        #  raises a FieldError. Probably meant document_id here and document.document.description below
        document = DocumentPermission.objects.get(  # type: ignore[misc]
            document_key=document_id,
            **{F"{self.destination}_id": self.location_id},
        )
        if document is None:
            return "Document object does not exist", status.HTTP_400_BAD_REQUEST

        # Update the document
        description = serializer.validated_data["description"]
        folder = serializer.validated_data["folder"]

        document.description = document.description if description is None else description  # type: ignore[attr-defined]
        document.folder = document.folder if folder is None else folder
        document.save()

        # Serializer
        serializer = DocumentSerializer(document)

        return serializer.data, status.HTTP_200_OK
