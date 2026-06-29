from NearBeach.models import Document, DocumentPermission
from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.services.document.file_handler.GetFileHandler import get_file_handler
from django.conf import settings
from django.db.models import F

FILE_HANDLER = get_file_handler(settings)


def handle_document_permissions(request, destination, location_id, file, serializer, is_profile_picture):
    """
    The function that handles the document permission - i.e. if user has access to the
    document then it'll send it to the user, otherwise it will send a 404 not found.
    Please note - we don't use permission denied here to hopefully trip people up
    """
    document_submit = Document(
        change_user=request.user,
        description=serializer.validated_data["description"],
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
        **{F"{destination}_id": location_id},
    )

    # Apply the parent folder if required
    parent_folder_id = serializer.validated_data["parent_folder_id"]
    if parent_folder_id != 0:
        document_permission_submit.folder = parent_folder_id

    # Save document permission
    document_permission_submit.save()

    # Handle the file upload
    upload = request.FILES["document"]
    FILE_HANDLER.upload(upload, document_submit, file)

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
