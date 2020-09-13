from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.template import loader
from NearBeach.views.tools.internal_functions import *
from django.core.serializers.json import DjangoJSONEncoder

from ..forms import *

import json, os

@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def document_add_folder(request,destination,location_id):
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
    folder_submit = folder(
        change_user=request.user,
        folder_description=form.cleaned_data['folder_description'],
        parent_folder=form.cleaned_data['parent_folder'],
    )
    folder_submit = set_object_from_destination(folder_submit,destination,location_id)
    folder_submit.save()

    # Return the data back
    folder_results = folder.objects.filter(folder_id=folder_submit.folder_id)

    return HttpResponse(serializers.serialize('json',folder_results),content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def document_add_link(request,destination,location_id):
    """

    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    # ADD IN PERMISSION CHECKS

    # Get the form data
    form = AddLinkForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return HttpResponseBadRequest(form.errors)

    # Save the document link
    document_submit = document(
        change_user=request.user,
        document_description=form.cleaned_data['document_description'],
        document_url_location=form.cleaned_data['document_url_location'],
    )
    document_submit.save()

    # Save the document permissions
    document_permission_submit = document_permission(
        change_user=request.user,
        document_key=document_submit,
        folder=form.cleaned_data['parent_folder'],
    )
    document_permission_submit = set_object_from_destination(
        document_permission_submit,
        destination,
        location_id
    )
    document_permission_submit.save()

    # Get current document results to send back
    document_results = document_permission.objects.filter(
        is_deleted="FALSE",
        document_key=document_submit,
    ).values(
        'document_key__document_description',
        'document_key__document_url_location',
        'document_key__document',
        'document_key__whiteboard',
        'folder',
    )

    # Send back json data
    json_results = json.dumps(list(document_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')



@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def document_list_files(request,destination,location_id):
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
    document_permission_results = document_permission.objects.filter(
        is_deleted="FALSE",
    ).values(
        'document_key__document_description',
        'document_key__document_url_location',
        'document_key__document',
        'document_key__whiteboard',
        'folder',
    )

    # Limit to the required destination and location id
    document_permission_results = get_object_from_destination(
        document_permission_results,
        destination,
        location_id
    )

    # Send back json data
    json_results = json.dumps(list(document_permission_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')


    # # Get the document information
    # document_results = document.objects.filter(
    #     is_deleted="FALSE",
    #     document_key__in=document_permission_results.values('document_key')
    # )
    #
    # return HttpResponse(serializers.serialize('json',document_results),content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def document_list_folders(request,destination,location_id):
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
    folder_results = folder.objects.filter(
        is_deleted="FALSE",
    )
    folder_results = get_object_from_destination(folder_results,destination,location_id)

    return HttpResponse(serializers.serialize('json',folder_results),content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def document_upload(request,destination,location_id):
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

    # WRITE CODE TO CHECK THE USER'S PERMISSION

    form = DocumentUploadForm(request.POST,request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the document description - if blank we use the file name
    document_description = form.cleaned_data['document_description']
    file = form.cleaned_data['document']
    if document_description == "":
        # Replace the document description with the file name
        document_description = str(file)

    # Add the document row
    document_submit = document(
        change_user=request.user,
        document_description=document_description,
        document=file,
    )
    document_submit.save()

    # Add the document permission row
    document_permission_submit = document_permission(
        change_user=request.user,
        document_key=document_submit,
        folder=form.cleaned_data['parent_folder'],
    )
    document_permission_submit = set_object_from_destination(
        document_permission_submit,
        destination,
        location_id
    )
    document_permission_submit.save()

    # Get current document results to send back
    document_results = document_permission.objects.filter(
        is_deleted="FALSE",
        document_key=document_submit,
    ).values(
        'document_key_id',
        'document_key__document_description',
        'document_key__document_url_location',
        'document_key__document',
        'document_key__whiteboard',
        'folder',
    )

    # Handle the document upload
    handle_file_upload(request.FILES['document'],document_results)

    # Send back json data
    json_results = json.dumps(list(document_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')


#Internal Function
def handle_file_upload(upload_document,document_results):
    """
    This function will upload the file and store it in the private folder destination under a subfolder that contains
    the same document_key value.
    :param upload_document: The FILE itself - to be uploaded
    :param document_results: The document_results - with variables we require
    :return:
    """
    # Make the directory we want to save the file in. The directory will have the document_key
    file_permissions = 0o755 #Look at these permissions later
    path = os.path.join(
        settings.PRIVATE_MEDIA_ROOT,
        '%s' % (document_results[0]['document_key_id'],),
    )
    os.mkdir(path, file_permissions)

    storage_location = '%s/%s/%s' % (
        settings.PRIVATE_MEDIA_ROOT,
        document_results[0]['document_key_id'],
        document_results[0]['document_key__document_description'],
    )

    #Save the upload document in the location
    with open(storage_location,'wb+') as destination:
        for chunk in upload_document.chunks():
            destination.write(chunk)