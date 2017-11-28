#Import NearBeach Modules
from .forms import *
from .models import *
from .private_media import *

#Import django Modules
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Q, Min
from django.http import HttpResponse,HttpResponseForbidden, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.urls import reverse

#import python modules
import datetime, json, simplejson, urllib, urllib2

@login_required(login_url='login')
def active_projects(request):
    # Get username_id from User
    current_user = request.user

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
      project.project_id AS "project_id"
    , '' AS "task_id"
    , project.project_name AS "description"
    , project.project_end_date AS "end_date"
    , organisations.organisation_name AS "organisation_name"
    , organisations.organisations_id AS "organisations_id"
    
    
    
    from 
      project left join project_tasks
        on project.project_id = project_tasks.project_id
        and project_tasks.is_deleted = 'FALSE'
    , project_groups
    , user_groups
    , organisations
    
    
    where 1 = 1
    and project.project_status IN ('New','Open')
    and project.project_status IN ('New','Open')
    and project.project_id = project_groups.project_id_id
    and project_groups.groups_id_id = user_groups.group_id_id
    and user_groups.username_id = %s
    and project.organisations_id_id=organisations.organisations_id
    
    
    UNION
    
    select 
      project_tasks.project_id AS `Project ID`
    , tasks.tasks_id AS `Task ID`
    , tasks.task_short_description AS `Description`
    , tasks.task_end_date AS `End Date` 
    , organisations.organisation_name AS "organisation_name"
    , organisations.organisations_id AS "organisations_id"
    
    from 
      tasks left join project_tasks
        on tasks.tasks_id = project_tasks.task_id 
        and project_tasks.is_deleted = "FALSE"
    , tasks_groups
    , user_groups
    , organisations
    
    
    where 1 = 1
    and tasks.task_status in ('New','Open')
    and tasks.tasks_id = tasks_groups.tasks_id_id
    and tasks_groups.groups_id_id = user_groups.group_id_id
    and user_groups.username_id = %s
    and tasks.organisations_id_id=organisations.organisations_id
        
    UNION
    
    select 
     project_tasks.project_id AS `Project ID`
    , tasks.tasks_id AS `Task ID`
    , tasks.task_short_description AS `Description`
    , tasks.task_end_date AS `End Date` 
    , organisations.organisation_name AS "organisation_name"
    , organisations.organisations_id AS "organisations_id"
    
    from 
      tasks left join project_tasks
        on tasks.tasks_id = project_tasks.task_id 
        and project_tasks.is_deleted = "FALSE"
    , organisations
    
    
    
    where 1 = 1
    and tasks.task_status in ('New','Open')
    and tasks.task_assigned_to_id = %s
    and tasks.organisations_id_id=organisations.organisations_id
    """, [current_user.id, current_user.id, current_user.id])

    active_projects_results = namedtuplefetchall(cursor)

    # Load the template
    t = loader.get_template('NearBeach/active_projects.html')

    # context
    c = {
        'active_projects_results': active_projects_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def assign_customer_project_task(request, customer_id):
    # Get username_id from User
    current_user = request.user

    if request.POST:

        assign_projects = request.POST.getlist('project_checkbox')
        assign_tasks = request.POST.getlist('task_checkbox')

        # Instance
        customer_instance = customers.objects.get(customer_id=customer_id)

        """
		We will now assign these projects and tasks in bulk to the customer
		"""
        for row in assign_projects:
            project_instance = project.objects.get(project_id=row)

            # Project customers
            assign_save = project_customers(
                project_id=project_instance,
                customer_id=customer_instance,
                change_user=request.user,
                # Customer description will have to be programmed in at a later date
            )
            assign_save.save()

        for row in assign_tasks:
            task_instance = tasks.objects.get(tasks_id=row)

            assign_save = tasks_customers(
                tasks_id=task_instance,
                customer_id=customer_instance,
                change_user=request.user,
            )
            assign_save.save()

        # Now return to the customer's information
        return HttpResponseRedirect(reverse('customer_information', args={customer_id}))

    # Get Data
    customer_results = customers.objects.get(customer_id=customer_id)

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
		SELECT DISTINCT
		  project.*
		FROM
		  user_groups
		, project_groups
		, project
		WHERE 1=1
		--USER_GROUPS CONDITIONS
		AND user_groups.username_id = %s --INSERT FILTER HERE!
		-- JOINS --
		AND user_groups.group_id_id = project_groups.groups_id_id
		AND project_groups.project_id_id = project.project_id
		-- END JOINS --	
	""", [current_user.id])
    project_results = namedtuplefetchall(cursor)

    cursor.execute("""
		SELECT DISTINCT
		tasks.*
		FROM
		user_groups
		, tasks_groups
		, tasks
		WHERE 1=1
		--USER_GROUPS CONDITIONS
		AND user_groups.username_id = %s
		-- JOINS --
		AND user_groups.group_id_id = tasks_groups.groups_id_id
		AND tasks_groups.tasks_id_id=tasks.tasks_id
		-- END JOINS --
	""", [current_user.id])
    task_results = namedtuplefetchall(cursor)

    # Load the template
    t = loader.get_template('NearBeach/assign_customer_project_task.html')

    # context
    c = {
        'project_results': project_results,
        'task_results': task_results,
        'customer_results': customer_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def associate(request, project_id, task_id, project_or_task):
    # Submit the data
    submit_result = project_tasks(
        project_id_id=project_id,
        task_id_id=task_id,
        change_user=request.user,
    )
    submit_result.save()

    # Once we assign them together, we go back to the original
    if project_or_task == "P":
        return HttpResponseRedirect(reverse('project_information', args={project_id}))
    else:
        return HttpResponseRedirect(reverse('task_information', args={task_id}))


@login_required(login_url='login')
def associated_projects(request, task_id):
    """
	We want the ability for the user to assign any project to the current
	task that their group owns. The user will have the ability to
	check to see if they want only new or open, or if they would like
	to see closed tasks too.
	"""
    search_projects = search_projects_form()

    # POST
    if request.method == "POST":
        # TO DO! EXTRACT POST AND FILTER RESULTS!!!
        projects_results = project.objects.filter()
    else:
        projects_results = project.objects.filter()

    # Load the template
    t = loader.get_template('NearBeach/associated_projects.html')

    # context
    c = {
        'projects_results': projects_results,
        'search_projects': search_projects,
        'task_id': task_id,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def associated_tasks(request, project_id):
    """
	We want the ability for the user to assign any task to the current
	project that their group owns. The user will have the ability to
	check to see if they want only new or open, or if they would like
	to see closed tasks too.
	"""
    search_tasks = search_tasks_form()

    # POST
    if request.method == "POST":
        # TO DO! EXTRACT POST AND FILTER RESULTS!!!
        tasks_results = tasks.objects.filter()
    else:
        tasks_results = tasks.objects.filter()

    # Load the template
    t = loader.get_template('NearBeach/associated_tasks.html')

    # context
    c = {
        'tasks_results': tasks_results,
        'search_tasks': search_tasks,
        'project_id': project_id,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def campus_information(request, campus_information):
    # Obtain data (before POST if statement as it is used insude)
    campus_results = organisations_campus.objects.get(pk=campus_information)

    # If instance is in POST
    if request.method == "POST":
        # Other save button must have been pressed
        form = campus_information_form(request.POST)
        if form.is_valid():
            # SQL instance
            campus_region_instance = list_of_countries_regions.objects.get(
                region_id=int(request.POST.get('campus_region_id')))
            campus_country_instance = list_of_countries.objects.get(country_id=request.POST.get('campus_country_id'))

            # Save all the data
            campus_results.campus_nickname = form.cleaned_data['campus_nickname']
            campus_results.campus_phone = form.cleaned_data['campus_phone']
            campus_results.campus_fax = form.cleaned_data['campus_fax']
            campus_results.campus_address1 = form.cleaned_data['campus_address1']
            campus_results.campus_address2 = form.cleaned_data['campus_address2']
            campus_results.campus_address3 = form.cleaned_data['campus_address3']
            campus_results.campus_suburb = form.cleaned_data['campus_suburb']
            campus_results.campus_region_id = campus_region_instance
            campus_results.campus_country_id = campus_country_instance
            campus_results.change_user=request.user

            campus_results.save()

        if 'add_customer_submit' in request.POST:
            # Obtain the ID of the customer
            customer_results = int(request.POST.get("add_customer_select"))

            # Get the SQL Instances
            customer_instance = customers.objects.get(customer_id=customer_results)
            campus_instances = organisations_campus.objects.get(id=campus_information)


            # Save the new campus
            submit_campus = customers_campus(
                customer_id=customer_instance,
                campus_id=campus_instances,
                customer_phone='',
                customer_fax='',
                change_user=request.user,
            )
            submit_campus.save()

            # Go to the form.
            return HttpResponseRedirect(reverse('customers_campus_information', args={submit_campus.id, 'CAMP'}))

    # Get Data
    customer_campus_results = customers_campus.objects.filter(
        campus_id=campus_information,
        is_deleted='FALSE',
    )
    add_customers_results = customers.objects.filter(organisations_id=campus_results.organisations_id)
    countries_regions_results = list_of_countries_regions.objects.all()
    countries_results = list_of_countries.objects.all()

    # Load the template
    t = loader.get_template('NearBeach/campus_information.html')

    # context
    c = {
        'campus_results': campus_results,
        'campus_information_form': campus_information_form(instance=campus_results),
        'customer_campus_results': customer_campus_results,
        'add_customers_results': add_customers_results,
        'countries_regions_results': countries_regions_results,
        'countries_results': countries_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def customers_campus_information(request, customer_campus_id, customer_or_org):
    """
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # IF method is post
    if request.method == "POST":
        form = customer_campus_form(request.POST)
        if form.is_valid():
            # Save the data
            save_data = customers_campus.objects.get(id=customer_campus_id)

            save_data.customer_phone = form.cleaned_data['customer_phone']
            save_data.customer_fax = form.cleaned_data['customer_fax']
            save_data.change_user=request.user

            save_data.save()

            """
			Now direct the user back to where they were from. The default
			will be the customer information
			"""
            if customer_or_org == "CAMP":
                return HttpResponseRedirect(reverse('campus_information', args={save_data.campus_id.id}))
            else:
                return HttpResponseRedirect(reverse('customer_information', args={save_data.customer_id.customer_id}))

    # Get Data
    customer_campus_results = customers_campus.objects.get(id=customer_campus_id)

    # Setup the initial results
    initial = {
        'customer_phone': customer_campus_results.customer_phone,
        'customer_fax': customer_campus_results.customer_fax,
    }

    # Load template
    t = loader.get_template('NearBeach/customer_campus.html')

    # context
    c = {
        'customer_campus_form': customer_campus_form(initial=initial),
        'customer_campus_results': customer_campus_results,
        'customer_campus_id': customer_campus_id,
        'customer_or_org': customer_or_org,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def customer_information(request, customer_id):
    """
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == "POST":
        # Save everything!
        form = customer_information_form(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            # Save the data
            save_data = customers.objects.get(customer_id=customer_id)

            save_data.customer_title = form.cleaned_data['customer_title']
            save_data.customer_first_name = form.cleaned_data['customer_first_name']
            save_data.customer_last_name = form.cleaned_data['customer_last_name']
            save_data.customer_email = form.cleaned_data['customer_email']
            save_data.change_user=request.user

            # Check to see if the picture has been updated
            update_profile_picture = request.FILES.get('update_profile_picture')
            if not update_profile_picture == None:
                save_data.customer_profile_picture = update_profile_picture

            save_data.save()

            """
			If the user has written something in the contact section, we want to save it
			"""
            contact_history_notes = form.cleaned_data['contact_history']
            print(contact_history_notes)

            if not contact_history_notes == '':
                # Lets save some contact history
                contact_type = form.cleaned_data['contact_type']

                contact_date = time_combined(
                    int(form.cleaned_data['start_date_year']),
                    int(form.cleaned_data['start_date_month']),
                    int(form.cleaned_data['start_date_day']),
                    int(form.cleaned_data['start_date_hour']),
                    int(form.cleaned_data['start_date_minute']),
                    form.cleaned_data['start_date_meridiems']
                )

                # documents
                contact_attachment = request.FILES.get('contact_attachment')
                if contact_attachment:
                    documents_save = documents(
                        document_description=contact_attachment,
                        document=contact_attachment,
                        change_user=request.user,
                    )
                    documents_save.save()

                    #Add to document permissions
                    document_permissions_save = document_permissions(
                        document_key=documents_save,
                        customer_id=customers.objects.get(customer_id=customer_id),
                        change_user=request.user,
                    )
                    document_permissions_save.save()

                submit_history = contact_history(
                    organisations_id=save_data.organisations_id,
                    customer_id=save_data,
                    contact_type=contact_type,
                    contact_date=contact_date,
                    contact_history=contact_history_notes,
                    user_id=current_user,
                    change_user=request.user,
                    #document_key=documents_save,
                )
                if contact_attachment:
                    submit_history.document_key=documents_save
                submit_history.save()

            """
			Document Uploads
			"""
            document = request.FILES.get('document')
            if not document == None:
                document_save = documents(
                    document_description=form.cleaned_data['document_description'],
                    document=form.cleaned_data['document'],
                    change_user=request.user,
                )
                document_save.save()

                document_permissions_save = document_permissions(
                    document_key=document_save,
                    organisations_id=save_data.organisations_id,
                    customer_id=save_data,
                    change_user=request.user,
                )
                document_permissions_save.save()

            # If we are adding a new campus
            if 'add_campus_submit' in request.POST:
                # Obtain the id of the campus_id
                campus_id_results = request.POST.get("add_campus_select")

                # Get the SQL Instances
                customer_instance = customers.objects.get(customer_id=customer_id)
                campus_instances = organisations_campus.objects.get(id=campus_id_results)

                # Save the new campus
                submit_campus = customers_campus(
                    customer_id=customer_instance,
                    campus_id=campus_instances,
                    customer_phone='',
                    customer_fax='',
                    change_user=request.user,
                )
                submit_campus.save()

                # Go to the form.
                return HttpResponseRedirect(reverse('customers_campus_information', args={submit_campus.id, 'CUST'}))
        else:
            print(form.errors)

    # Get the instance
    customer_results = customers.objects.get(pk=customer_id)
    add_campus_results = organisations_campus.objects.filter(organisations_id=customer_results.organisations_id)
    customer_contact_history = contact_history.objects.filter(customer_id=customer_id)
    customer_document_results = document_permissions.objects.filter(customer_id=customer_id)
    organisation_document_results = document_permissions.objects.filter(
        organisations_id=customer_results.organisations_id,
        customer_id__isnull=True
    )

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
		SELECT DISTINCT
		project.*
		FROM
		project_customers
		, project
		WHERE 1=1
		AND project_customers.is_deleted='FALSE'
		AND project_customers.project_id_id=project.project_id
		AND project_customers.project_customers_id = %s
	""", [customer_id])
    project_results = namedtuplefetchall(cursor)

    cursor.execute("""
		SELECT DISTINCT
		tasks.*
		FROM
		tasks_customers
		, tasks
		WHERE 1=1
		AND tasks_customers.is_deleted='FALSE'
		AND tasks_customers.tasks_id_id=tasks.tasks_id
		AND tasks_customers.tasks_customers_id = %s
		""", [customer_id])
    task_results = namedtuplefetchall(cursor)

    # The campus the customer is associated to
    """
    We need to limit the amount of opportunities to those that the user has access to.
    """
    user_groups_results = user_groups.objects.filter(username=request.user)

    opportunity_permissions_results = opportunity_permissions.objects.filter(
        Q(
            Q(assigned_user=request.user)  # User has permission
            | Q(groups_id__in=user_groups_results.values('group_id'))  # User's groups have permission
            | Q(all_users='TRUE')  # All users have access
        )
    )
    opportunity_results = opportunity.objects.filter(
        customer_id=customer_id,
        opportunity_id__in=opportunity_permissions_results.values('opportunity_id')
    )
    campus_results = customers_campus.objects.filter(
        customer_id=customer_id,
        is_deleted='FALSE',
    )


    try:
        profile_picture = customer_results.customer_profile_picture.url
    except:
        profile_picture = ''

    # Date required to initiate date
    today = datetime.datetime.now()

    """
    We need to do some basic formulations with the hour and and minutes.
    For the hour we need to find all those who are in the PM and
    change both the hour and meridiem accordingly.
    For the minute, we have to create it in 5 minute blocks.
    """
    hour = today.hour
    minute = int(5 * round(today.minute / 5.0))
    meridiems = 'AM'

    if hour > 12:
        hour = hour - 12
        meridiems = 'PM'
    elif hour == 0:
        hour = 12

    # load template
    t = loader.get_template('NearBeach/customer_information.html')

    # context
    c = {
        'customer_information_form': customer_information_form(
            instance=customer_results,
            initial={
                'start_date_year': today.year,
                'start_date_month': today.month,
                'start_date_day': today.day,
                'start_date_hour': hour,
                'start_date_minute': minute,
                'start_date_meridiems': meridiems,
            }),
        'campus_results': campus_results,
        'add_campus_results': add_campus_results,
        'customer_results': customer_results,
        'customer_contact_history': customer_contact_history,
        'media_url': settings.MEDIA_URL,
        'profile_picture': profile_picture,
        'customer_document_results': customer_document_results,
        'organisation_document_results': organisation_document_results,
        'project_results': project_results,
        'task_results': task_results,
        'opportunity_results': opportunity_results,
        'PRIVATE_MEDIA_URL': settings.PRIVATE_MEDIA_URL,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def dashboard(request):
    # Load the template
    t = loader.get_template('NearBeach/dashboard.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))

@login_required(login_url='login')
def dashboard_active_projects(request):
    #Get username id from User
    current_user = request.user

    #Get Data
    assigned_users_results = assigned_users.objects.filter(
        is_deleted='FALSE',
        user_id=current_user,
    )

    # Load the template
    t = loader.get_template('NearBeach/dashboard_widgets/active_projects.html')

    # context
    c = {
        'assigned_users_results': assigned_users_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def dashboard_active_tasks(request):
    # Get username id from User
    current_user = request.user

    # Get Data

    # Load the template
    t = loader.get_template('NearBeach/dashboard_widgets/active_tasks.html')

    # context
    c = {
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def dashboard_group_active_projects(request):
    #Data
    # Get username_id from User
    current_user = request.user

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
      project.project_id AS "project_id"
    , '' AS "task_id"
    , project.project_name AS "description"
    , project.project_end_date AS "end_date"
    , organisations.organisation_name AS "organisation_name"
    , organisations.organisations_id AS "organisations_id"



    from 
      project left join project_tasks
        on project.project_id = project_tasks.project_id
        and project_tasks.is_deleted = 'FALSE'
    , project_groups
    , user_groups
    , organisations


    where 1 = 1
    and project.project_status IN ('New','Open')
    and project.is_deleted = 'FALSE'
    and project.project_id = project_groups.project_id_id
    and project_groups.groups_id_id = user_groups.group_id_id
    and user_groups.username_id = %s
    and project.organisations_id_id=organisations.organisations_id
    """, [current_user.id])

    active_projects_results = namedtuplefetchall(cursor)

    # Load the template
    t = loader.get_template('NearBeach/dashboard_widgets/group_active_projects.html')

    # context
    c = {
        'active_projects_results': active_projects_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def dashboard_group_active_tasks(request):
    # Get username_id from User
    current_user = request.user

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
       SELECT DISTINCT
          tasks.tasks_id
        , tasks.task_short_description
        , tasks.task_end_date
        , organisations.organisation_name
        , organisations.organisations_id
        FROM 
          tasks
        , organisations
        , tasks_groups
        , user_groups
        
        WHERE 1=1
        
        AND tasks.is_deleted = 'FALSE'
        AND tasks.task_status IN ('New','Open')
        AND tasks.organisations_id_id=organisations.organisations_id
        AND tasks.tasks_id = tasks_groups.tasks_id_id
        AND tasks_groups.groups_id_id = user_groups.group_id_id
        AND user_groups.username_id = %s
       """, [ current_user.id])

    active_tasks_results = namedtuplefetchall(cursor)

    # Load the template
    t = loader.get_template('NearBeach/dashboard_widgets/group_active_tasks.html')

    # context
    c = {
        'active_tasks_results': active_tasks_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def dashboard_group_opportunities(request):
    # Get username_id from User
    current_user = request.user

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT
        opportunities.opportunity_id
        , opportunities.opportunity_name
        , organisations.organisations_id
        , organisations.organisation_name
        , customers.customer_id
        , customers.customer_first_name
        , customers.customer_last_name
        , list_of_opportunity_stage.opportunity_stage_description
        , opportunities.opportunity_expected_close_date
        
        
        FROM 
        opportunity_permission LEFT JOIN user_groups
        ON opportunity_permission.assigned_user_id = user_groups.username_id
        , opportunities JOIN organisations
        ON opportunities.organisations_id_id = organisations.organisations_id
        LEFT JOIN customers
        ON opportunities.customer_id_id = customers.customer_id
        JOIN list_of_opportunity_stage
        ON opportunities.opportunity_stage_id_id = list_of_opportunity_stage.opportunity_stage_id
        WHERE 1=1
        AND opportunity_permission.opportunity_id_id = opportunities.opportunity_id
        AND list_of_opportunity_stage.opportunity_stage_description NOT LIKE '%%Close%%'
        AND (
        --Assigned user
        opportunity_permission.assigned_user_id = %s
        --Group ID
        OR (
        user_groups.username_id = %s
        AND user_groups.is_deleted = 'FALSE'
        )	
        --All users
        OR opportunity_permission.all_users = 'TRUE'
        )
        AND opportunity_permission.is_deleted = 'FALSE'
    """,[current_user.id,current_user.id])
    active_group_opportunities = namedtuplefetchall(cursor)

    # Load the template
    t = loader.get_template('NearBeach/dashboard_widgets/group_opportunities.html')

    # context
    c = {
        'active_group_opportunities': active_group_opportunities,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def dashboard_opportunities(request):
    # Get username_id from User
    current_user = request.user

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT
        opportunities.opportunity_id
        , opportunities.opportunity_name
        , organisations.organisations_id
        , organisations.organisation_name
        , customers.customer_id
        , customers.customer_first_name
        , customers.customer_last_name
        , list_of_opportunity_stage.opportunity_stage_description
        , opportunities.opportunity_expected_close_date


        FROM 
        opportunity_permission LEFT JOIN user_groups
        ON opportunity_permission.assigned_user_id = user_groups.username_id
        , opportunities JOIN organisations
        ON opportunities.organisations_id_id = organisations.organisations_id
        LEFT JOIN customers
        ON opportunities.customer_id_id = customers.customer_id
        JOIN list_of_opportunity_stage
        ON opportunities.opportunity_stage_id_id = list_of_opportunity_stage.opportunity_stage_id
        WHERE 1=1
        AND opportunity_permission.opportunity_id_id = opportunities.opportunity_id
        AND list_of_opportunity_stage.opportunity_stage_description NOT LIKE '%%Close%%'
        AND opportunity_permission.assigned_user_id = %s
    """, [current_user.id])
    active_opportunities = namedtuplefetchall(cursor)

    # Load the template
    t = loader.get_template('NearBeach/dashboard_widgets/opportunities.html')

    # context
    c = {
        'active_opportunities': active_opportunities,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def delete_campus_contact(request, customers_campus_id, cust_or_camp):
    """
    So... I will need to add in security to define IF a user can do this action
    """
    save_customers_campus = customers_campus.objects.get(pk=customers_campus_id)
    save_customers_campus.is_deleted = "TRUE"
    save_customers_campus.change_user = request.user
    save_customers_campus.save()

    print(save_customers_campus.campus_id.id)
    if cust_or_camp=="CAMP":
        return HttpResponseRedirect(reverse('campus_information', args={save_customers_campus.campus_id.id}))
    else:
        return HttpResponseRedirect(reverse('customer_information', args={save_customers_campus.customer_id.customer_id}))


@login_required(login_url='login')
def delete_cost(request, cost_id, location_id, project_or_task):
    # Delete the cost
    cost_save = costs.objects.get(pk=cost_id)
    cost_save.is_deleted = "TRUE"
    cost_save.change_user=request.user
    cost_save.save()

    # Once we assign them together, we go back to the original
    if project_or_task == "P":
        return HttpResponseRedirect(reverse('project_information', args={location_id}))
    else:
        return HttpResponseRedirect(reverse('task_information', args={location_id}))


@login_required(login_url='login')
def delete_opportunity_permission(request, opportunity_id, groups_id, assigned_user):
    """
    Method
    ~~~~~~
    1.) If groups_id not empty, remove the permissions
    2.) If user_id not empty, remove the permissions
    3.) If the count of active permissions for the opportunity is 0, add the permission "ALL USERS"
    """
    opportunity_instance = opportunity.objects.get(opportunity_id=opportunity_id)

    if (not groups_id == 0):
        # Will remove the ALL USERS permissions now that we have limited the permissions
        opportunity_permissions.objects.filter(
            opportunity_id=opportunity_instance,
            groups_id=groups_id,
            is_deleted='FALSE'
        ).update(is_deleted='TRUE')

    if (not assigned_user == 0):
        # Will remove the ALL USERS permissions now that we have limited the permissions
        opportunity_permissions.objects.filter(
            opportunity_id=opportunity_instance,
            assigned_user=assigned_user,
            is_deleted='FALSE'
        ).update(is_deleted='TRUE')

    if (opportunity_permissions.objects.filter(opportunity_id=opportunity_id,is_deleted='FALSE').count() == 0):
        #Add all users
        permission_save=opportunity_permissions(
            opportunity_id=opportunity_instance,
            all_users='TRUE',
            user_id=request.user,
            change_user=request.user,
        )
        permission_save.save()
    return HttpResponseRedirect(reverse('opportunity_information', args={opportunity_id}))

#MyModel.objects.filter(pk=some_value).update(field1='some value')

@login_required(login_url='login')
def index(request):
    """
	The index page determines if a particular user has logged in. It will
	follow the following steps
	
	Method
	~~~~~~
	1.) If there is a user logged in, if not, send them to login
	2.) Find out if this user should be in the system, if not send them to
		invalid view
	3.) If survived this far the user will be sent to "Active Projects"
	"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('active_projects'))

    # Default
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def is_admin(request):
    """
	We will determine if the user is an administrator. Then we
	will return
	"""
    current_user = request.user
    results = user_groups.objects.filter(username_id=current_user.id).aggregate(Min('user_group_permission'))

    # ADMIN
    if results.values()[0] == 1:
        request.session['IS_ADMIN'] = 'TRUE'
    else:
        request.session['IS_ADMIN'] = 'FALSE'

    # Group Admin
    if results.values()[0] == 2:
        request.session['IS_GROUP_ADMIN'] = 'TRUE'
    else:
        request.session['IS_GROUP_ADMIN'] = 'FALSE'

    return


