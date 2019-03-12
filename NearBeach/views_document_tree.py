from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import  loader
from NearBeach.forms import *
from .models import *
from .misc_functions import *
from django.db.models import Q
from .user_permissions import return_user_permission_level

import simplejson

@login_required(login_url='login',redirect_field_name="")
def delete_document(request,document_key):
    if request.method == "POST":
        # Delete the document
        document_instance = document.objects.get(document_key=document_key)
        document_instance.is_deleted = "TRUE"
        document_instance.change_user = request.user
        document_instance.save()

        document_permission_save = document_permission.objects.get(document_key=document_key)
        document_permission_save.is_deleted = "TRUE"
        document_permission_save.change_user = request.user
        document_permission_save.save()

        print("Deleted Document: " + document_key)

        # Return a blank page for fun
        t = loader.get_template('NearBeach/blank.html')

        # context
        c = {}

        return HttpResponse(t.render(c, request))
    else:
        return HttpResponseBadRequest("Can only do this action in post.")


@login_required(login_url='login',redirect_field_name="")
def delete_folder(request, folder_id):
    if request.method == "POST":
        folder_results = folder.objects.get(folder_id=folder_id)
        folder_results.is_deleted = "TRUE"
        folder_results.change_user = request.user
        folder_results.save()

        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c,request))
    else:
        return HttpResponseBadRequest("Sorry, this request has to be post")


@login_required(login_url='login',redirect_field_name="")
def document_tree_folder(request, location_id, destination, folder_id=''):
    if request.method == "POST":
        form = new_folder_form(request.POST)
        if form.is_valid():
            folder_submit = folder(
                folder_description=form.cleaned_data['folder_description'],
                change_user=request.user,
            )

            if folder_id == "" or folder_id == None or folder_id == "0" or folder_id == 0:
                print("There is a bug in python here")
            else:
                print("FOLDER ID = " + str(folder_id))
                folder_submit.parent_folder_id=folder.objects.get(folder_id=folder_id)

            if destination == "project":
                folder_submit.project_id=project.objects.get(project_id=location_id)
            elif destination == "task":
                folder_submit.task_id=task.objects.get(task_id=location_id)
            elif destination == "customer":
                folder_submit.customer_id=customer.objects.get(customer_id=location_id)
            elif destination == "organisation":
                folder_submit.organisation_id=organisation.objects.get(organisation_id=location_id)
            elif destination == "request_for_change":
                folder_submit.request_for_change=request_for_change.objects.get(rfc_id=location_id)

            folder_submit.save()


            t = loader.get_template('NearBeach/blank.html')

            c = {}

            return HttpResponse(t.render(c,request))
        else:
            print(form.errors)
            return HttpResponseBadRequest("Form not valid")
    else:
        return HttpResponseBadRequest("Requst must be a POST")


