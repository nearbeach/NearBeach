from NearBeach.serializers.documentation.document_delete_serializer import DocumentDeleteSerializer
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from NearBeach.services.document.DocumentLinkService import DocumentLinkService
from NearBeach.services.document.DocumentService import DocumentService
from NearBeach.services.document.FolderService import FolderService
from NearBeach.utils.api.check_object_exists import check_object_exists
from NearBeach.utils.objects.error_object import ErrorObject


class DocumentMiddlemanService(ObjectServiceAbstraction):
    """Middleman Service to help point at the correct document service"""

    def create(self, request):
        if not check_object_exists(self.destination, self.location_id):
            return ErrorObject("Object does not exist"), False

        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer, False

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

    def delete(self, request, document_pk):
        if not check_object_exists(self.destination, self.location_id):
            return False

        serializer = DocumentDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return False

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

    def update(self, request, document_pk):
        if not check_object_exists(self.destination, self.location_id):
            return ErrorObject("Object does not exist"), False

        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

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
