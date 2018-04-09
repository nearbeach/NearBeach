from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.template import  loader
from NearBeach.forms import *
from .models import *
from .misc_functions import *
from .user_permissions import return_user_permission_level



@login_required(login_url='login')
def new_requirement(request):
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST" and permission_results['requirement'] > 2:
        form = new_requirement_form(request.POST)
        if form.is_valid():
            requirement_title = form.cleaned_data['requirement_title']
            requirement_scope = form.cleaned_data['requirement_scope']
            requirement_type = form.cleaned_data['requirement_type']


            requirements_save = requirements(
                requirement_title=requirement_title,
                requirement_scope=requirement_scope,
                requirement_type=requirement_type,
                requirement_status=form.cleaned_data['requirement_status'],
                change_user=request.user,
            )
            requirements_save.save()

            return HttpResponseRedirect(reverse(requirement_information, args={requirements_save.requirement_id}))
        else:
            print(form.errors)

    #Load template
    t = loader.get_template('NearBeach/new_requirement.html')

    # context
    c = {
        'new_requirement_form': new_requirement_form(),
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def requirement_documents_uploads(request, location_id, destination):
    permission_results = return_user_permission_level(request, None, ['requirement','document'])

    if permission_results['requirement'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        # Get the file data
        file = request.FILES['file']

        # Data objects required
        filename = str(file)
        file_size = file._size
        print("File name: " + filename + "\nFile Size: " + str(file_size))

        """
        File Uploads
        """
        document_save = documents(
            document_description=filename,
            document=file,
            change_user=request.user,
        )
        document_save.save()

        document_permissions_save = document_permissions(
            document_key=document_save,
            change_user=request.user,
        )
        if destination == "requirement":
            document_permissions_save.requirements = requirements.objects.get(requirement_id=location_id)
        else:
            document_permissions_save.requirement_item = requirement_item.objects.get(requirement_item_id=location_id)

        document_permissions_save.save()

    if destination == "requirement":
        document_results = document_permissions.objects.filter(
            is_deleted='FALSE',
            requirements=location_id,
        )
    else:
        document_results = document_permissions.objects.filter(
            is_deleted='FALSE',
            requirement_item=location_id,
        )


    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_documents.html')

    # context
    c = {
        'location_id': location_id,
        'destination': destination,
        'requirement_permissions': permission_results['requirement'],
        'document_permissions': permission_results['document'],
        'document_results': document_results,
    }

    return HttpResponse(t.render(c, request))




@login_required(login_url='login')
def requirement_information(request, requirement_id):
    permission_results = return_user_permission_level(request, None, ['requirement','requirement_link'])

    if permission_results['requirement'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST" and permission_results['requirement'] > 1:
        form = requirement_information_form(request.POST)
        if form.is_valid():
            requirements_update = requirements.objects.get(requirement_id=requirement_id)
            requirements_update.requirement_title = form.cleaned_data['requirement_title']
            requirements_update.requirement_scope = form.cleaned_data['requirement_scope']
            requirements_update.requirement_type = form.cleaned_data['requirement_type']
            requirements_update.requirement_status = form.cleaned_data['requirement_status']
            requirements_update.change_user = request.user
            requirements_update.save()

            """
            Now we need to update any kanban board cards connected to this project.
            """
            kanban_card_results = kanban_card.objects.filter(
                is_deleted="FALSE",
                requirements=requirement_id,
            )
            for row in kanban_card_results:
                print('hello world')
                row.kanban_card_text = "REQ" + str(requirement_id) + " - " + form.cleaned_data['requirement_title']
                row.save()
        else:
            print(form.errors)

    #Setup the initial data for the form
    requirement_results = requirements.objects.get(requirement_id=requirement_id)
    initial = {
        'requirement_title': requirement_results.requirement_title,
        'requirement_scope': requirement_results.requirement_scope,
        'requirement_type': requirement_results.requirement_type,
        'requirement_status': requirement_results.requirement_status,
    }

    #Load template
    t = loader.get_template('NearBeach/requirement_information.html')

    # context
    c = {
        'requirement_id': requirement_id,
        'requirement_information_form': requirement_information_form(initial=initial),
        'permission': permission_results['requirement'],
        'requirement_link_permissions': permission_results['requirement_link'],
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],

    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def requirement_item_edit(request, requirement_item_id):
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST" and permission_results['requirement'] > 1:
        form = requirement_items_form(request.POST)
        if form.is_valid():
            # Save the data
            requirement_item_save = requirement_item.objects.get(requirement_item_id=requirement_item_id)
            requirement_item_save.requirement_item_title=form.cleaned_data['requirement_item_title']
            requirement_item_save.requirement_item_scope=form.cleaned_data['requirement_item_scope']
            requirement_item_save.requirement_item_status=form.cleaned_data['requirement_item_status']
            requirement_item_save.requirement_item_type=form.cleaned_data['requirement_item_type']
            requirement_item_save.change_user=request.user

            requirement_item_save.save()
        else:
            print(form.errors)

    #Get data
    requirement_item_results = requirement_item.objects.get(requirement_item_id=requirement_item_id)

    initial = {
        'requirement_item_title': requirement_item_results.requirement_item_title,
        'requirement_item_scope': requirement_item_results.requirement_item_scope,
        'requirement_item_status': requirement_item_results.requirement_item_status,
        'requirement_item_type': requirement_item_results.requirement_item_type,
    }

    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_item_edit.html')

    # context
    c = {
        'requirement_item_id': requirement_item_id,
        'requirement_items_form': requirement_items_form(initial=initial),
        'permission': permission_results['requirement'],
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],

    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_items_list(request, requirement_id):
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    requirement_items_results = requirement_item.objects.filter(requirement_id=requirement_id)

    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_items_list.html')

    # context
    c = {
        'requirement_id': requirement_id,
        'requirement_items_results': requirement_items_results,
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_items_new(request, requirement_id):
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        form = requirement_items_form(request.POST)
        if form.is_valid():
            requirement_item_title = form.cleaned_data['requirement_item_title']
            requirement_item_scope = form.cleaned_data['requirement_item_scope']
            requirement_item_status = int(request.POST.get('requirement_item_status'))
            requirement_item_type = int(request.POST.get('requirement_item_type'))

            #instances
            item_status_instance = list_of_requirement_item_status.objects.get(pk=requirement_item_status)
            item_type_instance = list_of_requirement_item_type.objects.get(pk=requirement_item_type)
            requirement_instance = requirements.objects.get(requirement_id=requirement_id)

            #Save the data
            requirement_item_save = requirement_item(
                requirement_item_title=requirement_item_title,
                requirement_item_scope=requirement_item_scope,
                requirement_item_status=item_status_instance,
                requirement_item_type=item_type_instance,
                change_user=request.user,
                requirement_id=requirement_instance,
            )

            requirement_item_save.save()

        else:
            print(form.errors)
    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_items_new.html')

    # context
    c = {
        'requirement_items_form': requirement_items_form(),
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_items_new_link(request, requirement_item_id, location_id= '', destination=''):
    permission_results = return_user_permission_level(request, None, 'requirement_link')

    if permission_results['requirement_link'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        #Check to make sure that there exists a location id and project_or_task value
        if location_id == '' or destination == '':
            #Well - this is not good for POST
            return HttpResponseBadRequest("Please note, both location_id and project_or_task will need to be filled out.")

        requirement_item_link_save = requirement_item_links(
            requirement_item_id=requirement_item_id,
            change_user=request.user,
        )

        if destination == "project":
            project_instance = project.objects.get(project_id=location_id)
            requirement_item_link_save.project_id = project_instance
        elif destination == "task":
            task_instance = tasks.objects.get(tasks_id=location_id)
            requirement_item_link_save.task_id = task_instance
        elif destination == "organisation":
            organisation_instance = organisations.objects.get(organisation_id=location_id)
            requirement_item_link_save.organisations_id = organisation_instance
        else:
            return HttpResponseBadRequest("You can only choose: project, task, or organisation")

        if requirement_item_link_save.save():
            print("Save successful")
        else:
            print("Save unsuccessful")

        #Return blank page\
        # Load template
        t = loader.get_template('NearBeach/blank.html')

        # context
        c = {
        }

        return HttpResponse(t.render(c, request))

    """
    The linked items will only link to items the user has access to. Nothing else.
    """
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
      project.project_id
    , project.project_name



    from 
      project left join project_tasks
        on project.project_id = project_tasks.project_id
        and project_tasks.is_deleted = 'FALSE'
    , project_groups
    , user_groups


    where 1 = 1
    and project.project_status IN ('New','Open')
    and project.project_status IN ('New','Open')
    and project.project_id = project_groups.project_id_id
    and project_groups.groups_id_id = user_groups.groups_id
    and user_groups.username_id = %s
    """, [request.user.id])
    project_results = namedtuplefetchall(cursor)

    cursor.execute("""
    select 
     tasks.tasks_id
    , tasks.task_short_description
    
    from 
      tasks 
    , tasks_groups
    , user_groups
    , organisations
    
    
    where 1 = 1
    and tasks.task_status in ('New','Open')
    and tasks.tasks_id = tasks_groups.tasks_id_id
    and tasks_groups.groups_id_id = user_groups.groups_id
    and user_groups.username_id = %s
    and tasks.organisations_id_id=organisations.organisations_id    
    """, [request.user.id])
    task_results = namedtuplefetchall(cursor)

    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_item_new_link.html')

    # context
    c = {
        'requirement_item_id': requirement_item_id,
        'project_results': project_results,
        'task_results': task_results,
    }

    return HttpResponse(t.render(c, request))





@login_required(login_url='login')
def requirement_links_list(request, requirement_id):
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    links_results = requirement_links.objects.filter(
        requirements=requirement_id,
        is_deleted="FALSE",
    )
    item_results = requirement_item.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    )
    item_links_results = requirement_item_links.objects.filter(requirement_item__in=item_results)
    requirement_results = requirements.objects.filter(requirement_id=requirement_id)



    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_links_list.html')

    # context
    c = {
        'item_results': item_results,
        'requirement_results': requirement_results,
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def requirement_new_link(request, requirement_id, location_id='', destination=''):
    permission_results = return_user_permission_level(request, None, 'requirement_link')

    if permission_results['requirement_link'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        print("Requirement ID: " + requirement_id + "\nLocation ID: " + location_id + "\nTask or Project: " + destination)
        #Check to make sure that there exists a location id and project_or_task value
        if location_id == '' or destination == '':
            #Well - this is not good for POST
            print("Please check the URL")
            return HttpResponseBadRequest("Please note, both location_id and project_or_task will need to be filled out.")

        print("Trying to save")
        requirement_link_save = requirement_links(
            requirements=requirements.objects.get(requirement_id=requirement_id),
            change_user=request.user,
        )

        if destination == "project":
            project_instance = project.objects.get(project_id=location_id)
            requirement_link_save.project_id = project_instance
        elif destination == "task":
            task_instance = tasks.objects.get(tasks_id=location_id)
            requirement_link_save.task_id = task_instance
        elif destination == "organisation":
            organisation_instance = organisations.objects.get(organisation_id=location_id)
            requirement_link_save.organisations_id = organisation_instance
        else:
            return HttpResponseBadRequest("You can only choose: project, task, or organisation")

        requirement_link_save.save()

        #Return blank page\
        # Load template
        t = loader.get_template('NearBeach/blank.html')

        # context
        c = {
        }

        return HttpResponse(t.render(c, request))
    """
    The linked requirements will only link to requirements the user has access to. Nothing else.
    """
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
          project.project_id
        , project.project_name



        from 
          project left join project_tasks
            on project.project_id = project_tasks.project_id
            and project_tasks.is_deleted = 'FALSE'
        , project_groups
        , user_groups


        where 1 = 1
        and project.project_status IN ('New','Open')
        and project.project_status IN ('New','Open')
        and project.project_id = project_groups.project_id_id
        and project_groups.groups_id_id = user_groups.groups_id
        and user_groups.username_id = %s
        """, [request.user.id])
    project_results = namedtuplefetchall(cursor)

    cursor.execute("""
        select 
         tasks.tasks_id
        , tasks.task_short_description

        from 
          tasks 
        , tasks_groups
        , user_groups
        , organisations


        where 1 = 1
        and tasks.task_status in ('New','Open')
        and tasks.tasks_id = tasks_groups.tasks_id_id
        and tasks_groups.groups_id_id = user_groups.groups_id
        and user_groups.username_id = %s
        and tasks.organisations_id_id=organisations.organisations_id    
        """, [request.user.id])
    task_results = namedtuplefetchall(cursor)

    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_new_link.html')

    # context
    c = {
        'requirement_id': requirement_id,
        'project_results': project_results,
        'task_results': task_results,

    }

    return HttpResponse(t.render(c, request))