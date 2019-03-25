from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import  loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from .models import *
from .misc_functions import *
from .user_permissions import return_user_permission_level
from .views import permission_denied




@login_required(login_url='login',redirect_field_name="")
def new_requirement(request,location_id='',destination=''):
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

            """
            If the user is creating a requirement for an opportunity we want to;
            1. Create the connection to the opportunity
            2. Go back to the opportunity
            """
            if destination == "opportunity":
                object_assignment_submit = object_assignment(
                    requirement_id=requirement_save,
                    opportunity_id=opportunity.objects.get(opportunity_id=location_id),
                    change_user=request.user,
                )
                object_assignment_submit.save()

                return HttpResponseRedirect(reverse('opportunity_information', args={location_id}))

            return HttpResponseRedirect(reverse(requirement_information, args={requirement_save.requirement_id}))
        else:
            print(form.errors)

    #Load template
    t = loader.get_template('NearBeach/new_requirement.html')

    # context
    c = {
        'new_requirement_form': new_requirement_form(),
        'location_id': location_id,
        'destination': destination,
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login',redirect_field_name="")
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



@login_required(login_url='login',redirect_field_name="")
def new_requirement_item_link(request,requirement_item_id,location_id="",destination=""):
    """
    This function is designed so users can link requirement items to either tasks/projects. When the function is a simple
    "GET" function it will produce an HTML page with all the possible object links.
    When the method is a "POST", it will create the link and return a blank page. Note that for a post it requires location
    and destination.
    :param request:
    :param requirement_item_id: The requirement item we are looking to link
    :param location_id: The location id of the object we are linking to
    :param destination: The destination object we are linking to
    :return: List of potential links

    Method
    ~~~~~~
    1. Check permissions
    2. Check method - if POST read instructions there
    3. Object a list of all objects that meet the current conditions
        -- Is not deleted
        -- Users can access those objects
        -- Are not currently linked
        -- Object is currently open
    4. Present the data to the user
    """
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        """
        Method
        ~~~~~~
        1. Make sure the location_id and destination are not "" - send error
        2. Create the requirement_link row
        3. Return the JSON result
        4. Profit
        """
        if location_id == "" or destination == "":
            return HttpResponseBadRequest("Sorry - those fields were blank")

        requirement_item_link_submit = requirement_item_link(
            change_user=request.user,
            requirement_item_id=requirement_item_id,
        )
        if destination == "project":
            """
            1. Get the project instance
            2. Save the project instance against the requirement_link
            3. Prepare the object_link and object_description
            """
            project_instance = project.objects.get(project_id=location_id)
            requirement_item_link_submit.project_id = project_instance
            object_link = "Project - " + str(location_id)
            object_description = project_instance.project_name
        elif destination == "task":
            """
            1. Get the task instance
            2. Save the task instance against the requirement_link
            3. Prepare the object_link and object_description
            """
            task_instance = task.objects.get(task_id=location_id)
            requirement_item_link_submit.task_id = task_instance
            object_link = "Task - " + str(location_id)
            object_description = task_instance.task_short_description


        # Save
        requirement_item_link_submit.save()

        # Send back the JSON
        return JsonResponse({
            'location_id': location_id,
            'destination': destination,
            'object_link': object_link,
            'object_description': object_description,
        })


    # Get required data
    project_results = project.objects.filter(
        is_deleted="FALSE",
        project_status__in={'New','Open'},
        project_id__in=object_assignment.objects.filter(
            is_deleted="FALSE",
            group_id__in=user_group.objects.filter(
                is_deleted="FALSE",
                username_id=request.user.id,
            ).values('group_id')
        ).values('project_id')
    ).exclude(
        project_id__in=requirement_item_link.objects.filter(
            is_deleted="FALSE",
            project_id__isnull=False,
            requirement_item_id=requirement_item_id,
        ).values('project_id')
    )

    task_results = task.objects.filter(
        is_deleted="FALSE",
        task_status__in={'New','Open'},
        task_id__in=object_assignment.objects.filter(
            is_deleted="FALSE",
            group_id__in=user_group.objects.filter(
                is_deleted="FALSE",
                username_id=request.user.id,
            ).values('group_id')
        ).values('task_id')
    ).exclude(
        task_id__in=requirement_item_link.objects.filter(
            is_deleted="FALSE",
            task_id__isnull=False,
            requirement_item_id=requirement_item_id,
        ).values('task_id')
    )

    # Get Template
    t = loader.get_template('NearBeach/requirement_information/new_requirement_link.html') #Cheeting here - as we do not need a clone of the same template :)

    # Context
    c = {
        'project_results': project_results,
        'task_results': task_results,
    }

    return HttpResponse(t.render(c,request))



@login_required(login_url='login',redirect_field_name="")
def new_requirement_link(request,requirement_id,location_id="",destination=""):
    """
    This function is designed so users can link requirement to either tasks/projects. When the function is a simple "GET"
    function it will produce an HTML page with all the possible object links.
    When the method is a "POST", it will create the link and return a blank page. Note that for a post it requires location
    and destination.
    :param request:
    :param requirement_id: The requirement we are looking to link
    :param location_id: The location id of the object we are linking to
    :param destination: The destination object we are linking to
    :return: List of potential links

    Method
    ~~~~~~
    1. Check permissions
    2. Check method - if POST read instructions there
    3. Object a list of all objects that meet the current conditions
        -- Is not deleted
        -- Users can access those objects
        -- Are not currently linked
        -- Object is currently open
    4. Present the data to the user
    """
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        """
        Method
        ~~~~~~
        1. Make sure the location_id and destination are not "" - send error
        2. Create the requirement_link row
        3. Return the JSON result
        4. Profit
        """
        if location_id == "" or destination == "":
            return HttpResponseBadRequest("Sorry - those fields were blank")

        requirement_link_submit = requirement_link(
            change_user=request.user,
            requirement_id=requirement_id,
        )
        if destination == "project":
            """
            1. Get the project instance
            2. Save the project instance against the requirement_link
            3. Prepare the object_link and object_description
            """
            project_instance = project.objects.get(project_id=location_id)
            requirement_link_submit.project_id = project_instance
            object_link = "Project - " + str(location_id)
            object_description = project_instance.project_name
        elif destination == "task":
            """
            1. Get the task instance
            2. Save the task instance against the requirement_link
            3. Prepare the object_link and object_description
            """
            task_instance = task.objects.get(task_id=location_id)
            requirement_link_submit.task_id = task_instance
            object_link = "Task - " + str(location_id)
            object_description = task_instance.task_short_description
        elif destination == "opportunity":
            """
            1. Get the opportunity instance
            2. Save the opportunity instance against the requirement_link
            3. Prepare the object_link and object_description
            """
            opportunity_instance = opportunity.objects.get(opportunity_id=location_id)
            requirement_link_submit.opportunity_id = opportunity_instance
            object_link = "Opp - " + str(location_id)
            object_description = opportunity_instance.opportunity_name


        # Save
        requirement_link_submit.save()

        # Send back the JSON
        return JsonResponse({
            'location_id': location_id,
            'destination': destination,
            'object_link': object_link,
            'object_description': object_description,
        })


    # Get required data
    project_results = project.objects.filter(
        is_deleted="FALSE",
        project_status__in={'New','Open'},
        project_id__in=object_assignment.objects.filter(
            is_deleted="FALSE",
            group_id__in=user_group.objects.filter(
                is_deleted="FALSE",
                username_id=request.user.id,
            ).values('group_id')
        ).values('project_id')
    ).exclude(
        project_id__in=requirement_link.objects.filter(
            is_deleted="FALSE",
            project_id__isnull=False,
            requirement_id=requirement_id,
        ).values('project_id')
    )

    task_results = task.objects.filter(
        is_deleted="FALSE",
        task_status__in={'New','Open'},
        task_id__in=object_assignment.objects.filter(
            is_deleted="FALSE",
            group_id__in=user_group.objects.filter(
                is_deleted="FALSE",
                username_id=request.user.id,
            ).values('group_id')
        ).values('task_id')
    ).exclude(
        task_id__in=requirement_link.objects.filter(
            is_deleted="FALSE",
            task_id__isnull=False,
            requirement_id=requirement_id,
        ).values('task_id')
    )

    opportunity_results = opportunity.objects.filter(
        is_deleted="FALSE",
        opportunity_id__in=object_assignment.objects.filter(
            is_deleted="FALSE",
            group_id__in=user_group.objects.filter(
                is_deleted="FALSE",
                username_id=request.user.id,
            ).values('group_id')
        ).values('opportunity_id'),
        opportunity_stage_id__in={
            '1', # prospecting
            '2', # qualification
            '3', # needs analysis
            '4', # valued proposition
            '5', # identify desision makers
            '6', # perception analysis
            '7', # proposal/price quote
            '8', # negotation/review
        }
    ).exclude(
        opportunity_id__in=requirement_link.objects.filter(
            is_deleted="FALSE",
            opportunity_id__isnull=False,
            requirement_id=requirement_id,
        ).values('opportunity_id'),
    )

    # Get Template
    t = loader.get_template('NearBeach/requirement_information/new_requirement_link.html')

    # Context
    c = {
        'project_results': project_results,
        'task_results': task_results,
        'opportunity_results': opportunity_results,
    }

    return HttpResponse(t.render(c,request))


@login_required(login_url='login',redirect_field_name="")
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




@login_required(login_url='login',redirect_field_name="")
def requirement_information(request, requirement_id):
    permission_results = return_user_permission_level(request, None, ['requirement','requirement_link'])

    if permission_results['requirement'] == 0:
        print(permission_results)
        print("Permission denied")
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


    #Get Data
    requirement_results = requirement.objects.get(requirement_id=requirement_id)
    requirement_item_results = requirement_item.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    )


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
        #'requirement_link_results': requirement_link_results,
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
        'requirement_link_permission': permission_results['requirement_link'],
        'requirement_permission': permission_results['requirement'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login',redirect_field_name="")
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
    requirement_item_results = requirement_item.objects.get(
        requirement_item_id=requirement_item_id
    )
    link_results = requirement_item_link.objects.filter(
        is_deleted="FALSE",
        requirement_item_id=requirement_item_id,
    )
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
        'link_results': link_results,
        'permission': permission_results['requirement'],
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],

    }

    return HttpResponse(t.render(c, request))

