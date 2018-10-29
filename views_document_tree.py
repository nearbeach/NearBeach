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
def document_tree_create_folder(request, location_id, project_or_task):
    permission_results = return_user_permission_level(request, None,['project','document','task'])

    #Permission for either project or task
    if project_or_task == "P":
        general_permission = permission_results['project']
    else:
        general_permission = permission_results['task']

    if request.method == "POST":
        print(request.POST)
        form = document_tree_create_folder_form(request.POST,location_id=location_id, project_or_task=project_or_task)
        if form.is_valid():
            folder_description = form.cleaned_data['folder_description']
            nested_folder = request.POST.get('nested_folder')


            #Save the folder
            folders_save = folder(
                folder_description=folder_description,
                change_user=request.user,
            )

            if nested_folder == '':
                print("")
                """
                Python bug here. I can not get
                if not nested_folder == '':
                to work correctly. So I have a blank print statement for the opposite
                of the condition I was looking for and then an else to bring in the 
                condition I want.
                """
            else:
                folders_save.parent_folder_id = folder.objects.get(folder_id=int(nested_folder))

            if project_or_task == 'P':
                folders_save.project_id = project.objects.get(project_id=location_id)
            else:
                folders_save.project_id = task.objects.get(task_id=location_id)

            folders_save.save()



        else:
            print(form.errors)


    #Load template
    t = loader.get_template('NearBeach/document_tree/document_tree_create_folder.html')


    # context
    c = {
        'create_folder_form': document_tree_create_folder_form(
            location_id=location_id,
            project_or_task=project_or_task,
        ),
        'general_permission': general_permission,
        'document_permission': permission_results['document'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def document_tree_list(request, location_id, project_or_task, folder_id='',):
    #Get Data
    folder_results = folder.objects.filter(is_deleted="FALSE")
    document_results = document_permission.objects.filter(is_deleted="FALSE")



    #Filter for project_or_task
    if project_or_task == 'P':
        #Project
        project_instance = project.objects.get(project_id=location_id)

        folder_results = folder_results.filter(project_id=project_instance)
        document_results = document_results.filter(project_id=project_instance)
    elif project_or_task == 'T':
        #Tasks
        task_instance=task.objects.get(task_id=location_id)

        folder_results = folder_results.filter(task_id=task_instance)
        document_results = document_results.filter(task_id=task_instance)
    else:
        #ERROR
        return  HttpResponseBadRequest("Sorry, but we can not tell if this is a project or task!")

    #Filter for folder_id
    if folder_id == '':
        folder_instance = '' #Empty if no folder instance
        folder_results = folder_results.filter(parent_folder_id=None)

        """
        We only want those document who are not in a folder. So we look up all document that were in a folder
        and exclude them from the document results.
        """
        document_folder_results = document_folder.objects.filter(is_deleted="FALSE")
        document_results = document_results.filter(~Q(document_key__in=document_folder_results.values('document_key')))
    else:
        folder_instance = folder.objects.get(folder_id=folder_id)
        folder_results = folder_results.filter(parent_folder_id=folder_instance)

        """
        We only want those document who are contained in the folder specified. So we look up all the 
        document that are in that specific folder and only include them.
        """
        document_folder_results = document_folder.objects.filter(
            is_deleted="FALSE",
            folder_id=folder_instance
        )
        document_results = document_results.filter(Q(document_key__in=document_folder_results.values('document_key')))

    # Load the template
    t = loader.get_template('NearBeach/document_tree/document_tree_list.html')

    print("PRIVATE MEDIA: " + settings.PRIVATE_MEDIA_URL)

    # context
    c = {
        'folder_results': folder_results,
        'document_results': document_results,
        'folder_id': folder_id,
        'folder_instance': folder_instance,
        'location_id': location_id,
        'project_or_task': project_or_task,
        'PRIVATE_MEDIA_URL': settings.PRIVATE_MEDIA_URL,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def document_tree_upload(request, location_id, project_or_task):
    if request.method == "POST":
        if request.FILES == None:
            return HttpResponseBadRequest('File needs to be uploaded')

        #Get the file data
        file = request.FILES['document']
        nested_folder = request.POST.get('nested_folder')

        #Data objects required
        filename = str(file)
        file_size = file._size
        print("File name: " + filename + "\nFile Size: " + str(file_size))

        """
        File Uploads
        """
        document_save = document(
            document_description=filename,
            document=file,
            change_user=request.user,
        )
        document_save.save()

        document_permissions_save = document_permission(
            document_key=document_save,
            change_user=request.user,
        )
        if project_or_task == "P":
            #Project
            project_instance = project.objects.get(project_id=location_id)
            document_permissions_save.project_id = project_instance
        else:
            #Task
            task_instance = task.objects.get(tasks_id=location_id)
            document_permissions_save.task_id = task_instance
        document_permissions_save.save()

        if nested_folder == '':
            print("")
            #PYTHON BUG HERE - this is the work around
        else:
            document_folder_save = document_folder(
                document_key=document_save,
                folder_id=folder.objects.get(folder_id=nested_folder),
                change_user=request.user,
            )
            document_folder_save.save()

        result = []
        result.append({
            "name" : filename,
            "size" : file_size,
            "url" : '',
            "thumbnail_url" : '',
            "delete_url" : '/',
            "delete_type" : "POST",
        })
        response_data = simplejson.dumps(result)
        return HttpResponse(response_data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Only POST accepted')



def document_tree_upload_documents(request, location_id, project_or_task):
    permission_results = return_user_permission_level(request, None,['project','task','document'])
    if project_or_task == "P":
        general_permission = permission_results['project']
    else:
        general_permission = permission_results['task']

    # Load the template
    t = loader.get_template('NearBeach/document_tree/document_tree_upload_documents.html')

    # context
    c = {
        'location_id': location_id,
        'project_or_task': project_or_task,
        'upload_form': document_tree_upload_form(
            location_id=location_id,
            project_or_task=project_or_task,
        ),
        'general_permission': general_permission,
        'document_permission': permission_results['document'],
    }

    return HttpResponse(t.render(c, request))




