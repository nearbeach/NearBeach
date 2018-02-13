"""
VIEWS - task information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the TASK INFORMATION MODULES. This is to help keep the VIEWS
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
from .misc_functions import *
from .user_permissions import return_user_permission_level


@login_required(login_url='login')
def information_task_assigned_users(request, task_id):
    task_permissions = 0

    if request.session['is_superuser'] == True:
        task_permissions = 4
    else:
        task_groups_results = tasks_groups.objects.filter(
            is_deleted="FALSE",
            tasks_id=tasks.objects.get(tasks_id=task_id),
        ).values('groups_id_id')

        for row in task_groups_results:
            pp_results = return_user_permission_level(request, row['groups_id_id'],'task')

            if pp_results > task_permissions:
                task_permissions = pp_results

    if request.method == "POST":
        user_results = int(request.POST.get("add_user_select"))
        user_instance = auth.models.User.objects.get(pk=user_results)
        submit_associate_user = assigned_users(
            user_id=user_instance,
            task_id=tasks.objects.get(tasks_id=task_id),
            change_user=request.user,
        )
        submit_associate_user.save()

    #Get data
    assigned_results = assigned_users.objects.filter(task_id=task_id,is_deleted="FALSE")

    cursor = connection.cursor()
    cursor.execute("""
    				SELECT DISTINCT
    				  auth_user.id
    				, auth_user.username
    				, auth_user.first_name
    				, auth_user.last_name
    				, auth_user.email
    				FROM
    				  tasks_groups
    				, user_groups
    				, auth_user

    				WHERE 1=1

    				-- AUTH_USER CONDITIONS
    				AND auth_user.is_active='1'

    				-- PROJECT_GROUPS CONDITIONS
    				AND tasks_groups.tasks_id_id=%s

    				-- JOINS --
    				AND tasks_groups.groups_id_id=user_groups.groups_id
    				AND user_groups.username_id=auth_user.id
    				-- END JOINS --
    			""", [task_id])
    users_results = namedtuplefetchall(cursor)

    #Load template
    t = loader.get_template('NearBeach/task_information/task_assigned_users.html')

    # context
    c = {
        'users_results': users_results,
        'assigned_results': assigned_results.values(
            'user_id__id',
            'user_id__username',
            'user_id__first_name',
            'user_id__last_name',
        ).distinct(),
        'task_permissions': task_permissions,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_delete_assigned_users(request, task_id, user_id):
    assigned_users_save = assigned_users.objects.filter(
        task_id=task_id,
        user_id=user_id,
    )
    assigned_users_save.update(is_deleted="TRUE")

    #Load template
    t = loader.get_template('NearBeach/blank.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_costs(request, task_id):
    task_permissions = 0

    if request.session['is_superuser'] == True:
        task_permissions = 4
    else:
        task_groups_results = tasks_groups.objects.filter(
            is_deleted="FALSE",
            tasks_id=tasks.objects.get(tasks_id=task_id),
        ).values('groups_id_id')

        for row in task_groups_results:
            pp_results = return_user_permission_level(request, row['groups_id_id'],'task')

            if pp_results > task_permissions:
                task_permissions = pp_results

    # Get the data from the form
    if request.method == "POST":
        form = information_task_costs_form(request.POST, request.FILES)
        if form.is_valid():
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

    #Get data
    task_results = tasks.objects.get(tasks_id=task_id)
    costs_results = costs.objects.filter(task_id=task_id, is_deleted='FALSE')

    #Load template
    t = loader.get_template('NearBeach/task_information/task_costs.html')

    # context
    c = {
        'costs_results': costs_results,
        'information_task_costs_form': information_task_costs_form(),
        'task_id': task_id,
        'task_permissions': task_permissions,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_customers(request, task_id):
    task_permissions = 0

    if request.session['is_superuser'] == True:
        task_permissions = 4
    else:
        task_groups_results = tasks_groups.objects.filter(
            is_deleted="FALSE",
            tasks_id=tasks.objects.get(tasks_id=task_id),
        ).values('groups_id_id')

        for row in task_groups_results:
            pp_results = return_user_permission_level(request, row['groups_id_id'],'task')

            if pp_results > task_permissions:
                task_permissions = pp_results

    if request.method == "POST":
        # The user has tried adding a customer
        customer_id = int(request.POST.get("add_customer_select"))

        submit_customer = tasks_customers(
            tasks_id=tasks.objects.get(pk=task_id),
            customer_id=customers.objects.get(pk=customer_id),
            change_user=request.user,
        )
        submit_customer.save()

    #Get Data
    task_results = tasks.objects.get(tasks_id=task_id)

    #Obtain a list of customers not already added to this task
    new_customers_results = customers.objects.filter(
        organisations_id=task_results.organisations_id,
        is_deleted="FALSE",
    ).exclude(
        customer_id__in=tasks_customers.objects.filter(tasks_id=task_results.tasks_id).values('customer_id')
    )

    # task_customers_results
    cursor = connection.cursor()
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
    			(SELECT customers_campus_id, customer_phone, customer_fax, campus_id_id, customer_id_id, organisations_campus_id, campus_nickname, campus_phone, campus_fax, campus_address1, campus_address2, campus_address3, campus_suburb, campus_country_id_id, campus_region_id_id, organisations_id_id FROM customers_campus join organisations_campus ON customers_campus.campus_id_id = organisations_campus.organisations_campus_id ) as customers_campus_information
    			ON customers.customer_id = customers_campus_information.customer_id_id
    		, tasks_customers
    		WHERE 1=1
    		AND customers.customer_id = tasks_customers.customer_id_id
    		AND tasks_customers.tasks_id_id = %s
    	""", [task_id])
    tasks_customers_results = namedtuplefetchall(cursor)

    #Load template
    t = loader.get_template('NearBeach/task_information/task_customers.html')

    # context
    c = {
        'task_results': task_results,
        'new_customers_results': new_customers_results,
        'tasks_customers_results': tasks_customers_results,
        'task_permissions': task_permissions,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_history(request, task_id):
    task_permissions = 0
    task_history_permissions = 0

    if request.session['is_superuser'] == True:
        task_permissions = 4
        task_history_permissions = 4
    else:
        task_groups_results = tasks_groups.objects.filter(
            is_deleted="FALSE",
            tasks_id=tasks.objects.get(tasks_id=task_id),
        ).values('groups_id_id')

        for row in task_groups_results:
            pp_results = return_user_permission_level(request, row['groups_id_id'],'task')
            ph_results = return_user_permission_level(request, row['groups_id_id'],'task_history')

            if pp_results > task_permissions:
                task_permissions = pp_results

            if ph_results > task_history_permissions:
                task_history_permissions = ph_results

    # Get the data from the form
    if request.method == "POST":
        form = information_task_history_form(request.POST, request.FILES)
        if form.is_valid():
            # Now save the new project history.
            task_history_results = form.cleaned_data['task_history']

            if not task_history_results == '':
                current_user = request.user

                task_id_connection = tasks.objects.get(tasks_id=task_id)

                data = tasks_history(
                    tasks_id=task_id_connection,
                    user_id=current_user,
                    task_history=task_history_results,
                    user_infomation=current_user.id,
                    change_user=request.user,
                )
                data.save()

    #Get data
    task_history_results = tasks_history.objects.filter(
        tasks_id=task_id,
        is_deleted='FALSE',
    )

    #Load template
    t = loader.get_template('NearBeach/task_information/task_history.html')

    # context
    c = {
        'information_task_history_form': information_task_history_form(),
        'task_history_results': task_history_results,
        'task_permissions': task_permissions,
        'task_history_permissions': task_history_permissions,
    }

    return HttpResponse(t.render(c, request))