def login(request):
    """
	For some reason I can not use the varable "login_form" here as it is already being used.
	Instead I will use the work form.
	
	The form is declared at the start and filled with either the POST data OR nothing. If this
	process is called in POST, then the form will be checked and if it passes the checks, the
	user will be logged in.
	
	If the form is not in POST (aka GET) OR fails the checks, then it will create the form with
	the relevant errors.
	"""
    form = login_form(request.POST or None)

    # reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KEY = ''
    if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY') and hasattr(settings, 'RECAPTCHA_PRIVATE_KEY'):
        RECAPTCHA_PUBLIC_KEY = settings.RECAPTCHA_PUBLIC_KEY
        RECAPTCHA_PRIVATE_KEY = settings.RECAPTCHA_PRIVATE_KEY

    # POST
    if request.method == 'POST':
        if form.is_valid():
            """
			Method
			~~~~~~
			1.) Collect the variables
			2.) IF reCAPTCHA is enabled, then process login through that
				statement
				IF it is not, proceed to verify login
			3.) If it all fails, it will just go back to the login screen.
			"""
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY') and hasattr(settings, 'RECAPTCHA_PRIVATE_KEY'):
                """
				As the Google documentation states. I have to send the request back to
				the given URL. It gives back a JSON object, which will contain the
				success results.
				
				Method
				~~~~~~
				1.) Collect the variables
				2.) With the data - encode the variables into URL format
				3.) Send the request to the given URL
				4.) The response will open and store the response from GOOGLE
				5.) The results will contain the JSON Object
				"""
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': RECAPTCHA_PRIVATE_KEY,
                    'response': recaptcha_response
                }
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data)
                response = urllib2.urlopen(req)
                result = json.load(response)

                # Check to see if the user is a robot. Success = human
                if result['success']:
                    user = auth.authenticate(username=username, password=password)
                    auth.login(request, user)

                    is_admin(request)


            else:
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)

                is_admin(request)

            # Just double checking. :)
            if request.user.is_authenticated:
				"""				
				The user is now authenticated. We now want to create the cookies required
				for this session's information. Such information would be
				1.) Is the user an admin?
				2.) What are their groups and their group permissions
				
				This information will be used to help quickly tell the server information
				about the user without having to constantly look it up.
				"""

				#from django.core import serializers
				#data = serializers.serialize("xml", SomeModel.objects.all())
				request.session['user_group_results'] = serializers.serialize('json',user_groups.objects.filter(
					username=request.user,
					is_deleted='FALSE'
				))

				return HttpResponseRedirect(reverse('active_projects'))
        else:
            print(form.errors)

    # load template
    t = loader.get_template('NearBeach/login.html')

    # context
    c = {
        'login_form': form,
        'RECAPTCHA_PUBLIC_KEY': RECAPTCHA_PUBLIC_KEY,
    }

    return HttpResponse(t.render(c, request))


