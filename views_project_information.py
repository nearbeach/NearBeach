"""
VIEWS - project information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the PROJECT INFORMATION MODULES. This is to help keep the VIEWS
file clean from AJAX (spray and wipe).
"""

from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import  loader
from NearBeach.forms import *
from .models import *
from .namedtuplefetchall import *
from .user_permissions import return_user_permission_level


@login_required(login_url='login')
def information_project_assigned_users(request, project_id):
    project_permissions = 0

    if request.session['is_superuser'] == True:
        project_permissions = 4
    else:
        project_groups_results = project_groups.objects.filter(
            is_deleted="FALSE",
            project_id=project.objects.get(project_id=project_id),
        ).values('groups_id_id')

        for row in project_groups_results:
            pp_results = return_user_permission_level(request, row['groups_id_id'],'project')

            if pp_results > project_permissions:
                project_permissions = pp_results

    if request.method == "POST":
        user_results = int(request.POST.get("add_user_select"))
        user_instance = auth.models.User.objects.get(pk=user_results)
        submit_associate_user = assigned_users(
            user_id=user_instance,
            project_id=project.objects.get(pk=project_id),
            change_user=request.user,
        )
        submit_associate_user.save()

    #Get data
    cursor = connection.cursor()

    cursor.execute("""
    			SELECT DISTINCT
    			  auth_user.id
    			, auth_user.username
    			, auth_user.first_name
    			, auth_user.last_name
    			, auth_user.email
    			FROM
    			  project_groups
    			, user_groups
    			, auth_user

    			WHERE 1=1

    			-- AUTH_USER CONDITIONS
    			AND auth_user.is_active='1' 

    			-- PROJECT_GROUPS CONDITIONS
    			AND project_groups.project_id_id=%s

    			-- JOINS --
    			AND project_groups.groups_id_id=user_groups.groups_id
    			AND user_groups.username_id=auth_user.id
    			-- END JOINS --
    		""", [project_id])
    users_results = namedtuplefetchall(cursor)

    assigned_results = assigned_users.objects.filter(project_id=project_id)

    #Load template
    t = loader.get_template('NearBeach/project_information/project_assigned_users.html')

    # context
    c = {
        'users_results': users_results,
        'assigned_results': assigned_results.values(
            'user_id',
            'user_id__username',
            'user_id__first_name',
            'user_id__last_name',
        ).distinct(),
        'project_permissions': project_permissions,
    }

    return HttpResponse(t.render(c, request))

