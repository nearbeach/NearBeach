from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.template import  loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from .models import *
from .misc_functions import *
from .user_permissions import return_user_permission_level
from .views import permission_denied



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
            requirement_permission = form.cleaned_data['requirement_permission']


            requirement_save = requirement(
                requirement_title=requirement_title,
                requirement_scope=requirement_scope,
                requirement_type=requirement_type,
                requirement_status=form.cleaned_data['requirement_status'],
                change_user=request.user,
            )
            requirement_save.save()

            """
            Permissions granting
            """
            for row in requirement_permission:
                submit_permission = object_assignment(
                    requirement_id=requirement_save,
                    group_id=row,
                    change_user=request.user,
                )
                submit_permission.save()

            return HttpResponseRedirect(reverse(requirement_information, args={requirement_save.requirement_id}))
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
def new_requirement_item(request, requirement_id):
    """
    If a user wants to create a new requirement item against a requirement, they will need this function. It will deal
    with both creation of the form and the creation of the requirement item.
    :param request:
    :param requirement_id: The requirement that this requirement item will be connected to
    :return: Either the form page, or return to the requirement

    Method
    ~~~~~~
    1. Check the user's permission
    2. Check to see if the method is in POST - read instructions in here
    3. Obtain any required SQL
    4. Get template and context
    5. Render the page
    """
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        #Check the form
        form = requirement_item_form(request.POST)
        if form.is_valid():
            """
            Method
            ~~~~~~
            1. Get any instances required
            2. Setup the requirement_item
            3. Save the requirement item
            4. Send user back to the requirement connected to the requirement item
            """

            # Get instances
            requirement_instance = requirement.objects.get(requirement_id=requirement_id)


            # Setup the requirement_item
            requirement_item_submit = requirement_item(
                requirement_item_title=form.cleaned_data['requirement_item_title'],
                requirement_item_scope=form.cleaned_data['requirement_item_scope'],
                requirement_item_status=form.cleaned_data['requirement_item_status'],
                requirement_item_type=form.cleaned_data['requirement_item_type'],
                change_user=request.user,
                requirement_id=requirement_instance,
            )
            requirement_item_submit.save()

            # Return user to the requirement information page they came from
            return HttpResponseRedirect(reverse('requirement_information', args={ requirement_id }))

        else:
            print(form.errors)

    # Get any required data
    requirement_results = requirement.objects.get(requirement_id=requirement_id)

    #Load template
    t = loader.get_template('NearBeach/new_requirement_item.html')

    # context
    c = {
        'new_requirement_item_form': new_requirement_item_form,
        'requirement_id': requirement_id,
        'requirement_results': requirement_results,
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
        if destination == "requirement":
            document_permissions_save.requirement = requirement.objects.get(requirement_id=location_id)
        else:
            document_permissions_save.requirement_item = requirement_item.objects.get(requirement_item_id=location_id)

        document_permissions_save.save()

    if destination == "requirement":
        document_results = document_permission.objects.filter(
            is_deleted='FALSE',
            requirement=location_id,
        )
    else:
        document_results = document_permission.objects.filter(
            is_deleted='FALSE',
            requirement_item=location_id,
        )


    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_documents.html')

    # context
    c = {
        'location_id': location_id,
        'destination': destination,
        'requirement_permission': permission_results['requirement'],
        'document_permission': permission_results['document'],
        'document_results': document_results,
    }

    return HttpResponse(t.render(c, request))




@login_required(login_url='login')
def requirement_information(request, requirement_id):
    permission_results = return_user_permission_level(request, None, ['requirement','requirement_link'])

    if permission_results['requirement'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    """
    Test User Access
    ~~~~~~~~~~~~~~~~
    A user who wants to access this requirements will need to meet one of these two conditions
    1. They have an access to  a group whom has been granted access to this requirements
    2. They are a super user (they should be getting access to all objects)
    """
    object_access = object_assignment.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
        group_id__in=user_group.objects.filter(
            is_deleted="FALSE",
            username=request.user,
        ).values('group_id')
    )
    if object_access.count() and not permission_results['administration'] == 4:
        return HttpResponseRedirect(reverse('permission_denied'))


    if request.method == "POST" and permission_results['requirement'] > 1:
        form = requirement_information_form(request.POST)
        if form.is_valid():
            requirement_update = requirement.objects.get(requirement_id=requirement_id)
            requirement_update.requirement_title = form.cleaned_data['requirement_title']
            requirement_update.requirement_scope = form.cleaned_data['requirement_scope']
            requirement_update.requirement_type = form.cleaned_data['requirement_type']
            requirement_update.requirement_status = form.cleaned_data['requirement_status']
            requirement_update.change_user = request.user
            requirement_update.save()

            """
            Now we need to update any kanban board cards connected to this project.
            """
            kanban_card_results = kanban_card.objects.filter(
                is_deleted="FALSE",
                requirement=requirement_id,
            )
            for row in kanban_card_results:
                row.kanban_card_text = "REQ" + str(requirement_id) + " - " + form.cleaned_data['requirement_title']
                row.save()
        else:
            print(form.errors)
    else:
        """
        We want to limit who can see what requirement. The exception to this is for the user
        who just created the opportunity. (I should program in a warning stating that they
        might not be able to see the opportunity again unless they add themselfs to the 
        permissions list.

        The user has to meet at least one of these conditions;
        1.) User has permission
        2.) User's group has permission
        3.) All users have permission
        """
        user_groups_results = user_group.objects.filter(username=request.user)

        requirement_permission_results = object_assignment.objects.filter(
            Q(
                Q(assigned_user=request.user) # User has permission
                | Q(group_id__in=user_groups_results.values('group_id')) # User's group have permission
            )
            & Q(requirement_id=requirement_id)
        )

        if (not requirement_permission_results):
            return HttpResponseRedirect(reverse(permission_denied))


    #Get Data
    requirement_results = requirement.objects.get(requirement_id=requirement_id)
    requirement_item_results = requirement_item.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    )
    requirement_link_results = requirement_link.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    ).values(
        'project_id',
        'project_id__project_name',
        'task_id',
        'task_id__task_short_description',
        'organisation_id',
        'organisation_id__organisation_name',
    ).distinct()

    kanban_board_results = kanban_board.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    )

    """
    If the requirement is completed, then we want to send the user to the readonly version. There is no need
    for the user to edit any of the results after the requirement has been completed.
    """
    if requirement_results.requirement_status.requirement_status == "Completed":
        return HttpResponseRedirect(reverse('requirement_readonly', args={requirement_id}))

    # Initialise form
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
        'requirement_results': requirement_results,
        'requirement_link_results': requirement_link_results,
        'requirement_item_results': requirement_item_results,
        'requirement_id': requirement_id,
        'requirement_information_form': requirement_information_form(
            initial=initial,
        ),
        'kanban_board_results': kanban_board_results,
        'permission': permission_results['requirement'],
        'requirement_link_permissions': permission_results['requirement_link'],
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],

    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def requirement_item_information(request, requirement_item_id):
    """
    If a user requires to edit or view the requirement item information, this is the page.
    :param request:
    :param requirement_item_id: The ID for the requirement item
    :return: The requirement item page

    Method
    ~~~~~~
    1. Check permission
    2. Check to see if POST (aka update item) - read method in here
    3. Collect data required
    4. Return page
    """
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST" and permission_results['requirement'] > 1:
        form = requirement_item_form(request.POST)
        if form.is_valid():
            # Save the data
            requirement_item_save = requirement_item.objects.get(requirement_item_id=requirement_item_id)
            requirement_item_save.requirement_item_title=form.cleaned_data['requirement_item_title']
            requirement_item_save.requirement_item_scope=form.cleaned_data['requirement_item_scope']
            requirement_item_save.requirement_item_status=form.cleaned_data['requirement_item_status']
            requirement_item_save.requirement_item_type=form.cleaned_data['requirement_item_type']
            requirement_item_save.change_user=request.user

            requirement_item_save.save()

            # Return the user to the requirement page
            return HttpResponseRedirect(reverse('requirement_information', args={ requirement_item_save.requirement_id_id }))
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
    t = loader.get_template('NearBeach/requirement_item_information.html')

    # context
    c = {
        'requirement_item_id': requirement_item_id,
        'requirement_item_form': requirement_item_form(initial=initial),
        'requirement_item_results': requirement_item_results,
        'permission': permission_results['requirement'],
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],

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

        requirement_item_link_save = requirement_item_link(
            requirement_item_id=requirement_item_id,
            change_user=request.user,
        )

        if destination == "project":
            project_instance = project.objects.get(project_id=location_id)
            requirement_item_link_save.project_id = project_instance
        elif destination == "task":
            task_instance = task.objects.get(task_id=location_id)
            requirement_item_link_save.task_id = task_instance
        elif destination == "organisation":
            organisation_instance = organisation.objects.get(organisation_id=location_id)
            requirement_item_link_save.organisation_id = organisation_instance
        else:
            return HttpResponseBadRequest("You can only choose: project, task, or organisation")

        requirement_item_link_save.save()

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
    project_results = project.objects.filter(
        Q(
            is_deleted="FALSE",
            project_id__in=object_assignment.objects.filter(
                is_deleted="FALSE",
                group_id__in=user_group.objects.filter(
                    is_deleted="FALSE",
                    username=request.user,
                ).values('group_id').distinct(),
            ).values('project_id').distinct(),
        ) and
        Q(
            Q(project_status='New') or
            Q(project_status='Open')
        )
    )

    task_results = task.objects.filter(
        Q(
            is_deleted="FALSE",
            task_id__in=object_assignment.objects.filter(
                is_deleted="FALSE",
                group_id__in=user_group.objects.filter(
                    is_deleted="FALSE",
                    username=request.user,
                ).values('group_id').distinct(),
            ).values('task_id').distinct(),
        ) and
        Q(
            Q(task_status='New') or
            Q(task_status='Open')
        )
    )

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

    item_results = requirement_item.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    )

    requirement_results = requirement.objects.filter(
        requirement_id=requirement_id,
        is_deleted="FALSE",
    )


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
        requirement_link_save = requirement_link(
            requirement=requirement.objects.get(requirement_id=requirement_id),
            change_user=request.user,
        )

        if destination == "project":
            project_instance = project.objects.get(project_id=location_id)
            requirement_link_save.project_id = project_instance
        elif destination == "task":
            task_instance = task.objects.get(task_id=location_id)
            requirement_link_save.task_id = task_instance
        elif destination == "organisation":
            organisation_instance = organisation.objects.get(organisation_id=location_id)
            requirement_link_save.organisation_id = organisation_instance
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
    The linked requirement will only link to requirement the user has access to. Nothing else.
    """
    project_results = project.objects.filter(
        Q(
            is_deleted="FALSE",
            project_id__in=object_assignment.objects.filter(
                group_id__in=user_group.objects.filter(
                    username=request.user,
                    is_deleted="FALSE",
                ).values('group_id'),
                is_deleted="FALSE",
            ).values('project_id').distinct()
        ) and
        Q(
            Q(project_status='New') or
            Q(project_status='Open')
        )
    )

    task_results = task.objects.filter(
        Q(
            is_deleted="FALSE",
            task_id__in=object_assignment.objects.filter(
                group_id__in=user_group.objects.filter(
                    username=request.user,
                    is_deleted="FALSE",
                ).values('group_id'),
                is_deleted="FALSE",
            ).values('task_id').distinct()
        ) and
        Q(
            Q(task_status='New') or
            Q(task_status='Open')
        )
    )

    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_new_link.html')

    # context
    c = {
        'requirement_id': requirement_id,
        'project_results': project_results,
        'task_results': task_results,

    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def requirement_readonly(request,requirement_id):
    permission_results = return_user_permission_level(request, None, 'requirement_link')

    if permission_results['requirement_link'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    #Get Data
    requirement_results = requirement.objects.get(requirement_id=requirement_id)
    requirement_item_results = requirement_item.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    )
    bug_results = bug.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    )

    #Load template
    t = loader.get_template('NearBeach/requirement_information/requirement_readonly.html')

    # context
    c = {
        'requirement_readonly_form': requirement_readonly_form(initial={
            'requirement_scope': requirement_results.requirement_scope,
        }),
        'requirement_results': requirement_results,
        'requirement_item_results': requirement_item_results,
        'requirement_id': requirement_id,
        'bug_results': bug_results,
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))