def logout(request):
    # log the user out and go to login page
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def new_campus(request, organisations_id):
    """
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        form = new_campus_form(request.POST)
        if form.is_valid():
            # Get instances
            region_instance = list_of_countries_regions.objects.get(region_id=request.POST.get('campus_region_id'))
            country_instance = list_of_countries.objects.get(country_id=request.POST.get('campus_country_id'))

            campus_nickname = form.cleaned_data['campus_nickname']
            campus_phone = form.cleaned_data['campus_phone']
            campus_fax = form.cleaned_data['campus_fax']
            campus_address1 = form.cleaned_data['campus_address1']
            campus_address2 = form.cleaned_data['campus_address2']
            campus_address3 = form.cleaned_data['campus_address3']
            campus_suburb = form.cleaned_data['campus_suburb']
            campus_region_id = region_instance
            campus_country_id = country_instance

            organisation = organisations.objects.get(organisations_id=organisations_id)

            # BUG - some simple validation should go here?

            # Submitting the data
            submit_form = organisations_campus(
                organisations_id=organisation,
                campus_nickname=campus_nickname,
                campus_phone=campus_phone,
                campus_fax=campus_fax,
                campus_address1=campus_address1,
                campus_address2=campus_address2,
                campus_address3=campus_address3,
                campus_suburb=campus_suburb,
                campus_region_id=campus_region_id,
                campus_country_id=campus_country_id,
                change_user = request.user,
            )
            submit_form.save()

            return HttpResponseRedirect(reverse(organisation_information, args={organisations_id}))
        else:
            print form.errors
            return HttpResponseRedirect(reverse(new_campus, args={organisations_id}))

    # SQL
    countries_results = list_of_countries.objects.all().order_by('country_name')
    countries_regions_results = list_of_countries_regions.objects.all().order_by('region_name')

    # load template
    t = loader.get_template('NearBeach/new_campus.html')

    # context
    c = {
        'organisations_id': organisations_id,
        'new_campus_form': new_campus_form(),
        'countries_results': countries_results,
        'countries_regions_results': countries_regions_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def new_customer(request, organisations_id):
    """
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        form = new_customer_form(request.POST)
        if form.is_valid():
            customer_title = form.cleaned_data['customer_title']
            customer_first_name = form.cleaned_data['customer_first_name']
            customer_last_name = form.cleaned_data['customer_last_name']
            customer_email = form.cleaned_data['customer_email']


            organisations_id = form.cleaned_data['organisations_id']

            submit_form = customers(
                customer_title=customer_title,
                customer_first_name=customer_first_name,
                customer_last_name=customer_last_name,
                customer_email=customer_email,
                organisations_id=organisations_id,
                change_user=request.user,
            )

            # BUG - no validation process to see if there exists a customer already :(
            submit_form.save()

            return HttpResponseRedirect(reverse(customer_information, args={submit_form.customer_id}))
    else:
        form = new_customer_form()

    # load template
    t = loader.get_template('NearBeach/new_customer.html')

    initial = {
        'organisations_id': organisations_id,
    }

    # context
    c = {
        'new_customer_form': new_customer_form(initial=initial),
        'organisations_id': organisations_id,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def new_opportunity(request, organisation_id='', customer_id=''):
    # POST or None
    if request.method == 'POST':
        form = new_opportunity_form(request.POST)
        if form.is_valid():
            current_user = request.user
            # Start saving the data in the form
            opportunity_name = form.cleaned_data['opportunity_name']
            opportunity_description = form.cleaned_data['opportunity_description']
            organisations_id = form.cleaned_data['organisations_id']
            currency_id = form.cleaned_data['currency_id']
            opportunity_amount = form.cleaned_data['opportunity_amount']
            amount_type_id = form.cleaned_data['amount_type_id']
            opportunity_success_probability = form.cleaned_data['opportunity_success_probability']
            lead_source_id = form.cleaned_data['lead_source_id']
            next_step_description = form.cleaned_data['next_step_description']
            select_groups = form.cleaned_data['select_groups']
            select_users = form.cleaned_data['select_users']



            """
			Some dropdown boxes will need to have instances made from the values.
			"""
            stage_of_opportunity_instance = list_of_opportunity_stage.objects.get(
                opportunity_stage_id=request.POST.get('opportunity_stage'))

            opportunity_end_date = time_combined(
                int(form.cleaned_data['finish_date_year']),
                int(form.cleaned_data['finish_date_month']),
                int(form.cleaned_data['finish_date_day']),
                int(form.cleaned_data['finish_date_hour']),
                int(form.cleaned_data['finish_date_minute']),
                form.cleaned_data['finish_date_meridiems']
            )

            """
			SAVE THE DATA
			"""
            submit_opportunity = opportunity(
                opportunity_name=opportunity_name,
                opportunity_description=opportunity_description,
                organisations_id=organisations_id,
                currency_id=currency_id,
                opportunity_amount=opportunity_amount,
                amount_type_id=amount_type_id,
                opportunity_success_probability=opportunity_success_probability,
                lead_source_id=lead_source_id,
                opportunity_expected_close_date=opportunity_end_date,
                opportunity_stage_id=stage_of_opportunity_instance,
                user_id=current_user,
                change_user=request.user,
            )
            if not request.POST.get('customer_id') == '':
                customer_instace = customers.objects.get(customer_id=int(request.POST.get('customer_id')))
                submit_opportunity.customer_id = customer_instace
            else:
                submit_opportunity.customer_id = None

            # submit_opportunity.save()

            submit_opportunity.save()
            opportunity_instance = opportunity.objects.get(opportunity_id=submit_opportunity.opportunity_id)

            """
			If the next step has words in it, save it to the database
			"""
            if not next_step_description == "":
                # Save the next step description
                submit_next_step = opportunity_next_step(
                    opportunity_id=opportunity_instance,
                    next_step_description=next_step_description,
                    user_id=current_user,
                    change_user=request.user,
                )
                submit_next_step.save()

            """
            Permissions granting
            """
            give_all_access = True

            if (select_groups):
                give_all_access = False


                for row in select_groups:
                    group_instance = groups.objects.get(group_name=row)
                    permission_save = opportunity_permissions(
                        opportunity_id=opportunity_instance,
                        groups_id=group_instance,
                        user_id=current_user,
                        change_user=request.user,
                    )
                    permission_save.save()

            if (select_users):
                give_all_access = False

                for row in select_users:
                    assigned_user_instance = auth.models.User.objects.get(username=row)
                    permission_save = opportunity_permissions(
                        opportunity_id=opportunity_instance,
                        assigned_user=assigned_user_instance,
                        user_id=current_user,
                        change_user=request.user,
                    )
                    permission_save.save()

            if (give_all_access):
                permission_save = opportunity_permissions(
                    opportunity_id=opportunity_instance,
                    all_users='TRUE',
                    user_id=current_user,
                    change_user=request.user,
                )
                permission_save.save()

            """
			Now we go to the opportunity information page so the user can start
			inputting the require information (like documents), and tasks.
			"""
            return HttpResponseRedirect(reverse(opportunity_information, args={submit_opportunity.opportunity_id}))
        else:
            print(form.errors)


    # load template
    t = loader.get_template('NearBeach/new_opportunity.html')

    # DATA
    customer_results = customers.objects.all()
    opportunity_stage_results = list_of_opportunity_stage.objects.filter(is_deleted="FALSE")


    # Setup dates for initalising
    next_week = datetime.datetime.now() + datetime.timedelta(days=31)

    """
	We need to do some basic formulations with the hour and and minutes.
	For the hour we need to find all those who are in the PM and
	change both the hour and meridiem accordingly.
	For the minute, we have to create it in 5 minute blocks.
	"""
    hour = next_week.hour
    minute = int(5 * round(next_week.minute / 5.0))
    meridiems = 'AM'

    if hour > 12:
        hour = hour - 12
        meridiems = 'PM'
    elif hour == 0:
        hour = 12

    # context
    c = {
        'new_opportunity_form': new_opportunity_form(initial={
            'finish_date_year': next_week.year,
            'finish_date_month': next_week.month,
            'finish_date_day': next_week.day,
            'finish_date_hour': hour,
            'finish_date_minute': minute,
            'finish_date_meridiems': meridiems, }),
        'customer_results': customer_results,
        'organisation_id': organisation_id,
        'customer_id': customer_id,
        'opportunity_stage_results': opportunity_stage_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def new_organisation(request):
    """
	To stop duplicates in the system, the code will quickly check to see if
	there is already a company that has either one of the following;
	-- same name
	-- same website
	-- same contact email.
	
	If one of these conditions are met then the user will be returned to the
	form and shown the possible duplicates. If the user accepts this, then
	the organisation is created.	
	"""
    form = new_organisation_form(request.POST or None)
    duplicate_results = None
    if request.method == 'POST':
        if form.is_valid():
            organisation_name = form.cleaned_data['organisation_name']
            organisation_email = form.cleaned_data['organisation_email']
            organisation_website = form.cleaned_data['organisation_website']

            duplicate_results = organisations.objects.filter(
                Q(organisation_name=organisation_name) | Q(organisation_email=organisation_email) | Q(
                    organisation_website=organisation_website))

            """
			If the user has clicked that they accept the duplicate OR if there
			are NO duplicates, just make the organisation :)
			"""
            if ((duplicate_results.count() == 0) or (request.POST.get("save_duplicate"))):
                # Save the form data
                submit_form = organisations(
                    organisation_name=organisation_name,
                    organisation_email=organisation_email,
                    organisation_website=organisation_website,
                    change_user=request.user,
                )
                submit_form.save()

                return HttpResponseRedirect(reverse(organisation_information, args={submit_form.organisations_id}))

    """
	Now that we have determined if the organisations should be saved or not
	we are left with the only options;
	1.) There was no organisation to save
	2.) there was a duplicate organisation and we are asking the user about it
	"""
    # load template
    t = loader.get_template('NearBeach/new_organisation.html')

    # Define the duplication count
    duplication_count = 0;
    if not duplicate_results == None:
        duplication_count = duplicate_results.count()

    # context
    c = {
        'new_organisation_form': form,
        'duplicate_results': duplicate_results,
        'duplication_count': duplication_count,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def new_project(request, organisations_id='', customer_id='', opportunity_id=''):
    print("Organisation ID = ", organisations_id)
    print("Customer ID = ", customer_id)
    print("Opportunity ID = ", opportunity_id)
    if request.method == "POST":
        form = new_project_form(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data['project_name']
            project_description = form.cleaned_data['project_description']
            organisations_id_form = form.cleaned_data['organisations_id']

            # Create the final start/end date fields
            project_start_date = time_combined(
                int(form.cleaned_data['start_date_year']),
                int(form.cleaned_data['start_date_month']),
                int(form.cleaned_data['start_date_day']),
                int(form.cleaned_data['start_date_hour']),
                int(form.cleaned_data['start_date_minute']),
                form.cleaned_data['start_date_meridiems']
            )

            project_end_date = time_combined(
                int(form.cleaned_data['finish_date_year']),
                int(form.cleaned_data['finish_date_month']),
                int(form.cleaned_data['finish_date_day']),
                int(form.cleaned_data['finish_date_hour']),
                int(form.cleaned_data['finish_date_minute']),
                form.cleaned_data['finish_date_meridiems']
            )

            submit_project = project(
                project_name=project_name,
                project_description=project_description,
                organisations_id=organisations_id_form,
                project_start_date=project_start_date,
                project_end_date=project_end_date,
                project_status='New',
                change_user=request.user,
            )

            # Submit the data
            submit_project.save()

            """
			Once the new project has been created, we will obtain a 
			primary key. Using this new primary key we will allocate
			groups to the new project.
			"""
            assigned_to_groups = request.POST.get('assigned_to_groups')

            for row in assigned_to_groups:
                submit_group = project_groups(
                    project_id_id=submit_project.pk,
                    groups_id_id=row,
                    change_user = request.user,
                )
                submit_group.save()

            # If there is a customer id attached to this. Assign the project to the customer and go back to customer informaton
            if (not customer_id == '') and (not customer_id == '0'):
                customer_instance = customers.objects.get(customer_id=customer_id)
                save_project_customers = project_customers(
                    project_id=submit_project,
                    customer_id=customer_instance,
                    change_user=request.user,
                )
                save_project_customers.save()

            print("opportunity id = " + opportunity_id)

            if not opportunity_id == '':
                print("Saving Opportunity Instance")
                opportunity_instance = opportunity.objects.get(opportunity_id=opportunity_id)
                save_project_opportunity = project_opportunity(
                    project_id=submit_project,
                    opportunity_id=opportunity_instance,
                    change_user=request.user,
                )
                save_project_opportunity.save()

            # If there is an organisation id, send the user to organisation info. Otherwise back to project infomration
            if not opportunity_id == '':
                return HttpResponseRedirect(reverse(opportunity_information, args={opportunity_id}))
            if not organisations_id == '':
                return HttpResponseRedirect(reverse(organisation_information, args={organisations_id}))
            elif (not customer_id == '') and (not customer_id == 0):
                return HttpResponseRedirect(reverse(customer_information, args={customer_id}))
            else:
                return HttpResponseRedirect(reverse(project_information, args={submit_project.pk}))

    else:
        # Obtain the groups the user is associated with
        current_user = request.user
        cursor = connection.cursor()

        cursor.execute(
            """
		SELECT DISTINCT
		  groups.group_id
		, groups.group_name

		FROM 
		  user_groups join groups
			on user_groups.group_id_id = groups.group_id

		WHERE 1=1
		AND user_groups.is_deleted = "FALSE"
		AND user_groups.username_id = %s
		"""
            , [current_user.id])
        groups_results = namedtuplefetchall(cursor)

        organisations_results = organisations.objects.filter(is_deleted='FALSE')

        # Setup dates for initalising
        today = datetime.datetime.now()
        next_week = today + datetime.timedelta(days=31)

        """
		We need to do some basic formulations with the hour and and minutes.
		For the hour we need to find all those who are in the PM and
		change both the hour and meridiem accordingly.
		For the minute, we have to create it in 5 minute blocks.
		"""
        hour = today.hour
        minute = int(5 * round(today.minute / 5.0))
        meridiems = 'AM'

        if hour > 12:
            hour = hour - 12
            meridiems = 'PM'
        elif hour == 0:
            hour = 12

        # Load the template
        t = loader.get_template('NearBeach/new_project.html')

        # context
        c = {
            'new_project_form': new_project_form(initial={
                'organisations_id': organisations_id,
                'start_date_year': today.year,
                'start_date_month': today.month,
                'start_date_day': today.day,
                'start_date_hour': hour,
                'start_date_minute': minute,
                'start_date_meridiems': meridiems,
                'finish_date_year': next_week.year,
                'finish_date_month': next_week.month,
                'finish_date_day': next_week.day,
                'finish_date_hour': hour,
                'finish_date_minute': minute,
                'finish_date_meridiems': meridiems, }),
            'groups_results': groups_results,
            'groups_count': groups_results.__len__(),
            'opportunity_id': opportunity_id,
            'organisations_count': organisations_results.count(),
            'organisations_id': organisations_id,
            'customer_id': customer_id,
        }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def new_quote(request,destination,primary_key):
    if request.method == "POST":
        form = new_quote_form(request.POST)
        if form.is_valid():
            quote_title=form.cleaned_data['quote_title']
            quote_terms=form.cleaned_data['quote_terms']
            quote_stage_id=form.cleaned_data['quote_stage_id']
            quote_approval_status_id=form.cleaned_data['quote_approval_status_id']
            customer_notes=form.cleaned_data['customer_notes']

            # Create the final start/end date fields
            quote_valid_till = time_combined(
                int(form.cleaned_data['quote_valid_till_year']),
                int(form.cleaned_data['quote_valid_till_month']),
                int(form.cleaned_data['quote_valid_till_day']),
                int(form.cleaned_data['quote_valid_till_hour']),
                int(form.cleaned_data['quote_valid_till_minute']),
                form.cleaned_data['quote_valid_till_meridiems']
            )
            quote_stage_instance = list_of_quote_stages.objects.get(quote_stages_id=quote_stage_id.quote_stages_id)
            quote_approval_status_instance=list_of_quote_approval_status.objects.get(
                quote_approval_status_id=quote_approval_status_id.quote_approval_status_id
            )
            submit_quotes = quotes(
                quote_title=quote_title,
                quote_terms=quote_terms,
                quote_stage_id=quote_stage_instance,
                quote_approval_status_id=quote_approval_status_instance,
                customer_notes=customer_notes,
                quote_valid_till=quote_valid_till,
                change_user=request.user
            )
            submit_quotes.save()

            #Now to go to the quote information page
            return HttpResponseRedirect(reverse(quote_information, args={submit_quotes.quote_id}))

        else:
            print(form.errors)

    # Load the template
    t = loader.get_template('NearBeach/new_quote.html')

    # context
    c = {
        'new_quote_form': new_quote_form,
        'primary_key': primary_key,
        'destination': destination,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def new_task(request, organisations_id='', customer_id='', opportunity_id=''):
    # Define if the page is loading in POST
    if request.method == "POST":
        form = new_task_form(request.POST)
        if form.is_valid():
            task_short_description = form.cleaned_data['task_short_description']
            task_long_description = form.cleaned_data['task_long_description']
            organisations_id_form = form.cleaned_data['organisations_id']

            # Create the final start/end date fields
            task_start_date = time_combined(
                int(form.cleaned_data['start_date_year']),
                int(form.cleaned_data['start_date_month']),
                int(form.cleaned_data['start_date_day']),
                int(form.cleaned_data['start_date_hour']),
                int(form.cleaned_data['start_date_minute']),
                form.cleaned_data['start_date_meridiems']
            )

            task_end_date = time_combined(
                int(form.cleaned_data['finish_date_year']),
                int(form.cleaned_data['finish_date_month']),
                int(form.cleaned_data['finish_date_day']),
                int(form.cleaned_data['finish_date_hour']),
                int(form.cleaned_data['finish_date_minute']),
                form.cleaned_data['finish_date_meridiems']
            )

            submit_task = tasks(
                task_short_description=task_short_description,
                task_long_description=task_long_description,
                organisations_id=organisations_id_form,
                task_start_date=task_start_date,
                task_end_date=task_end_date,
                task_status='New',
                change_user = request.user,
            )

            # Submit the data
            submit_task.save()

            """
			Once the new project has been created, we will obtain a 
			primary key. Using this new primary key we will allocate
			groups to the new project.
			"""
            assigned_to_groups = request.POST.get('assigned_to_groups')

            for row in assigned_to_groups:
                submit_group = tasks_groups(
                    tasks_id_id=submit_task.pk,
                    groups_id_id=row,
                    change_user=request.user,
                )
                submit_group.save()

            """
			If we have come from the customer information screen, you will notice that there are some extra
			variables in the URL. If one of them is the customer_id, we will use that to assign the task
			to the customer and then go back to that customer information page
			"""
            if (not customer_id == '') and (not customer_id == '0'):
                customer_instance = customers.objects.get(customer_id=customer_id)
                save_tasks_customers = tasks_customers(
                    tasks_id=submit_task,
                    customer_id=customer_instance,
                    change_user=request.user,
                )
                save_tasks_customers.save()

            if (not opportunity_id == ''):
                opportunity_instance = opportunity.objects.get(opportunity_id=opportunity_id)
                save_tasks_opportunity = tasks_opportunity(
                    tasks_id=submit_task,
                    opportunity_id=opportunity_instance,
                    change_user=request.user,
                )
                save_tasks_opportunity.save()

                # Lets go back to the customer

            # If there is an organisation id, send the user to organisation info. Otherwise back to project infomration
            if not opportunity_id == '':
                return HttpResponseRedirect(reverse(opportunity_information, args={opportunity_id}))
            if not organisations_id == '':
                return HttpResponseRedirect(reverse(organisation_information, args={organisations_id}))
            elif (not customer_id == '') and (not customer_id == 0):
                return HttpResponseRedirect(reverse(customer_information, args={customer_id}))
            else:
                return HttpResponseRedirect(reverse(project_information, args={submit_project.pk}))

    else:
        # Obtain the groups the user is associated with
        current_user = request.user
        cursor = connection.cursor()

        cursor.execute(
            """
		SELECT DISTINCT
		  groups.group_id
		, groups.group_name

		FROM 
		  user_groups join groups
			on user_groups.group_id_id = groups.group_id

		WHERE 1=1
		AND user_groups.is_deleted = "FALSE"
		AND user_groups.username_id = %s
		"""
            , [current_user.id])
        groups_results = namedtuplefetchall(cursor)

        # Setup dates for initalising
        today = datetime.datetime.now()
        next_week = today + datetime.timedelta(days=31)

        """
		We need to do some basic formulations with the hour and and minutes.
		For the hour we need to find all those who are in the PM and
		change both the hour and meridiem accordingly.
		For the minute, we have to create it in 5 minute blocks.
		"""
        hour = today.hour
        minute = int(5 * round(today.minute / 5.0))
        meridiems = 'AM'

        if hour > 12:
            hour = hour - 12
            meridiems = 'PM'
        elif hour == 0:
            hour = 12

        # Loaed the template
        t = loader.get_template('NearBeach/new_task.html')

        c = {
            'new_task_form': new_task_form(
                initial={
                    'start_date_year': today.year,
                    'start_date_month': today.month,
                    'start_date_day': today.day,
                    'start_date_hour': hour,
                    'start_date_minute': minute,
                    'start_date_meridiems': meridiems,
                    'finish_date_year': next_week.year,
                    'finish_date_month': next_week.month,
                    'finish_date_day': next_week.day,
                    'finish_date_hour': hour,
                    'finish_date_minute': minute,
                    'finish_date_meridiems': meridiems,
                    'organisations_id': organisations_id,
                }),
            'groups_results': groups_results,
            'groups_count': groups_results.__len__(),
            'organisations_id': organisations_id,
            'organisations_count': organisations.objects.filter(is_deleted='FALSE').count(),
            'customer_id': customer_id,
            'opportunity_id': opportunity_id,
        }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def next_step(request, next_step_id, opportunity_id):
    next_step_save = opportunity_next_step.objects.get(id=next_step_id)
    next_step_save.next_step_completed = 1
    next_step.change_user=request.user
    next_step_save.save()

    return HttpResponseRedirect(
        reverse(
            opportunity_information,
            args={opportunity_id}
        )
    )


@login_required(login_url='login')
def opportunity_information(request, opportunity_id):
    if request.method == "POST":
        form = opportunity_information_form(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user

            save_opportunity = opportunity.objects.get(opportunity_id=opportunity_id)

            # Save opportunity information
            save_opportunity.opportunity_name = form.cleaned_data['opportunity_name']
            save_opportunity.opportunity_description = form.cleaned_data['opportunity_description']
            save_opportunity.opportunity_amount = form.cleaned_data['opportunity_amount']
            save_opportunity.opportunity_success_probability = form.cleaned_data['opportunity_success_probability']
            save_opportunity.change_user=request.user

            # Instance needed
            save_opportunity.currency_id = list_of_currency.objects.get(currency_id=int(request.POST['currency_id']))
            save_opportunity.amount_type_id = list_of_amount_type.objects.get(
                amount_type_id=int(request.POST['amount_type_id']))
            save_opportunity.opportunity_stage_id = list_of_opportunity_stage.objects.get(
                opportunity_stage_id=int(request.POST['opportunity_stage_id']))


            save_opportunity.opportunity_expected_close_date = time_combined(
                int(form.cleaned_data['finish_date_year']),
                int(form.cleaned_data['finish_date_month']),
                int(form.cleaned_data['finish_date_day']),
                int(form.cleaned_data['finish_date_hour']),
                int(form.cleaned_data['finish_date_minute']),
                form.cleaned_data['finish_date_meridiems']
            )

            #Save the opportunity
            save_opportunity.save()
            opportunity_instance = opportunity.objects.get(opportunity_id=opportunity_id)

            # Save the to-do if required
            next_step = form.cleaned_data['next_step']
            if not next_step == '':
                save_next_step = opportunity_next_step(
                    opportunity_id=opportunity_instance,
                    next_step_description=next_step,
                    change_user_id=request.user.id, #WHY???
                    user_id=current_user,
                )
                save_next_step.save()

            # If we need to add more users :D
            select_groups = form.cleaned_data['select_groups']
            if select_groups:
                for row in select_groups:
                    group_instance = groups.objects.get(group_id=row.group_id)
                    permission_save = opportunity_permissions(
                        opportunity_id=opportunity_instance,
                        groups_id=group_instance,
                        user_id=current_user,
                        change_user=request.user,
                    )
                    permission_save.save()
                #Will remove the ALL USERS permissions now that we have limited the permissions
                opportunity_permissions.objects.filter(
                    opportunity_id=opportunity_id,
                    all_users='TRUE',
                    is_deleted='FALSE'
                ).update(is_deleted='TRUE')

            select_users = form.cleaned_data['select_users']
            print(select_users)
            if select_users:
                for row in select_users:
                    assigned_user_instance = auth.models.User.objects.get(username=row)
                    permission_save = opportunity_permissions(
                        opportunity_id=opportunity_instance,
                        assigned_user=assigned_user_instance,
                        user_id=current_user,
                        change_user=request.user,
                    )
                    permission_save.save()
                #Will remove the ALL USERS permissions now that we have limited the permissions
                opportunity_permissions.objects.filter(
                    opportunity_id=opportunity_id,
                    all_users='TRUE',
                    is_deleted='FALSE'
                ).update(is_deleted='TRUE')
        else:
            print(form.errors)

    else:
        """
        We want to limit who can see what opportunity. The exception to this is for the user
        who just created the opportunity. (I should program in a warning stating that they
        might not be able to see the opportunity again unless they add themselfs to the 
        permissions list.

        The user has to meet at least one of these conditions;
        1.) User has permission
        2.) User's group has permission
        3.) All users have permission
        """
        user_groups_results = user_groups.objects.filter(username=request.user)

        permission_results = opportunity_permissions.objects.filter(
            Q(
                Q(assigned_user=request.user)  # User has permission
                | Q(groups_id__in=user_groups_results.values('group_id'))  # User's groups have permission
                | Q(all_users='TRUE')  # All users have access
            )
            & Q(opportunity_id=opportunity_id)
        )

        print(permission_results)

        if (not permission_results):
            return HttpResponseRedirect(
                reverse(
                    permission_denied,
                )
            )


    # Data
    project_results = project_opportunity.objects.filter(
        opportunity_id=opportunity_id,
        is_deleted='FALSE',
    )
    tasks_results = tasks_opportunity.objects.filter(
        opportunity_id=opportunity_id,
        is_deleted='FALSE',
    )
    opportunity_results = opportunity.objects.get(opportunity_id=opportunity_id)
    customer_results = customers.objects.filter(organisations_id=opportunity_results.organisations_id)
    next_step_results = opportunity_next_step.objects.filter(opportunity_id=opportunity_id)
    group_permissions = opportunity_permissions.objects.filter(
        groups_id__isnull=False,
        opportunity_id=opportunity_id,
        is_deleted='FALSE',
    ).distinct()
    user_permissions = auth.models.User.objects.filter(
        id__in=opportunity_permissions.objects.filter(
            assigned_user__isnull=False,
            opportunity_id=opportunity_id,
            is_deleted='FALSE',
        ).values('assigned_user').distinct()
    )
    print(user_permissions)

    end_hour = opportunity_results.opportunity_expected_close_date.hour
    end_meridiem = u'AM'

    print(str(end_hour))

    if end_hour > 12:
        end_hour = end_hour - 12
        end_meridiem = 'PM'
    elif end_hour == 0:
        end_hour = 12

    # initial data
    initial = {
        'finish_date_year': opportunity_results.opportunity_expected_close_date.year,
        'finish_date_month': opportunity_results.opportunity_expected_close_date.month,
        'finish_date_day': opportunity_results.opportunity_expected_close_date.day,
        'finish_date_hour': end_hour,
        'finish_date_minute': opportunity_results.opportunity_expected_close_date.minute,
        'finish_date_meridiems': end_meridiem,
    }

    # Loaed the template
    t = loader.get_template('NearBeach/opportunity_information.html')

    c = {
        'opportunity_id': str(opportunity_id),
        'opportunity_information_form': opportunity_information_form(
            instance=opportunity_results,
            initial=initial,
        ),
        'opportunity_results': opportunity_results,
        'customer_results': customer_results,
        'next_step_results': next_step_results,
        'group_permissions': group_permissions,
        'user_permissions': user_permissions,
        'project_results': project_results,
        'tasks_results': tasks_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def organisation_information(request, organisations_id):
    # Get the data from the form if the information has been submitted
    if request.method == "POST":
        form = organisation_information_form(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            # Define the data we will edit
            #			save_data = customers.objects.get(customer_id=customer_id)

            save_data = organisations.objects.get(organisations_id=organisations_id)


            # Extract it from website
            save_data.organisation_name = form.cleaned_data['organisation_name']
            save_data.organisation_website = form.cleaned_data['organisation_website']
            save_data.change_user=request.user

            # Check to see if the picture has been updated
            update_profile_picture = request.FILES.get('update_profile_picture')
            if not update_profile_picture == None:
                save_data.organisation_profile_picture = update_profile_picture

            # Save
            save_data.save()

            """
            If the user has written something in the contact section, we want to save it
            """
            contact_history_notes = form.cleaned_data['contact_history']

            if not contact_history_notes == '':
                # Lets save some contact history
                # organisation_id = form.cleaned_data['organisations_id'] #Not going to work :( #organisations_results.organisations_id
                contact_type = form.cleaned_data['contact_type']

                # Create the final start/end date fields
                task_start_date = time_combined(
                    int(form.cleaned_data['start_date_year']),
                    int(form.cleaned_data['start_date_month']),
                    int(form.cleaned_data['start_date_day']),
                    0,
                    0,
                    'AM'
                )

                # documents
                contact_attachment = request.FILES.get('contact_attachment')

                if contact_attachment:
                    documents_save = documents(
                        document_description=contact_attachment,
                        document=contact_attachment,
                        change_user=request.user,
                    )
                    documents_save.save()

                    #Add to document permissions
                    document_permissions_save = document_permissions(
                        document_key=documents_save,
                        organisations_id=organisations.objects.get(organisations_id=organisations_id),
                        change_user=request.user,
                    )
                    document_permissions_save.save()


                submit_history = contact_history(
                    organisations_id=save_data,
                    contact_type=contact_type,
                    contact_date=task_start_date,
                    contact_history=contact_history_notes,
                    user_id=current_user,
                    change_user=request.user,
                    #document_key=documents_save,
                )
                if contact_attachment:
                    submit_history.document_key=documents_save
                submit_history.save()



            """
			Document Uploads
			"""
            document = request.FILES.get('document')
            if not document == None:
                document_save = documents(
                    #organisations_id=save_data,
                    #document_description=form.cleaned_data['document_description'],
                    document=form.cleaned_data['document'],
                    change_user=request.user,
                )
                document_description = form.cleaned_data['document_description']
                if document_description=="":
                    document_save.document_description=document_save.document
                else:
                    document_save.document_description=document_description
                document_save.save()

                document_permissions_save = document_permissions(
                    organisations_id=save_data,
                    change_user=request.user,
                    document_key=document_save,
                )
                document_permissions_save.save()

    # Query the database for organisation information
    organisation_results = organisations.objects.get(pk=organisations_id)
    campus_results = organisations_campus.objects.filter(organisations_id=organisations_id)
    customers_results = customers.objects.filter(organisations_id=organisation_results)
    organisation_contact_history = contact_history.objects.filter(organisations_id=organisations_id)
    customer_document_results = document_permissions.objects.filter(
        organisations_id=organisations_id,
        customer_id__isnull=False
    )
    organisation_document_results = document_permissions.objects.filter(
        organisations_id=organisations_id,
        customer_id__isnull=True
    )
    project_results = project.objects.filter(organisations_id=organisations_id)
    task_results = tasks.objects.filter(organisations_id=organisations_id)
    #opportunity_results = opportunity.objects.filter(organisations_id=organisations_id)
    """
    We need to limit the amount of opportunities to those that the user has access to.
    """
    user_groups_results = user_groups.objects.filter(username=request.user)

    opportunity_permissions_results = opportunity_permissions.objects.filter(
        Q(
            Q(assigned_user=request.user)  # User has permission
            | Q(groups_id__in=user_groups_results.values('group_id'))  # User's groups have permission
            | Q(all_users='TRUE')  # All users have access
        )
    )
    opportunity_results = opportunity.objects.filter(
        organisations_id=organisations_id,
        opportunity_id__in=opportunity_permissions_results.values('opportunity_id')
    )


    # Date required to initiate date
    today = datetime.datetime.now()

    # Loaed the template
    t = loader.get_template('NearBeach/organisation_information.html')

    # profile picture


    try:
        profile_picture = organisation_results.organisation_profile_picture.url
    except:
        profile_picture = ''

    c = {
        'organisation_results': organisation_results,
        'campus_results': campus_results,
        'customers_results': customers_results,
        'organisation_information_form': organisation_information_form(
            instance=organisation_results,
            initial={
                'start_date_year': today.year,
                'start_date_month': today.month,
                'start_date_day': today.day,
            }),
        'organisation_contact_history': organisation_contact_history,
        'profile_picture': profile_picture,
        'customer_document_results': customer_document_results,
        'organisation_document_results': organisation_document_results,
        'project_results': project_results,
        'task_results': task_results,
        'opportunity_results': opportunity_results,
        'PRIVATE_MEDIA_URL': settings.PRIVATE_MEDIA_URL,
    }

    return HttpResponse(t.render(c, request))

@login_required(login_url='login')
def permission_denied(request):
    #The user has no access to this page
    # Load the template
    t = loader.get_template('NearBeach/permission_denied.html')

    # context
    c = {
    }

    return HttpResponse(t.render(c, request))



"""
TEMP CODE
"""
@login_required(login_url='login')
def private_document(request, document_key):
    """
    This is temp code. Hopefully I will make this function
    a lot better
    """
    PRIVATE_MEDIA_ROOT = settings.PRIVATE_MEDIA_ROOT
    #Now get the document location and return that to the user.
    document_results=documents.objects.get(pk=document_key)

    path = PRIVATE_MEDIA_ROOT + '/' + document_results.document.name
    #path = '/home/luke/Downloads/gog_gods_will_be_watching_2.1.0.9.sh'

    """
    Serve private files to users with read permission.
    """
    #logger.debug('Serving {0} to {1}'.format(path, request.user))
    #if not permissions.has_read_permission(request, path):
    #    if settings.DEBUG:
    #        raise PermissionDenied
    #    else:
    #        raise Http404('File not found')
    return server.serve(request, path=path)

"""
END TEMP DOCUMENT
"""

@login_required(login_url='login')
def project_information(request, project_id):
    """
	We need to determine if the user has access to any of the groups that
	this project is associated to. We will do a simple count(*) SQL QUERY
	that will determine this.
	"""
    current_user = request.user

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
		SELECT COUNT(*)
		FROM
		  project_groups
		, user_groups
		
		WHERE 1=1
		AND project_groups.groups_id_id = user_groups.group_id_id
		AND project_groups.is_deleted = 'FALSE'
		AND user_groups.is_deleted = 'FALSE'
		AND user_groups.username_id = %s
		AND project_groups.project_id_id = %s
	""", [current_user.id, project_id])
    has_permission = cursor.fetchall()

    if not has_permission[0][0] == 1 and not request.session['IS_ADMIN'] == 'TRUE':
        # Send them to permission denied!!
        return HttpResponseRedirect(
            reverse(
                permission_denied,
            )
        )

    """
	There are two buttons on the project information page. Both will come
	here. Both will save the data, however only one of them will resolve
	this project.
	"""
    # Get the data from the form if the information has been submitted
    if request.method == "POST":
        form = project_information_form(request.POST, request.FILES)
        if form.is_valid():
            # Define the data we will edit
            project_results = project.objects.get(project_id=project_id)

            project_results.project_name = form.cleaned_data['project_name']
            project_results.project_description = form.cleaned_data['project_description']

            # Create the final start/end date fields
            project_results.project_start_date = time_combined(
                int(form.cleaned_data['start_date_year']),
                int(form.cleaned_data['start_date_month']),
                int(form.cleaned_data['start_date_day']),
                int(form.cleaned_data['start_date_hour']),
                int(form.cleaned_data['start_date_minute']),
                form.cleaned_data['start_date_meridiems']
            )

            project_results.project_end_date = time_combined(
                int(form.cleaned_data['finish_date_year']),
                int(form.cleaned_data['finish_date_month']),
                int(form.cleaned_data['finish_date_day']),
                int(form.cleaned_data['finish_date_hour']),
                int(form.cleaned_data['finish_date_minute']),
                form.cleaned_data['finish_date_meridiems']
            )

            # Check to make sure the resolve button was hit
            if 'Resolve' in request.POST:
                # Well, we have to now resolve the data
                project_results.project_status = 'Resolved'

            project_results.change_user=request.user
            project_results.save()


            if 'add_customer_submit' in request.POST:
                # The user has tried adding a customer
                customer_id = int(request.POST.get("add_customer_select"))

                submit_customer = project_customers(
                    project_id=project.objects.get(pk=project_id),
                    customer_id=customers.objects.get(pk=customer_id),
                    change_user=request.user,
                )

                submit_customer.save()

            cost_description = form.cleaned_data['cost_description']
            cost_amount = form.cleaned_data['cost_amount']
            if ((not cost_description == '') and ((cost_amount <= 0) or (cost_amount >= 0))):
                submit_cost = costs(
                    project_id=project.objects.get(pk=project_id),
                    cost_description=cost_description,
                    cost_amount=cost_amount,
                    change_user=request.user,
                )
                submit_cost.save()

            """
			If the user has added another user to the project
			auth.models.User.objects.all() <-bug in the system,this is workaround
			"""
            if 'add_user_submit' in request.POST:
                user_results = int(request.POST.get("add_user_select"))
                user_instance = auth.models.User.objects.get(pk=user_results)
                submit_associate_user = assigned_users(
                    user_id=user_instance,
                    project_id=project.objects.get(pk=project_id),
                    change_user=request.user,
                )
                submit_associate_user.save()

            """
			If the user has submitted a new document. We only upload the document IF and ONLY IF the user
			has selected the "Submit" button on the "New Document" dialog. We do not want to accidently
			upload a document if we hit the "SAVE" button from a different location
			"""
            if 'new_document' in request.POST:
                # document = request.FILES['document']
                document = request.FILES.get('document')
                document_description = request.POST.get("document_description")
                document_url_location = request.POST.get("document_url_location")

                parent_folder_id = request.POST.get("parent_folder_id")

                submit_document = documents(
                    document=document,
                    document_description=document_description,
                    document_url_location=document_url_location,
                    change_user=request.user,
                )
                try:
                    submit_document.document_folder_id = folders.objects.get(
                        folder_id=int(parent_folder_id),
                        change_user=request.user,
                    )
                    submit_document.save()
                except:
                    submit_document.save()
                submit_document_permissions = document_permissions(
                    project_id=project.objects.get(pk=project_id),
                    change_user=request.user,
                )

            """
			Fuck - someone wants to create a new folder...
			"""
            if 'new_folder' in request.POST:
                document_folder_description = form.cleaned_data['folder_description']
                folder_location = request.POST.get("folder_location")

                submit_folder = folders(
                    project_id=project.objects.get(pk=project_id),
                    folder_description=document_folder_description,
                    change_user=request.user,
                )

                try:
                    submit_folder.parent_folder_id = folders.objects.get(
                        folder_id=int(folder_location),
                    )
                    submit_folder.save()
                except:
                    submit_folder.save()

            # Now save the new project history.
            project_history_text_results = form.cleaned_data['project_history_text']

            if not project_history_text_results == '':
                current_user = request.user

                ### TEMP SOLUTION ###
                project_id_connection = project.objects.get(pk=project_id)
                ### END TEMP SOLUTION ###

                data = project_history(
                    project_id=project_id_connection,
                    user_id=current_user,
                    project_history=project_history_text_results,
                    user_infomation=current_user.id,
                    change_user = request.user,
                )
                data.save()

        else:
            print(form.errors)

    project_results = get_object_or_404(project, project_id=project_id)

    # Obtain the required data
    project_history_results = project_history.objects.filter(project_id=project_id, is_deleted='FALSE')
    cursor.execute(
        """
        SELECT DISTINCT
          documents.document_key
        , documents.document_description
        , documents.document_url_location
        , documents.document
        , documents_folder.folder_id_id
        
        FROM 
          documents
          LEFT JOIN
                document_permissions
                ON documents.document_key = document_permissions.document_key_id
		LEFT JOIN
				folder
				ON folder.project_id_id = %s
		LEFT JOIN
				documents_folder
				ON documents_folder.folder_id_id = folder.folder_id
				AND documents_folder.document_key_id = documents.document_key

        
        WHERE 1=1
        
        AND document_permissions.project_id_id = %s
        ORDER BY documents.document_description 
        """, [project_id,project_id]
    )
    documents_results = cursor.fetchall()

    folders_results = folders.objects.filter(
        project_id=project_id,
        is_deleted='FALSE'
    ).order_by(
        'folder_description'
    )
    costs_results = costs.objects.filter(project_id=project_id, is_deleted='FALSE')

    """
	The 24 hours to 12 hours formula.
	00:00 means that it is 12:00 AM - change required for hour
	01:00 means that it is 01:00 AM - no change required
	12:00 means that it is 12:00 PM - change required for meridiem
	13:00 means that it is 01:00 PM - change required for hour and meridiem
	"""
    start_hour = project_results.project_start_date.hour
    start_meridiem = u'AM'
    if start_hour == 0:
        start_hour = 12
    elif start_hour == 12:
        start_meridiem = u'PM'
    elif start_hour > 12:
        start_hour = start_hour - 12
        start_meridiem = u'PM'

    end_hour = project_results.project_end_date.hour
    end_meridiem = u'AM'
    if end_hour == 0:
        end_hour = 12
    elif end_hour == 12:
        end_meridiem = u'PM'
    elif end_hour > 12:
        end_hour = end_hour - 12
        end_meridiem = u'PM'

    # Setup the initial data for the form
    initial = {
        'project_name': project_results.project_name,
        'project_description': project_results.project_description,
        'start_date_year': project_results.project_start_date.year,
        'start_date_month': project_results.project_start_date.month,
        'start_date_day': project_results.project_start_date.day,
        'start_date_hour': start_hour,
        'start_date_minute': project_results.project_start_date.minute,
        'start_date_meridiems': start_meridiem,
        'finish_date_year': project_results.project_end_date.year,
        'finish_date_month': project_results.project_end_date.month,
        'finish_date_day': project_results.project_end_date.day,
        'finish_date_hour': end_hour,
        'finish_date_minute': project_results.project_end_date.minute,
        'finish_date_meridiems': end_meridiem,
    }

    # Query the database for associated task information
    cursor = connection.cursor()
    cursor.execute("""
		SELECT DISTINCT
		  tasks.tasks_id
		, tasks.task_short_description
		, tasks.task_end_date
		FROM tasks
			JOIN project_tasks
			ON tasks.tasks_id = project_tasks.task_id
			AND project_tasks.is_deleted = 'FALSE'
			AND project_id = %s
		""", [project_id])
    associated_tasks_results = namedtuplefetchall(cursor)

    cursor.execute("""
		SELECT DISTINCT
		  customers.customer_first_name
		, customers.customer_last_name
		, project_customers.customer_description
		, customers.customer_email
		, customers_campus_information.campus_nickname
		, customers_campus_information.customer_phone
		FROM
		  customers LEFT JOIN 
			(SELECT * FROM customers_campus join organisations_campus ON customers_campus.campus_id_id = organisations_campus.id) as customers_campus_information
			ON customers.customer_id = customers_campus_information.customer_id_id
		, project_customers
		WHERE 1=1
		AND customers.customer_id = project_customers.customer_id_id
		AND project_customers.project_id_id = %s
	""", [project_id])
    project_customers_results = namedtuplefetchall(cursor)

    cursor.execute("""
		SELECT DISTINCT 
		  customers.customer_id
		, customers.customer_first_name || ' ' || customers.customer_last_name AS customer_name
		
		FROM
		  project 
		, organisations LEFT JOIN customers
			ON organisations.organisations_id = customers.organisations_id_id
		
		WHERE 1=1
		AND project.organisations_id_id = organisations.organisations_id
		
		AND customers.customer_id NOT IN (SELECT DISTINCT project_customers.customer_id_id
					FROM project_customers
					WHERE 1=1
					AND project_customers.project_id_id = project.project_id
					AND project_customers.is_deleted = 'FALSE')
		
		
		-- LINKS --
		AND organisations.organisations_id = %s
		AND project.project_id = %s
		-- END LINKS --
	""", [project_results.organisations_id_id, project_id])
    new_customers_results = namedtuplefetchall(cursor)

    cursor.execute("""
			SELECT DISTINCT
			  auth_user.id
			, auth_user.username
			, auth_user.first_name
			, auth_user.last_name
			, auth_user.first_name || ' ' || auth_user.last_name AS "Name"
			, auth_user.email
			FROM
			  project_groups
			, user_groups
			, auth_user

			WHERE 1=1

			--AUTH_USER CONDITIONS
			AND auth_user.is_active=1

			--PROJECT_GROUPS CONDITIONS
			AND project_groups.project_id_id=%s

			-- JOINS --
			AND project_groups.groups_id_id=user_groups.group_id_id
			AND user_groups.username_id=auth_user.id
			-- END JOINS --
		""", [project_id])
    users_results = namedtuplefetchall(cursor)

    assigned_results = assigned_users.objects.filter(project_id=project_id)

    # Load the template
    t = loader.get_template('NearBeach/project_information.html')

    # context
    c = {
        'project_information_form': project_information_form(initial=initial),
        'project_results': project_results,
        'associated_tasks_results': associated_tasks_results,
        'project_history_results': project_history_results,
        'project_customers_results': project_customers_results,
        'new_customers_results': new_customers_results,
        'documents_results': simplejson.dumps(documents_results,encoding='utf-8'),
        'folders_results': serializers.serialize('json', folders_results),
        'media_url': settings.MEDIA_URL,
        'users_results': users_results,
        'assigned_results': assigned_results.values(
            'user_id',
            'user_id__username',
            'user_id__first_name',
            'user_id__last_name',
        ).distinct(),
        'costs_results': costs_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def quote_information(request, quote_id):
    quotes_results = quotes.objects.get(quote_id=quote_id)


    # Load the template
    t = loader.get_template('NearBeach/quote_information.html')

    # context
    c = {
        'quotes_results': quotes_results,
        'quote_information_form': quote_information_form,
    }

    return HttpResponse(t.render(c, request))

@login_required(login_url='login')
def resolve_project(request, project_id):
    project_update = project.objects.get(project_id=project_id)
    project_update.project_status = 'Resolved'
    project_update.change_user=request.user
    project_update.save()
    return HttpResponseRedirect(reverse('active_projects'))


@login_required(login_url='login')
def resolve_task(request, task_id):
    task_update = tasks.object.get(task_id=task_id)
    task_update.task_status = 'Resolved'
    task_update.change_user=request.user
    task_update.save()
    return HttpResponseRedirect(reverse('active_projects'))


@login_required(login_url='login')
def search(request):
    # Load the template
    t = loader.get_template('NearBeach/search.html')

    """
	We will use the POST varable to help filter the results from the 
	database. The results will then appear below
	"""
    search_results = ''

    # Define if the page is loading in POST
    if request.method == "POST":
        form = search_form(request.POST)
        if form.is_valid():
            search_results = form.cleaned_data['search_for']

    """
	This is where the magic happens. I will remove all spaces and replace
	them with a wild card. This will be used to search the concatenated
	first and last name fields
	"""
    search_like = '%'

    for split_row in search_results.split(' '):
        search_like += split_row
        search_like += '%'

    # Query the database for organisations
    cursor = connection.cursor()
    cursor.execute("""
		SELECT DISTINCT
		project.*
		, organisations.organisation_name
		FROM project JOIN organisations
		ON project.organisations_id_id = organisations.organisations_id
		WHERE 1=1
		AND (
			project.project_id like %s
			or project.project_name like %s
			or project.project_description like %s
			)
		""", [search_like, search_like, search_like])
    project_results = namedtuplefetchall(cursor)

    # Get list of tasks
    cursor.execute("""
		SELECT DISTINCT
		tasks.*
		, organisations.organisation_name
		FROM tasks JOIN organisations
		ON tasks.organisations_id_id = organisations.organisations_id
		WHERE 1=1
		AND (
			tasks.tasks_id like %s
			or tasks.task_short_description like %s
			or tasks.task_long_description like %s
		)
	""", [search_like, search_like, search_like])
    task_results = namedtuplefetchall(cursor)

    # context
    c = {
        'search_form': search_form(initial={'search_for': search_results}),
        'project_results': project_results,
        'task_results': task_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def search_customers(request):
    # Load the template
    t = loader.get_template('NearBeach/search_customers.html')

    """
	We will use the POST varable to help filter the results from the 
	database. The results will then appear below
	"""
    search_customers_results = ''

    # Define if the page is loading in POST
    if request.method == "POST":
        form = search_customers_form(request.POST)
        if form.is_valid():
            search_customers_results = form.cleaned_data['search_customers']

    """
	This is where the magic happens. I will remove all spaces and replace
	them with a wild card. This will be used to search the concatenated
	first and last name fields
	"""
    search_customers_like = '%'

    for split_row in search_customers_results.split(' '):
        search_customers_like += split_row
        search_customers_like += '%'

    # Query the database for organisations
    cursor = connection.cursor()
    cursor.execute("""
		SELECT DISTINCT
		  customers.customer_id
		, customers.customer_first_name
		, customers.customer_last_name
		, organisations.organisation_name

		FROM customers JOIN organisations
			ON customers.organisations_id_id = organisations.organisations_id
		WHERE 1=1
		AND UPPER(customers.customer_first_name || ' ' || customers.customer_last_name) LIKE %s
		""", [search_customers_like])
    customers_results = namedtuplefetchall(cursor)

    # context
    c = {
        'search_customers_form': search_customers_form(initial={'search_customers': search_customers_results}),
        'customers_results': customers_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def search_organisations(request):
    # Load the template
    t = loader.get_template('NearBeach/search_organisations.html')

    """
	We will use the following varable to help filterer our database
	results. ***WrTIE BETTER TOO TIRED TO DESCRIBE THIS!!!***
	"""
    search_organisations_results = ''

    # Define if the page is loading in POST
    if request.method == "POST":
        form = search_organisations_form(request.POST)
        if form.is_valid():
            search_organisations_results = form.cleaned_data['search_organisations']

    """
	This is where the magic happens. I will remove all spaces and replace
	them with a wild card. This will be used to search the concatenated
	first and last name fields
	"""
    search_organisations_like = '%'

    for split_row in search_organisations_results.split(' '):
        search_organisations_like += split_row
        search_organisations_like += '%'

    # Now search the organisations
    # organisations_results = organisations.objects.filter(organisation_name__contains = search_organisations_like)

    # Query the database for organisations
    cursor = connection.cursor()
    cursor.execute("""
		SELECT DISTINCT
		  organisations.organisations_id
		, organisations.organisation_name
		, organisations.organisation_website
		, organisations.organisation_email
		FROM organisations
		WHERE 1=1
		AND organisations.organisation_name LIKE %s
		""", [search_organisations_like])
    organisations_results = namedtuplefetchall(cursor)

    # context
    c = {
        'search_organisations_form': search_organisations_form(
            initial={'search_organisations': search_organisations_results}),
        'organisations_results': organisations_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def search_projects_tasks(request):
    # Load the template
    t = loader.get_template('NearBeach/search_projects_and_tasks.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def task_information(request, task_id):
    """
	We need to determine if the user has access to any of the groups that
	this task is associated to. We will do a simple count(*) SQL QUERY
	that will determine this.
	"""
    current_user = request.user

    # Setup connection to the database and query it
    cursor = connection.cursor()

    cursor.execute("""
		SELECT COUNT(*)
		FROM
		  tasks_groups
		, user_groups
		WHERE 1=1
		AND tasks_groups.groups_id_id = user_groups.group_id_id
		AND tasks_groups.is_deleted = 'FALSE'
		AND user_groups.is_deleted = 'FALSE'
		AND user_groups.username_id = %s
		AND tasks_groups.tasks_id_id = %s
	""", [current_user.id, task_id])
    has_permission = cursor.fetchall()

    if not has_permission[0][0] == 1 and not request.session['IS_ADMIN'] == 'TRUE':
        # Send them to permission denied!!
        return HttpResponseRedirect(
            reverse(
                permission_denied,
            )
        )
    """
	There are two buttons on the task information page. Both will come
	here. Both will save the data, however only one of them will resolve
	the task.
	"""
    # Define the data we will edit
    # task_results = tasks.objects.get(tasks_id = task_id)
    task_results = get_object_or_404(tasks, tasks_id=task_id)

    # Get the data from the form
    if request.method == "POST":
        form = task_information_form(request.POST, request.FILES)
        if form.is_valid():
            # Extract all the information from the form and save
            task_results.task_short_description = form.cleaned_data['task_short_description']
            task_results.task_long_description = form.cleaned_data['task_long_description']

            # Calendar values
            task_results.task_start_date = time_combined(
                int(form.cleaned_data['start_date_year']),
                int(form.cleaned_data['start_date_month']),
                int(form.cleaned_data['start_date_day']),
                int(form.cleaned_data['start_date_hour']),
                int(form.cleaned_data['start_date_minute']),
                form.cleaned_data['start_date_meridiems']
            )
            task_results.task_end_date = time_combined(
                int(form.cleaned_data['finish_date_year']),
                int(form.cleaned_data['finish_date_month']),
                int(form.cleaned_data['finish_date_day']),
                int(form.cleaned_data['finish_date_hour']),
                int(form.cleaned_data['finish_date_minute']),
                form.cleaned_data['finish_date_meridiems']
            )

            # Check to make sure the resolve button was hit
            if 'Resolve' in request.POST:
                # Well, we have to now resolve the data
                task_results.task_status = 'Resolved'

            task_results.save()

            if 'add_customer_submit' in request.POST:
                # The user has tried adding a customer
                customer_id = int(request.POST.get("add_customer_select"))

                submit_customer = tasks_customers(
                    tasks_id=tasks.objects.get(pk=task_id),
                    customer_id=customers.objects.get(pk=customer_id),
                    change_user=request.user,
                )
                submit_customer.save()

            if 'add_user_submit' in request.POST:
                user_results = int(request.POST.get("add_user_select"))
                user_instance = auth.models.User.objects.get(pk=user_results)
                submit_associate_user = assigned_users(
                    user_id=user_instance,
                    task_id=tasks.objects.get(tasks_id=task_id),
                    change_user=request.user,
                )
                submit_associate_user.save()

            if 'add_cost_submit' in request.POST:
                # Extract information
                cost_description = form.cleaned_data['cost_description']
                cost_amount = form.cleaned_data['cost_amount']
                # SAve
                submit_cost = costs(
                    cost_description=cost_description,
                    cost_amount=cost_amount,
                    task_id=tasks.objects.get(tasks_id=task_id),
                    change_user=request.user,
                )
                submit_cost.save()

            """
			If the user has submitted a new document. We only upload the document IF and ONLY IF the user
			has selected the "Submit" button on the "New Document" dialog. We do not want to accidently
			upload a document if we hit the "SAVE" button from a different location
			"""
            if 'new_document' in request.POST:
                document = request.FILES.get('document')
                document_description = request.POST.get("document_description")
                document_url_location = request.POST.get("document_url_location")

                parent_folder_id = request.POST.get("parent_folder_id")

                print(parent_folder_id)

                submit_document = documents(
                    #task_id=tasks.objects.get(pk=task_id),
                    document=document,
                    document_description=document_description,
                    document_url_location=document_url_location,
                    change_user=request.user,
                )
                submit_document.save()

                print(parent_folder_id)

                #If the document is under a folder
                if isinstance(parent_folder_id, int):
                    submit_documents_folder = documents_folder(
                        document_key=submit_document,
                        change_user=request.user,
                        folder_id=int(parent_folder_id),
                    )
                    submit_documents_folder.save()


                #Submit the document permissions
                submit_document_permissions = document_permissions(
                    document_key=submit_document,
                    task_id=tasks.objects.get(pk=task_id),
                    change_user=request.user,
                )
                submit_document_permissions.save()

            """
			Fuck - someone wants to create a new folder...
			"""
            if 'new_folder' in request.POST:
                folder_description = form.cleaned_data['folder_description']
                folder_location = request.POST.get("folder_location")

                submit_folder = folders(
                    task_id=tasks.objects.get(pk=task_id),
                    folder_description=folder_description,
                    change_user=request.user,
                )

                try:
                    submit_folder.parent_folder_id = folders.objects.get(
                        folder_id=int(folder_location))
                    submit_folder.save()
                except:
                    submit_folder.save()

            # Now save the new project history.
            task_history_text_results = form.cleaned_data['task_history_text']

            if not task_history_text_results == '':
                current_user = request.user

                task_id_connection = tasks.objects.get(tasks_id=task_id)

                data = tasks_history(
                    tasks_id=task_id_connection,
                    user_id=current_user,
                    task_history=task_history_text_results,
                    user_infomation=current_user.id,
                    change_user=request.user,
                )
                data.save()

    # Obtain required data
    task_history_results = tasks_history.objects.filter(tasks_id=task_id)  # Will need to remove all IS_DELETED=TRUE

    cursor.execute(
        """
        SELECT DISTINCT
          documents.document_key
        , documents.document_description
        , documents.document_url_location
        , documents.document
        , documents_folder.folder_id_id
        
        FROM 
          documents
          LEFT JOIN
                document_permissions
                ON documents.document_key = document_permissions.document_key_id
		LEFT JOIN
				folder
				ON folder.task_id_id = %s
		LEFT JOIN
				documents_folder
				ON documents_folder.folder_id_id = folder.folder_id
				AND documents_folder.document_key_id = documents.document_key

        
        WHERE 1=1
        
        AND document_permissions.task_id_id = %s
        ORDER BY documents.document_description     
        """, [task_id,task_id])
    #documents_results = namedtuplefetchall(cursor)
    documents_results = cursor.fetchall()

    #print(documents_results)

    folders_results = folders.objects.filter(
        task_id=task_id,
        is_deleted='FALSE',
    ).order_by(
        'folder_description'
    )
    costs_results = costs.objects.filter(task_id=task_id, is_deleted='FALSE')

    """
	The 24 hours to 12 hours formula.
	00:00 means that it is 12:00 AM - change required for hour
	01:00 means that it is 01:00 AM - no change required
	12:00 means that it is 12:00 PM - change required for meridiem
	13:00 means that it is 01:00 PM - change required for hour and meridiem
	"""
    start_hour = task_results.task_start_date.hour
    start_meridiem = u'AM'
    if start_hour == 0:
        start_hour = 12
    elif start_hour == 12:
        start_meridiem = u'PM'
    elif start_hour > 12:
        start_hour = start_hour - 12
        start_meridiem = u'PM'

    end_hour = task_results.task_end_date.hour
    end_meridiem = u'AM'
    if end_hour == 0:
        end_hour = 12
    elif end_hour == 12:
        end_meridiem = u'PM'
    elif end_hour > 12:
        end_hour = end_hour - 12
        end_meridiem = u'PM'

    # Setup the initial
    initial = {
        'task_short_description': task_results.task_short_description,
        'task_long_description': task_results.task_long_description,
        'start_date_year': task_results.task_start_date.year,
        'start_date_month': task_results.task_start_date.month,
        'start_date_day': task_results.task_start_date.day,
        'start_date_hour': start_hour,
        'start_date_minute': task_results.task_start_date.minute,
        'start_date_meridiems': start_meridiem,
        'finish_date_year': task_results.task_end_date.year,
        'finish_date_month': task_results.task_end_date.month,
        'finish_date_day': task_results.task_end_date.day,
        'finish_date_hour': end_hour,
        'finish_date_minute': task_results.task_end_date.minute,
        'finish_date_meridiems': end_meridiem,
    }

    # Query the database for associated project information
    cursor = connection.cursor()
    cursor.execute("""
		SELECT 
		  project.project_id
		, project.project_name
		, project.project_end_date
		FROM project
			JOIN project_tasks
			ON project.project_id = project_tasks.project_id
			AND project_tasks.is_deleted = 'FALSE'
			AND project_tasks.task_id = %s
		""", [task_id])
    associated_project_results = namedtuplefetchall(cursor)

    cursor.execute("""
		SELECT DISTINCT
		  customers.customer_first_name
		, customers.customer_last_name
		, tasks_customers.customers_description
		, customers.customer_email
		, customers_campus_information.campus_nickname
		, customers_campus_information.customer_phone
		FROM
		  customers LEFT JOIN 
			(SELECT 
			  * 
			  FROM 
			  customers_campus join organisations_campus 
			  ON customers_campus.campus_id_id = organisations_campus.id) as customers_campus_information
			ON customers.customer_id = customers_campus_information.customer_id_id
		, tasks_customers
		WHERE 1=1
		AND customers.customer_id = tasks_customers.customer_id_id
		AND tasks_customers.tasks_id_id = %s
	""", [task_id])
    tasks_customers_results = namedtuplefetchall(cursor)

    # task_customers_results
    cursor.execute("""
		SELECT DISTINCT 
		  customers.customer_id
		, customers.customer_first_name || ' ' || customers.customer_last_name AS customer_name
		
		FROM
		  tasks 
		, organisations LEFT JOIN customers
			ON organisations.organisations_id = customers.organisations_id_id
		
		WHERE 1=1
		AND tasks.organisations_id_id = organisations.organisations_id
		
		AND customers.customer_id NOT IN (SELECT DISTINCT tasks_customers.customer_id_id
					FROM tasks_customers
					WHERE 1=1
					AND tasks_customers.tasks_id_id = tasks.tasks_id
					AND tasks_customers.is_deleted = 'FALSE')
		
		
		-- LINKS --
		AND organisations.organisations_id = %s
		AND tasks.tasks_id = %s
		-- END LINKS --	
	""", [task_results.organisations_id_id, task_id])
    new_customers_results = namedtuplefetchall(cursor)

    cursor.execute("""
				SELECT DISTINCT
				  auth_user.id
				, auth_user.username
				, auth_user.first_name
				, auth_user.last_name
				, auth_user.first_name || ' ' || auth_user.last_name AS "Name"
				, auth_user.email
				FROM
				  tasks_groups
				, user_groups
				, auth_user

				WHERE 1=1

				--AUTH_USER CONDITIONS
				AND auth_user.is_active=1

				--PROJECT_GROUPS CONDITIONS
				AND tasks_groups.tasks_id_id=%s

				-- JOINS --
				AND tasks_groups.groups_id_id=user_groups.group_id_id
				AND user_groups.username_id=auth_user.id
				-- END JOINS --
			""", [task_id])
    users_results = namedtuplefetchall(cursor)

    assigned_results = assigned_users.objects.filter(task_id=task_id)
    running_total = 0
    # Load the template
    t = loader.get_template('NearBeach/task_information.html')

    # context
    c = {
        'task_results': task_results,
        'task_information_form': task_information_form(initial=initial),
        'associated_project_results': associated_project_results,
        'task_history_results': task_history_results,
        'tasks_customers_results': tasks_customers_results,
        'new_customers_results': new_customers_results,
        'documents_results': simplejson.dumps(documents_results,encoding='utf-8'),
        'folders_results': serializers.serialize('json', folders_results),
        'media_url': settings.MEDIA_URL,
        'users_results': users_results,
        'assigned_results': assigned_results.values(
            'user_id',
            'user_id__username',
            'user_id__first_name',
            'user_id__last_name',
        ).distinct(),
        'costs_results': costs_results,
    }

    return HttpResponse(t.render(c, request))


# Extra functionality
"""
The following function helps change the cursor's results into useable
SQL that the html templates can read.
"""
from collections import namedtuple
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


"""
The following def are designed to help display a customer 404 and 500 pages
"""


def handler404(request):
    response = render_to_response(
        '404.html',
        {},
        context_instance=RequestContext(request)
    )
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response(
        '500.html',
        {},
        context_instance=RequestContext(request)
    )
    response.status_code = 500
    return response



"""
The time converter - we need a function that breaks time up into different segments, and also
combines it back. This is the time converter
"""
def time_combined(year,month,day,hour,minute,meridiem):
    """
    Time is tricky. So I am following the simple rules;
    12:** AM will have the hour changed to 0
    1:** AM will not have the hour changed
    12:** PM will not have the hour changed
    1:** PM will have the hour changed by adding 12

    From these simple points, I have constructed the following
    if statements to take control of the correct hour.
    """
    if meridiem == "AM":
        if hour == 12:
            hour = 0
    else:
        if hour < 12:
            hour = hour + 12



    # Create the final start/end date fields
    return datetime.datetime(
        year,
        month,
        day,
        hour,
        minute
    )
