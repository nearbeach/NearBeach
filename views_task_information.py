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
    task_groups_results = task_group.objects.filter(
        is_deleted="FALSE",
        task_id=task.objects.get(task_id=task_id),
    ).values('group_id_id')

    permission_results = return_user_permission_level(request, task_groups_results,'task')

    if request.method == "POST":
        user_results = int(request.POST.get("add_user_select"))
        user_instance = auth.models.User.objects.get(pk=user_results)
        submit_associate_user = assigned_user(
            user_id=user_instance,
            task_id=task.objects.get(task_id=task_id),
            change_user=request.user,
        )
        submit_associate_user.save()

    #Get data
    assigned_results = assigned_user.objects.filter(task_id=task_id, is_deleted="FALSE")

    users_results = user_group.objects.filter(
        is_deleted="FALSE",
        group_id__in=task_group.objects.filter(
            is_deleted="FALSE",
            task_id=task_id,
        ).values('group_id')) \
        .exclude(username_id__in=assigned_results.values('user_id')) \
        .values(
        'username_id',
        'username',
        'username_id__first_name',
        'username_id__last_name', ) \
        .distinct()

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
        'task_permissions': permission_results['task'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_delete_assigned_users(request, task_id, user_id):
    assigned_users_save = assigned_user.objects.filter(
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
    task_groups_results = task_group.objects.filter(
        is_deleted="FALSE",
        task_id=task.objects.get(task_id=task_id),
    ).values('group_id_id')

    permission_results = return_user_permission_level(request, task_groups_results,'task')

    # Get the data from the form
    if request.method == "POST":
        form = information_task_cost_form(request.POST, request.FILES)
        if form.is_valid():
            # Extract information
            cost_description = form.cleaned_data['cost_description']
            cost_amount = form.cleaned_data['cost_amount']
            # SAve
            submit_cost = cost(
                cost_description=cost_description,
                cost_amount=cost_amount,
                task_id=task.objects.get(task_id=task_id),
                change_user=request.user,
            )
            submit_cost.save()

    #Get data
    task_results = task.objects.get(task_id=task_id)

    """
    Cost results and running total.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Due to Django not having the ability to have a runnning total, I needed to extract all the costs and manually create
    the running total as a separate array. Now I need to combine both sets of data into one loop. To do that we use a 
    zip function to bring them together. Then we can just use a simple
    for a,b in zip_results
    """
    costs_results = cost.objects.filter(task_id=task_id, is_deleted='FALSE')

    running_total = []
    grand_total = 0 #Used to calculate the grand total in the loop
    for line_item in costs_results:
        grand_total = grand_total + float(line_item.cost_amount)
        running_total.append(grand_total)

    cost_zip_results = zip(costs_results, running_total)

    #Load template
    t = loader.get_template('NearBeach/task_information/task_costs.html')

    # context
    c = {
        'cost_zip_results': cost_zip_results,
        'grand_total': grand_total,
        'information_task_cost_form': information_task_cost_form(),
        'task_id': task_id,
        'task_permissions': permission_results['task'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_customer(request, task_id):
    task_groups_results = task_group.objects.filter(
        is_deleted="FALSE",
        task_id=task.objects.get(task_id=task_id),
    ).values('group_id_id')

    permission_results = return_user_permission_level(request, task_groups_results,'task')

    if request.method == "POST":
        # The user has tried adding a customer
        customer_id = int(request.POST.get("add_customer_select"))

        submit_customer = task_customer(
            task_id=task.objects.get(pk=task_id),
            customer_id=customer.objects.get(pk=customer_id),
            change_user=request.user,
        )
        submit_customer.save()

    #Get Data
    task_results = task.objects.get(task_id=task_id)

    #Obtain a list of customer not already added to this task
    new_customers_results = customer.objects.filter(
        organisation_id=task_results.organisation_id,
        is_deleted="FALSE",
    ).exclude(
        customer_id__in=task_customer.objects.filter(task_id=task_results.task_id).values('customer_id')
    )

    task_customers_results=task_customer.objects.filter(
        is_deleted="FALSE",
        task_id=task_id
    )

    #Load template
    t = loader.get_template('NearBeach/task_information/task_customers.html')

    # context
    c = {
        'task_results': task_results,
        'new_customers_results': new_customers_results,
        'task_customers_results': task_customers_results,
        'task_permissions': permission_results['task'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_history(request, task_id):
    task_groups_results = task_group.objects.filter(
        is_deleted="FALSE",
        task_id=task.objects.get(task_id=task_id),
    ).values('group_id_id')

    permission_results = return_user_permission_level(request, task_groups_results,['task','task_history'])


    # Get the data from the form
    if request.method == "POST":
        form = information_task_history_form(request.POST, request.FILES)
        if form.is_valid():
            # Now save the new project history.
            task_history_results = form.cleaned_data['task_history']

            if not task_history_results == '':
                current_user = request.user

                task_id_connection = task.objects.get(task_id=task_id)

                data = task_history(
                    task_id=task_id_connection,
                    user_id=current_user,
                    task_history=task_history_results,
                    user_infomation=current_user.id,
                    change_user=request.user,
                )
                data.save()

    #Get data
    task_history_results = task_history.objects.filter(
        task_id=task_id,
        is_deleted='FALSE',
    )

    #Load template
    t = loader.get_template('NearBeach/task_information/task_history.html')

    # context
    c = {
        'task_history_results': task_history_results,
        'task_permissions': permission_results['task'],
        'task_history_permissions': permission_results['task_history'],
    }

    return HttpResponse(t.render(c, request))



