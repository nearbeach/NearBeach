
from django.db.models import F
from django.utils import timezone
from rest_framework import status
from rest_framework.serializers import Serializer

from NearBeach.models.document.document import Document
from NearBeach.models.document.document_permission import DocumentPermission
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.serializers.documentation.folder_serializer import FolderSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse,
)


class DocumentLinkService(ObjectServiceAbstraction):
    """Class for handling link crud operations"""
    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

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
        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, document_id: str) -> ServiceResponse:
        """Method to delete a link"""
        serializer = FolderSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        document = Document.objects.filter(
            is_deleted=False,
            pk=document_id,
        )

        document_permission = DocumentPermission.objects.filter(
            is_deleted=False,
            document_id=document_id,
            **{F"{self.destination}_id": self.location_id},
        )

        # If there are no values to update - notify the user
        if len(document) == 0 or len(document_permission) == 0:
            return "Document does not exist", status.HTTP_400_BAD_REQUEST

        # Soft delete the data
        document.update(
            change_user=request.user,
            is_deleted=True,
            date_modified=timezone.now(),
        )

        document_permission.update(
            change_user=request.user,
            is_deleted=True,
            date_modified=timezone.now(),
        )

        return {}, status.HTTP_204_NO_CONTENT

    def get_list(self, _: AuthenticatedRequest) -> ServiceResponse:
        raise NotImplementedError  # Method not required in current class

    def update(self, request: AuthenticatedRequest, document_id: str) -> ServiceResponse:
        """Method to update a link"""
        serializer: Serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Check folder exists
        # TODO - Document has no project_id or folder (both live on DocumentPermission), so updating a link
        #  raises a FieldError, and the response serializes the folder rather than the document
        document = Document.objects.get(
            is_deleted=False,
            pk=document_id,
            **{F"documentpermission__{self.destination}_id": self.location_id},
        )
        if document is None:
            return "Folder object does not exist", status.HTTP_400_BAD_REQUEST

        # Update
        if hasattr(serializer.validated_data, "description"):
            document.description = serializer.validated_data["description"]

        if hasattr(serializer.validated_data, "folder"):
            document.folder = serializer.validated_data["folder"]

        if hasattr(serializer.validated_data, "url_location"):
            document.url_location = serializer.validated_data["url_location"]

        document.save()

        # Serialize
        serializer = FolderSerializer(document)

        return serializer.data, status.HTTP_200_OK