@login_required(login_url='login')
def information_project_costs(request, project_id):
    project_permissions = 0

    if request.session['is_superuser'] == True:
        project_permissions = 4
    else:
        project_groups_results = project_groups.objects.filter(
            is_deleted="FALSE",
            project_id=project.objects.get(project_id=project_id),
        ).values('groups_id_id')

        for row in project_groups_results:
            pp_results = return_user_permission_level(request, row['groups_id_id'],'project')

            if pp_results > project_permissions:
                project_permissions = pp_results

    if request.method == "POST":
        form = information_project_costs_form(request.POST, request.FILES)
        if form.is_valid():
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

    #Get data
    costs_results = costs.objects.filter(project_id=project_id, is_deleted='FALSE')

    #Load template
    t = loader.get_template('NearBeach/project_information/project_costs.html')

    # context
    c = {
        'information_project_costs_form': information_project_costs_form(),
        'costs_results': costs_results,
        'project_permissions': project_permissions,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_project_customers(request, project_id):
    project_permissions = 0

    if request.session['is_superuser'] == True:
        project_permissions = 4
    else:
        project_groups_results = project_groups.objects.filter(
            is_deleted="FALSE",
            project_id=project.objects.get(project_id=project_id),
        ).values('groups_id_id')

        for row in project_groups_results:
            pp_results = return_user_permission_level(request, row['groups_id_id'],'project')

            if pp_results > project_permissions:
                project_permissions = pp_results

    if request.method == "POST":
        # The user has tried adding a customer
        customer_id = int(request.POST.get("add_customer_select"))

        submit_customer = project_customers(
            project_id=project.objects.get(pk=project_id),
            customer_id=customers.objects.get(pk=customer_id),
            change_user=request.user,
        )
        submit_customer.save()

    #Get data
    project_results = project.objects.get(project_id=project_id)

    #Obtain a list of customers not already added to this task
    new_customers_results = customers.objects.filter(
        organisations_id=project_results.organisations_id,
        is_deleted="FALSE",
    ).exclude(
        customer_id__in=tasks_customers.objects.filter(tasks_id=project_results.project_id).values('customer_id')
    )

    #Cursor for custom SQL :)
    cursor = connection.cursor()
    cursor.execute("""
    		SELECT DISTINCT
    		  customers.customer_id
    		, customers.customer_first_name
    		, customers.customer_last_name
    		, project_customers.customer_description
    		, customers.customer_email
    		, customers_campus_information.campus_nickname
    		, customers_campus_information.customer_phone
    		FROM
    		  customers LEFT JOIN 
    			(SELECT customers_campus_id, customer_phone, customer_fax, campus_id_id, customer_id_id, organisations_campus_id, campus_nickname, campus_phone, campus_fax, campus_address1, campus_address2, campus_address3, campus_suburb, campus_country_id_id, campus_region_id_id, organisations_id_id FROM customers_campus join organisations_campus ON customers_campus.campus_id_id = organisations_campus.organisations_campus_id) as customers_campus_information
    			ON customers.customer_id = customers_campus_information.customer_id_id
    		, project_customers
    		WHERE 1=1
    		AND customers.customer_id = project_customers.customer_id_id
    		AND project_customers.project_id_id = %s
    	""", [project_id])
    project_customers_results = namedtuplefetchall(cursor)

    t = loader.get_template('NearBeach/project_information/project_customers.html')

    # context
    c = {
        'project_results': project_results,
        'new_customers_results': new_customers_results,
        'project_customers_results': project_customers_results,
        'project_permissions': project_permissions,
    }

    return HttpResponse(t.render(c, request))




@login_required(login_url='login')
def information_project_history(request, project_id):
    project_permissions = 0
    project_history_permissions = 0

    if request.session['is_superuser'] == True:
        project_permissions = 4
        project_history_permissions = 4
    else:
        project_groups_results = project_groups.objects.filter(
            is_deleted="FALSE",
            project_id=project.objects.get(project_id=project_id),
        ).values('groups_id_id')

        for row in project_groups_results:
            pp_results = return_user_permission_level(request, row['groups_id_id'],'project')
            ph_results = return_user_permission_level(request, row['groups_id_id'],'project_history')

            if pp_results > project_permissions:
                project_permissions = pp_results

            if ph_results > project_history_permissions:
                project_history_permissions = ph_results

    if request.method == "POST":
        form = information_project_history_form(request.POST, request.FILES)
        if form.is_valid():
            project_history_results = form.cleaned_data['project_history']

            if not project_history_results == '':
                current_user = request.user

                project_id_instance = project.objects.get(pk=project_id)

                data = project_history(
                    project_id=project_id_instance,
                    user_id=current_user,
                    project_history=project_history_results,
                    user_infomation=current_user.id,
                    change_user = request.user,
                )
                data.save()
        else:
            print(form.errors)

    project_history_results = project_history.objects.filter(
        project_id=project_id,
        is_deleted="FALSE",
    )

    t = loader.get_template('NearBeach/project_information/project_history.html')

    # context
    c = {
        'information_project_history_form': information_project_history_form(),
        'project_history_results': project_history_results,
        'project_id': project_id,
        'project_permissions': project_permissions,
        'project_history_permissions': project_history_permissions,
    }

    return HttpResponse(t.render(c, request))



