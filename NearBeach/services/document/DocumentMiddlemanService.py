from typing import Dict, Tuple, Union

from rest_framework import status

from NearBeach.serializers.documentation.document_delete_serializer import DocumentDeleteSerializer
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.services.document.DocumentLinkService import DocumentLinkService
from NearBeach.services.document.DocumentService import DocumentService
from NearBeach.services.document.FolderService import FolderService


class DocumentMiddlemanService(ObjectServiceAbstraction):
    """Middleman Service to help point at the correct document service"""

    def create(self, request) -> Tuple[Union[Dict, str], int]:
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Depending on the type - depends on what we do
        match serializer.validated_data["type"]:
            case "folder":
                folder_service = FolderService(
                    destination="project",
                    location_id=self.location_id,
                )

                # Return results
                return folder_service.create(request)
            case "link":
                link_service = DocumentLinkService(
                    destination="project",
                    location_id=self.location_id,
                )

                # Return results
                return link_service.create(request)
            case _:
                document_service = DocumentService(
                    destination="project",
                    location_id=self.location_id,
                )

                # Return results
                return document_service.create(request)

    def delete(self, request, document_pk) -> Tuple[Union[Dict, str], int]:
        serializer = DocumentDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Depending on the type - depends on what we do
        match serializer.validated_data["type"]:
            case "folder":
                folder_service = FolderService(
                    destination="project",
                    location_id=self.location_id
                )

                # Return results
                return folder_service.delete(request, document_pk)
            case "link":
                link_service = DocumentLinkService(
                    destination="project",
                    location_id=self.location_id,
                )

                # Return results
                return link_service.delete(request, document_pk)
            case _:
                document_service = DocumentService(
                    destination="project",
                    location_id=self.location_id,
                )

                # Return results
                return document_service.delete(request, document_pk)

    def get_list(self, request):
        pass

    def update(self, request, document_pk) -> Tuple[Union[Dict, str], int]:
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Depending on the type - depends on what we do
        match serializer.validated_data["type"]:
            case "folder":
                folder_service = FolderService(
                    destination="project",
                    location_id=self.location_id,
                )

                # Return data
                return folder_service.update(request, document_pk)
            case "link":
                link_service = DocumentLinkService(
                    destination="project",
                    location_id=self.location_id,
                )

                # Return Data
                return link_service.update(request, document_pk)
            case _:
                document_service = DocumentService(
                    destination="project",
                    location_id=self.location_id,
                )

                # Return Data
                return document_service.update(request, document_pk)