@login_required(login_url='login')
def requirement_item_link_remove(request,requirement_item_link_id):
    """
    The user wants to remove the requirement link from the requirement. We will do this in this fuction
    :param request:
    :param requirement_link_id: The requirement link to delete
    :return:

    Method
    ~~~~~~
    1. Check method is POST
    2. Check user has permission
    3. Delete the requirement link
    4. Send back blank page
    """
    if request.method == "POST":
        permission_results = return_user_permission_level(request,None,'requirement_link')
        if permission_results['requirement_link'] < 4:
            return HttpResponseRedirect(reverse('permission_denied'))

        requirement_item_link.objects.filter(
            requirement_item_link_id=requirement_item_link_id,
        ).update(
            is_deleted="TRUE"
        )

        #Send back the new list.
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c,request))
    else:
        return HttpResponseBadRequest("Sorry, can only do this in post")


@login_required(login_url='login',redirect_field_name='')
def requirement_link_list(request,requirement_id):
    """
    List all the requirement and requirement item links. This is an AJAX model and will be called when there is a change
    applied on the front end
    :param request:
    :param requirement_id: The requirement id we are looking at
    :return: A list of all requirement and requirement item links

    Method
    ~~~~~~
    1. Get the requirement link results
    2. Get the requirement item link results
    3. Get templtate and context
    4. Render and send to user :)
    """
    permission_results = return_user_permission_level(request, None, 'requirement_link')

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
        'requirement_link_id',
    ).distinct()

    requirement_item_results = requirement_item.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id,
    )

    t = loader.get_template('NearBeach/requirement_information/requirement_link_list.html')

    c = {
        'requirement_item_results': requirement_item_results,
        'requirement_link_results': requirement_link_results,
        'requirement_permission': permission_results['requirement_link']
    }

    return HttpResponse(t.render(c,request))


@login_required(login_url='login')
def requirement_link_remove(request,requirement_link_id):
    """
    The user wants to remove the requirement link from the requirement. We will do this in this fuction
    :param request:
    :param requirement_link_id: The requirement link to delete
    :return:

    Method
    ~~~~~~
    1. Check method is POST
    2. Check user has permission
    3. Delete the requirement link
    4. Send back blank page
    """
    if request.method == "POST":
        permission_results = return_user_permission_level(request,None,'requirement_link')
        if permission_results['requirement_link'] < 4:
            return HttpResponseRedirect(reverse('permission_denied'))

        requirement_link.objects.filter(
            requirement_link_id=requirement_link_id,
        ).update(
            is_deleted="TRUE"
        )

        #Return blank page
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c,request))
    else:
        return HttpResponseBadRequest("Sorry, can only do this in post")


@login_required(login_url='login',redirect_field_name="")
def requirement_readonly(request,requirement_id):
    """
    Requirement readonly is a read only module. This will print out all the requirement information that the user will
    require.
    :param request:
    :param requirement_id: The requirement that the end user wants to look at.
    :return: A read only page for the user
    """
    permission_results = return_user_permission_level(request, None, 'requirement')

    if permission_results['requirement_link'] == 0:
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


