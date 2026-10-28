
from rest_framework import status
from rest_framework.serializers import Serializer
from django.db.models import F
from NearBeach.models.document.document import Document
from NearBeach.models.document.document_permission import DocumentPermission
from NearBeach.models.document.folder import Folder
from NearBeach.serializers.documentation.document_delete_serializer import DocumentDeleteSerializer
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
        serializer = DocumentDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # The document has to be on this object - that link lives on the document permission
        document_permission = DocumentPermission.objects.filter(
            is_deleted=False,
            document_id=document_id,
            document__is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        )
        if len(document_permission) == 0:
            return "Document object does not exist", status.HTTP_400_BAD_REQUEST

        Document.objects.filter(pk=document_id).update(
            change_user=request.user,
            date_modified=timezone.now(),
            is_deleted=True,
        )

        # Remove the document permission
        document_permission.update(
            change_user=request.user,
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
        """Method for updating an uploaded document - its description and the folder it is in"""
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # The document has to be on this object - that link lives on the document permission
        document_permission = DocumentPermission.objects.filter(
            is_deleted=False,
            document_id=document_id,
            document__is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        )
        if len(document_permission) == 0:
            return "Document object does not exist", status.HTTP_400_BAD_REQUEST

        # Update the document
        document = Document.objects.get(pk=document_id)
        document.description = serializer.validated_data["description"]
        document.change_user = request.user
        document.date_modified = timezone.now()
        document.save()

        # The folder it lives in is on the permission - 0 means the root
        if "parent_folder_id" in serializer.validated_data:
            document_permission.update(
                folder_id=serializer.validated_data["parent_folder_id"] or None,
                change_user=request.user,
                date_modified=timezone.now(),
            )

        # Serialize the document - the same shape as when it was uploaded
        serializer = DocumentSerializer(
            DocumentPermission.objects.filter(
                is_deleted=False,
                document=document,
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
            ).first()
        )

        return serializer.data, status.HTTP_200_OK