@login_required(login_url='login',redirect_field_name="")
def document_tree_list(request, location_id, destination, folder_id=''):
    permission_results = return_user_permission_level(request, None, destination)

    if destination == "project":
        folder_results = folder.objects.filter(
            is_deleted="FALSE",
            project_id=location_id,
        )
        document_permission_results = document_permission.objects.filter(
            is_deleted="FALSE",
            project_id=location_id,
        )
    elif destination == "task":
        folder_results = folder.objects.filter(
            is_deleted="FALSE",
            task_id=location_id,
        )
        document_permission_results = document_permission.objects.filter(
            is_deleted="FALSE",
            task_id=location_id,
        )
    elif destination == "customer":
        folder_results = folder.objects.filter(
            is_deleted="FALSE",
            customer_id=location_id,
        )
        document_permission_results = document_permission.objects.filter(
            is_deleted="FALSE",
            customer_id=location_id,
        )
    elif destination == "organisation":
        folder_results = folder.objects.filter(
            is_deleted="FALSE",
            organisation_id=location_id,
        )
        document_permission_results = document_permission.objects.filter(
            is_deleted="FALSE",
            organisation_id=location_id,
        )
    elif destination == "requirement":
        folder_results = folder.objects.filter(
            is_deleted="FALSE",
            requirement_id=location_id,
        )
        document_permission_results = document_permission.objects.filter(
            is_deleted="FALSE",
            requirement_id=location_id,
        )
    elif destination == "request_for_change":
        folder_results = folder.objects.filter(
            is_deleted="FALSE",
            request_for_change=location_id,
        )
        document_permission_results = document_permission.objects.filter(
            is_deleted="FALSE",
            request_for_change=location_id,
        )

    if folder_id:
        folder_results = folder_results.filter(parent_folder_id=folder_id)
        document_permission_results = document_permission_results.filter(folder_id=folder_id)
        current_folder_results = folder.objects.get(folder_id=folder_id)
    else:
        folder_results = folder_results.filter(parent_folder_id__isnull=True)
        document_permission_results = document_permission_results.filter(folder_id__isnull=True)
        folder_id=0 #A non existing folder!
        current_folder_results=""

    # Load the template
    t = loader.get_template('NearBeach/document_tree/document_tree_list.html')

    # context
    c = {
        'document_permission_results': document_permission_results,
        'folder_results': folder_results,
        'destination': destination,
        'location_id': location_id,
        'folder_id': folder_id,
        'document_upload_form': document_upload_form(),
        'document_url_form': document_url_form(),
        'new_folder_form': new_folder_form(),
        'current_folder_results': current_folder_results,
        'permission_results': permission_results[destination],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login',redirect_field_name="")
def document_tree_upload(request, location_id, destination, folder_id):
    if request.method == "POST":
        if request.FILES == None:
            return HttpResponseBadRequest('File needs to be uploaded')

        form = document_upload_form(request.POST, request.FILES)
        if form.is_valid():
            #Get form data
            file = form.cleaned_data['document']
            document_description = form.cleaned_data['document_description']

            # Data objects required
            if document_description == "":
                document_description = str(file)
            file_size = file.size

            """
            File Uploads
            """
            document_submit = document(
                document_description=document_description,
                document=file,
                change_user=request.user,
            )
            document_submit.save()

            document_permissions_submit = document_permission(
                document_key=document_submit,
                change_user=request.user,
            )
            if destination == "project":
                document_permissions_submit.project_id = project.objects.get(project_id=location_id)
            elif destination == "task":
                document_permissions_submit.task_id = task.objects.get(task_id=location_id)
            elif destination == "customer":
                document_permissions_submit.customer_id = customer.objects.get(customer_id=location_id)
            elif destination == "organisation":
                document_permissions_submit.organisation_id = organisation.objects.get(organisation_id=location_id)
            elif destination == "requirement":
                document_permissions_submit.requirement_id = requirement.objects.get(requirement_id=location_id)
            elif destination == "request_for_change":
                document_permissions_submit.request_for_change = request_for_change.objects.get(rfc_id=location_id)

            # NEST UPLOAD TO CURRENT FOLDER
            if folder_id == 0 or folder_id == '0' or not folder_id:
                print("Due to a python bug. We have to do this like this :'(")
            else:
                print("There is an else")
                document_permissions_submit.folder_id = folder.objects.get(folder_id=folder_id)

            document_permissions_submit.save()

            result = []
            result.append({
                "name": document_description,
                "size": file_size,
                "url": '',
                "thumbnail_url": '',
                "delete_url": '/',
                "delete_type": "POST",
            })
            response_data = simplejson.dumps(result)
            return HttpResponse(response_data, content_type='application/json')
        else:
            print(form.errors)
            return HttpResponseBadRequest("Sorry, there was an issue with the form")
    else:
        return HttpResponseBadRequest("Sorry, this function is only a POST function")


@login_required(login_url='login',redirect_field_name="")
def document_tree_url(request,location_id,destination,folder_id=''):
    if request.method == "POST":
        form = document_url_form(request.POST)
        if form.is_valid():
            document_submit = document(
                document_url_location=form.cleaned_data['document_url_location'],
                document_description=form.cleaned_data['document_description'],
                change_user=request.user,
            )
            document_submit.save()

            document_permissions_submit = document_permission(
                document_key=document_submit,
                change_user=request.user,
            )
            if destination == "project":
                document_permissions_submit.project_id = project.objects.get(project_id=location_id)
            elif destination == "task":
                document_permissions_submit.task_id = task.objects.get(task_id=location_id)
            elif destination == "customer":
                document_permissions_submit.customer_id = customer.objects.get(customer_id=location_id)
            elif destination == "organisation":
                document_permissions_submit.organisation_id = organisation.objects.get(organisation_id=location_id)
            elif destination == "requirement":
                document_permissions_submit.requirement_id = requirement.objects.get(requirement_id=location_id)
            elif destination == "request_for_change":
                document_permissions_submit.request_for_change = request_for_change.objects.get(rfc_id=location_id)
            # Must apply other objects

            # NEST UPLOAD TO CURRENT FOLDER
            if folder_id == 0 or folder_id == '0' or not folder_id:
                print("Due to a python bug. We have to do this like this :'(")
            else:
                print("There is an else")
                document_permissions_submit.folder_id = folder.objects.get(folder_id=folder_id)

            document_permissions_submit.save()

            # send back a blank page
            t = loader.get_template('NearBeach/blank.html')

            c = {}

            return HttpResponse(t.render(c, request))
        else:
            print(form.errors)

            return HttpResponseBadRequest("Form is not valid")
    else:
        return HttpResponseBadRequest("Request can only be post")

