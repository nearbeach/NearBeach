from django.db.migrations import serializer
from django.db.models import F

from NearBeach.models import Document, DocumentPermission, Folder
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.serializers.documentation.file_system_serializer import FileSystemSerializer
from NearBeach.services.abstraction.object_services_abstraction import ObjectServiceAbstraction
from django.conf import settings
from django.utils import timezone


class DocumentService(ObjectServiceAbstraction):
    """Class for handling document crud operations"""

    @staticmethod
    def _get_max_upload():
        """
        This function will query the settings file for the variable "max_upload_size".
        If it does not exist it will send back
        a simple 0. If it does exist it will send back itself
        """
        if hasattr(settings, "MAX_UPLOAD_SIZE"):
            return settings.MAX_UPLOAD_SIZE

        return 0

    # TODO - pass through serializer to remove most fields
    # TODO - if this is utilized with profile picture uploads - move to an external function
    def _handle_document_permissions(self, request, upload, file, document_description, parent_folder=0,
                                     is_profile_picture=False):
        """
        The function that handles the document permission - i.e. if user has access to the
        document then it'll send it to the user. Otherwise it will send a 404 not found.
        Please note - we don't use permission denied here to hopefully trip people up
        """
        document_submit = Document(
            change_user=request.user,
            document_description=document_description,
        )
        document_submit.save()

        # Add the document location
        document_submit.document = f"private/{document_submit.key}/{file}"
        document_submit.save()

        # Add the document permission row
        document_permission_submit = DocumentPermission(
            change_user=request.user,
            document_key=document_submit,
            is_profile_picture=is_profile_picture,
            **{F"{self.destination}_id": self.location_id},
        )

        # Apply the parent folder if required
        if parent_folder != 0:
            document_permission_submit.folder = parent_folder

        # Save document permission
        document_permission_submit.save()

        # Handle the file upload
        # TODO - Import the FILE HANLDER
        FILE_HANDLER.upload(upload, document_submit, file)
        # TODO FIX

        document_submit.document_upload_successfully = True
        document_submit.save()

        # Serializer
        document_results = Document.objects.filter(
            is_deleted=False,
            key=document_submit,
        ).annotate(
            folder=F("documentpermission__folder"),
        ).values(
            "key",
            "description",
            "url_location",
            "document",
            "folder",
        )
        serializer = DocumentSerializer(document_results)

        return serializer, True

    def create(self, request):
        """
        The following function will deal with the uploaded document. It will first;
        1. Check user's permission
        2. Place the request.POST values into a form for validation
        3. Create a new row in document and store the relevant data inside
        4. Create a new row in document permission and assign it to the appropriate object
        5. Send back the document information in JSON format
        :param request:
        :param destination: the object in question
        :param location_id: The location of the object
        :return:
        """
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Get the document description - if blank we use the file name
        document_description = serializer.validated_data["document_description"]
        file = serializer.validated_data["document"]

        # Check file size upload
        if file.size > settings.MAX_FILE_SIZE_UPLOAD:
            return {"File size too large"}, False

        if document_description == "":
            # Replace the document description with the file name
            document_description = str(file)

        # Upload the document
        # TODO - Review the fields being passed through
        serializer = self._handle_document_permissions(
            request,
            request.FILES["document"],
            file,
            document_description,
            serializer.validated_data["parent_folder"],
        )

        return serializer, True

    def delete(self, request, document_id):
        """Method for removing document"""
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        # Check to make sure data exists
        document = Document.objects.filter(
            is_deleted=False,
            pk=document_id,
            **{F"{self.destination}_id": self.location_id},
        )
        if len(document) == 0:
            return {"Document object does not exist"}, False

        document.update(
            change_user=request.user,
            modification_date=timezone.now(),
            is_deleted=True,
        )

        # Remove the document permission
        DocumentPermission.objects.filter(
            document_id__in=document.values("document_id"),
            **{F"{self.destination}_id": self.location_id},
        ).update(
            is_deleted=True,
            date_modified=timezone.now(),
        )

        return None, True

    def get_list(self, _):
        # Fetch required data
        folder_results = Folder.objects.filter(
            is_deleted=False,
            **{F"{self.destination}_id": self.location_id},
        ).values(
            'id',
            'description',
            'parent_folder',
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
            folder=F("documentpermission__folder"),
        ).values(
            "key",
            "description",
            "url_location",
            "document",
            "folder",
        )

        serializer = FileSystemSerializer({
            "documents": document_results,
            "folders": folder_results,
            "max_upload_size": self._get_max_upload(),
        })

        return serializer

    def update(self, request, document_id):
        serializer = DocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.errors, False

        document = DocumentPermission.objects.get(
            document_key=document_id,
            **{F"{self.destination}_id": self.location_id},
        )
        if document is None:
            return {"Document object does not exist"}, False

        # Update the document
        description = serializer.validated_data["description"]
        folder = serializer.validated_data["folder"]

        document.description = document.description if description is None else description
        document.folder = document.folder if folder is None else folder
        document.save()

        # Serializer
        serializer = DocumentSerializer(document)

        return serializer, True
