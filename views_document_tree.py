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


@login_required(login_url='login')
def document_tree_list(request, location_id, destination, folder_id=''):
    #NOTE - need to add in permission for read only users.

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
    else:
        #TEMP CODE - will need to expand to utilise other objects
        document_permission_results = document_permission.all() #haha - ALL
        folder_results = folder.objects.all()

    if folder_id:
        folder_results = folder_results.filter(parent_folder_id=folder_id)
        document_permission_results = document_permission_results.filter(folder_id=folder_id)
    else:
        folder_results = folder_results.filter(parent_folder_id__isnull=True)
        document_permission_results = document_permission_results.filter(folder_id__isnull=True)
        folder_id=0 #A non existing folder!

    # Load the template
    t = loader.get_template('NearBeach/document_tree/document_tree_list.html')

    print("PRIVATE MEDIA: " + settings.PRIVATE_MEDIA_URL)

    # context
    c = {
        'document_permission_results': document_permission_results,
        'folder_results': folder_results,
        'destination': destination,
        'location_id': location_id,
        'folder_id': folder_id,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def document_tree_upload(request, location_id, destination, folder_id):
    if request.method == "POST":
        if request.FILES == None:
            return HttpResponseBadRequest('File needs to be uploaded')

        # Get the file data
        print(request.FILES)
        file = request.FILES['fileupload']

        # Data objects required
        filename = str(file)
        file_size = file.size
        print("File name: " + filename + "\nFile Size: " + str(file_size))

        """
        File Uploads
        """
        document_submit = document(
            document_description=filename,
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
        #Must apply other objects


        #NEST UPLOAD TO CURRENT FOLDER
        if not folder_id == 0:
            document_permissions_submit.folder_id = folder.objects.get(folder_id=folder_id)

        document_permissions_submit.save()

        result = []
        result.append({
            "name": filename,
            "size": file_size,
            "url": '',
            "thumbnail_url": '',
            "delete_url": '/',
            "delete_type": "POST",
        })
        response_data = simplejson.dumps(result)
        return HttpResponse(response_data, content_type='application/json')
    else:
        return HttpResponseBadRequest("Sorry, this function is only a POST function")


