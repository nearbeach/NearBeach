from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core import serializers
from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    Http404,
    FileResponse,
    JsonResponse,
)
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404

from NearBeach.views.tools.internal_functions import (
    set_object_from_destination,
    get_object_from_destination,
)
from ..forms import (
    AddFolderForm,
    Folder,
    AddLinkForm,
    Document,
    DocumentRemoveForm,
    DocumentUploadForm,
    RequirementItem,
)
from ..models import DocumentPermission, UserGroup, ObjectAssignment, UserProfilePicture

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import boto3
import json
import os


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def document_add_folder(request, destination, location_id):
    """
    This will add a folder to the user's destination and location_id
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    # Check users PERMISSION - NEED TO ADD

    # Obtain the data and verify against the form
    form = AddFolderForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the form information
    folder_submit = Folder(
        change_user=request.user,
        folder_description=form.cleaned_data["folder_description"],
        parent_folder=form.cleaned_data["parent_folder"],
    )
    folder_submit = set_object_from_destination(folder_submit, destination, location_id)
    folder_submit.save()

    # Return the data back
    folder_results = Folder.objects.filter(folder_id=folder_submit.folder_id)

    return HttpResponse(
        serializers.serialize("json", folder_results), content_type="application/json"
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def document_add_link(request, destination, location_id):
    """
    Will add a link to the document
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    # ADD IN PERMISSION CHECKS

    # Get the form data
    form = AddLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the document link
    document_submit = Document(
        change_user=request.user,
        document_description=form.cleaned_data["document_description"],
        document_url_location=form.cleaned_data["document_url_location"],
    )
    document_submit.save()

    # Save the document permissions
    document_permission_submit = DocumentPermission(
        change_user=request.user,
        document_key=document_submit,
        folder=form.cleaned_data["parent_folder"],
    )
    document_permission_submit = set_object_from_destination(
        document_permission_submit, destination, location_id
    )
    document_permission_submit.save()

    # Get current document results to send back
    document_results = DocumentPermission.objects.filter(
        is_deleted=False,
        document_key=document_submit,
    ).values(
        "document_key_id",
        "document_key__document_description",
        "document_key__document_url_location",
        "document_key__document",
        "folder",
    )

    # Send back json data
    json_results = json.dumps(list(document_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def document_list_files(request, destination, location_id):
    """
    Get the documents that are associated with the destination and location id

    Method
    ~~~~~~
    1. Get all the document permissions connected to the destination and location
    2. Get the document information from this
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    document_permission_results = DocumentPermission.objects.filter(
        is_deleted=False,
    ).values(
        "document_key_id",
        "document_key__document_description",
        "document_key__document_url_location",
        "document_key__document",
        "folder",
    )

    # Limit to the required destination and location id
    document_permission_results = get_object_from_destination(
        document_permission_results, destination, location_id
    )

    # Send back json data
    json_results = json.dumps(list(document_permission_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")

    # # Get the document information
    # document_results = document.objects.filter(
    #     is_deleted=False,
    #     document_key__in=document_permission_results.values('document_key')
    # )
    #
    # return HttpResponse(serializers.serialize('json',document_results),content_type='application/json')


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def document_list_folders(request, destination, location_id):
    """
    Get the folders that are associated with the destination and location id

    Method
    ~~~~~~
    1. Get all the document permissions connected to the destination and location
    2. Get the folder information from this

    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    # Get the document information
    folder_results = Folder.objects.filter(
        is_deleted=False,
    )
    folder_results = get_object_from_destination(
        folder_results, destination, location_id
    )

    return HttpResponse(
        serializers.serialize("json", folder_results), content_type="application/json"
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def document_remove(request, destination, location_id):
    # Get form data
    form = DocumentRemoveForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)
    
    # Get document from the form
    document_update = form.cleaned_data["document_key"]
    document_update.is_deleted = True
    document_update.save()

    document_permission_update = DocumentPermission.objects.get(document_key = document_update.document_key)
    document_permission_update.is_deleted = True
    document_permission_update.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def document_upload(request, destination, location_id):
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
    :param folder_id: Which folder we will associate this with
    :return:
    """
    form = DocumentUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the document description - if blank we use the file name
    document_description = form.cleaned_data["document_description"]
    file = form.cleaned_data["document"]
    if document_description == "":
        # Replace the document description with the file name
        document_description = str(file)

    # Upload the document
    _, document_results = handle_document_permissions(
        request,
        request.FILES["document"],
        file,
        document_description,
        destination,
        location_id,
        form.cleaned_data["parent_folder"],
    )

    # Send back json data
    json_results = json.dumps(list(document_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type="application/json")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def get_max_upload(request):
    """
    This function will query the settings file for the variable "max_upload_size".
    If it does not exist it will send back
    a simple 0. If it does exist it will send back itself
    :param request:
    :return:
    """
    if hasattr(settings, "MAX_UPLOAD_SIZE"):
        max_upload_size = {"max_upload_size": settings.MAX_UPLOAD_SIZE}
    else:
        max_upload_size = {"max_upload_size": 0}

    return JsonResponse(max_upload_size)


@login_required(login_url="login", redirect_field_name="")
def private_download_file(request, document_key):
    """
    The following function will check;
    1. The user's permission to the document
    2. If the document exists

    From there it will use X-Sendfile to send the document.
    :param request:
    :param document_key:
    :return:
    """
    # Extract the user groups the user is associated with
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        username=request.user,
    )

    # Extract the permissions the document is associated with
    document_permission_results = DocumentPermission.objects.filter(
        is_deleted=False,
        document_key=document_key,
    )

    # Consolidate at the object assignment
    object_assignment_results = ObjectAssignment.objects.filter(
        Q(
            is_deleted=False,
            # JOIN IN USER GROUPS
            group_id__in=user_group_results.values("group_id"),
        )
        & Q(
            # One of these conditions have to be met
            # Q(
            #     # If the document is uploaded against a customer
            #     customer__isnull=False,
            # )
            # | Q(
            #     # If the document is uploaded against an organisation
            #     organisation__isnull=False,
            # )
            Q(
                # Project Links
                project__isnull=False,
                project_id__in=document_permission_results.values("project_id"),
            )
            | Q(
                # Task links
                task__isnull=False,
                task_id__in=document_permission_results.values("task_id"),
            )
            | Q(
                # Requirement
                requirement__isnull=False,
                requirement_id__in=document_permission_results.values("requirement_id"),
            )
            | Q(
                # Requirement Item
                # Have to use the requirement item's requirement as permissions are not on the item
                requirement_id__in=RequirementItem.objects.filter(
                    is_deleted=False,
                    requirement_item_id__in=document_permission_results.values(
                        "requirement_item_id"
                    ),
                    requirement_item_id__isnull=False,
                ).values("requirement_id")
            )
            | Q(
                # Request for change
                request_for_change__isnull=False,
                request_for_change_id__in=document_permission_results.values(
                    "request_for_change_id"
                ),
            )
        )
    )

    profile_picture_permission = document_permission_results.filter(
        Q(
            customer__isnull=False,
        )
        | Q(organisation__isnull=False)
    )

    user_profile_picture = UserProfilePicture.objects.filter(
        document=document_key,
        is_deleted=False,
    )

    # If the object_assignment_results.count() == 0, then user does not have permissions
    if (
        object_assignment_results.count() == 0
        and profile_picture_permission.count() == 0
        and user_profile_picture.count() == 0
        and request.user.is_superuser is False
    ):
        raise Http404

    # Get Document information
    document_results = get_object_or_404(Document, document_key=document_key)

    # If not a document but a URL
    if document_results.document_url_location:
        return HttpResponseRedirect(document_results.document_url_location)

    # If S3 has been setup - download file from S3 bucket
    if getattr(settings, "AWS_ACCESS_KEY_ID", None):
        # Use boto3 to download
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        response = s3.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"{document_results.document}",
        )

        return FileResponse(
            response["Body"],
            as_attachment=True,
            filename=document_results.document_description,
        )
    elif getattr(settings, "AZURE_STORAGE_CONNECTION_STRING", None):
        # Use Azure to download
        blob_service_client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )

        # Get container
        container_client = blob_service_client.get_container_client(
            container=settings.AZURE_STORAGE_CONTAINER_NAME
        )

        # Setup the file to send
        file_to_send = ContentFile(
            container_client.download_blob(
                f"{document_results.document}"
            ).readall()
        )

        # Return file
        return FileResponse(
            file_to_send,
            as_attachment=True,
            filename=document_results.document_description,
        )

    # Normal setup - find document on server and serve
    # Get the Document path information
    path = f"{settings.PRIVATE_MEDIA_ROOT}/{document_results.document}"

    # Send file to user
    return FileResponse(open(path, "rb"))


# Internal Function
def handle_document_permissions(
    request, upload, file, document_description, destination, location_id, parent_folder = 0
):
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
    document_submit.document = f"private/{document_submit.document_key}/{file}"
    document_submit.save()

    # Add the document permission row
    document_permission_submit = DocumentPermission(
        change_user=request.user,
        document_key=document_submit,
    )
    document_permission_submit = set_object_from_destination(
        document_permission_submit, destination, location_id
    )

    # Apply the parent folder if required
    if parent_folder is not 0:
        document_permission_submit.folder = parent_folder
    
    # Save document permission
    document_permission_submit.save()

    # Get current document results to send back
    document_results = DocumentPermission.objects.filter(
        is_deleted=False,
        document_key=document_submit,
    ).values(
        "document_key_id",
        "document_key__document_description",
        "document_key__document_url_location",
        "document_key__document",
        "folder",
    )

    # Handle the document upload
    if getattr(settings, "AWS_ACCESS_KEY_ID", None):
        # Use boto to upload the file
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        # Upload a new file
        s3.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            f"private/{document_submit.document_key}/{file}",
        )
    elif getattr(settings, "AZURE_STORAGE_CONNECTION_STRING", None):
        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )

        # Create the blob client using the private file path name as the name for the blob
        blob_client = blob_service_client.get_blob_client(
            container=settings.AZURE_STORAGE_CONTAINER_NAME, 
            blob=f"private/{document_submit.document_key}/{file}",
        )

        # Upload the created file
        blob_client.upload_blob(file)
    else:
        handle_file_upload(upload, document_results, file)

    return document_submit, document_results


# Internal Function
def handle_file_upload(upload_document, document_results, file):
    """
    This function will upload the file and store it in the private folder destination under a subfolder that contains
    the same document_key value.
    :param upload_document: The FILE itself - to be uploaded
    :param document_results: The document_results - with variables we require
    :return:
    """
    # Make the directory we want to save the file in. The directory will have the document_key
    file_permissions = 0o755  # Look at these permissions later
    path = os.path.join(
        settings.PRIVATE_MEDIA_ROOT,
        f"private/{document_results[0]['document_key_id']}",
    )
    os.mkdir(path, file_permissions)

    storage_location = f"{settings.PRIVATE_MEDIA_ROOT}/private/{document_results[0]['document_key_id']}/{file}"

    # Save the upload document in the location
    with open(storage_location, "wb+") as destination:
        for chunk in upload_document.chunks():
            destination.write(chunk)
