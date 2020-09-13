from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.template import loader
from NearBeach.views.tools.internal_functions import *
from django.core.serializers.json import DjangoJSONEncoder


from ..forms import *

import json

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
        'document_key__document_description',
        'document_key__document_url_location',
        'document_key__document',
        'document_key__whiteboard',
        'folder',
    )

    # Send back json data
    json_results = json.dumps(list(document_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')