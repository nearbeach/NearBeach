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
from .namedtuplefetchall import *


@login_required(login_url='login')
def information_task_assigned_users(request, task_id):
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
    assigned_results = assigned_users.objects.filter(task_id=task_id)

    cursor = connection.cursor()
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

    #Load template
    t = loader.get_template('NearBeach/task_information/task_assigned_users.html')

    # context
    c = {
        'users_results': users_results,
        'assigned_results': assigned_results.values(
            'user_id',
            'user_id__username',
            'user_id__first_name',
            'user_id__last_name',
        ).distinct(),
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_costs(request, task_id):
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
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_customers(request, task_id):
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

    # task_customers_results
    cursor = connection.cursor()
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

    #Load template
    t = loader.get_template('NearBeach/task_information/task_customers.html')

    # context
    c = {
        'task_results': task_results,
        'new_customers_results': new_customers_results,
        'tasks_customers_results': tasks_customers_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_history(request, task_id):
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
    }

    return HttpResponse(t.render(c, request))



