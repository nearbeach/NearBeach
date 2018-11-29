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
from .misc_functions import *
from .user_permissions import return_user_permission_level
from django.db.models import Sum, Q, Min


"""
@login_required(login_url='login')
def information_project_assigned_users(request, project_id):
    project_groups_results = object_assignment.objects.filter(
        is_deleted="FALSE",
        project_id=project.objects.get(project_id=project_id),
    ).values('group_id_id')

    permission_results = return_user_permission_level(request, project_groups_results,'project')

    if request.method == "POST":
        user_results = int(request.POST.get("add_user_select"))
        user_instance = auth.models.User.objects.get(pk=user_results)
        submit_associate_user = assigned_user(
            user_id=user_instance,
            project_id=project.objects.get(pk=project_id),
            change_user=request.user,
        )
        submit_associate_user.save()

    assigned_results = assigned_user.objects.filter(
        project_id=project_id,
        is_deleted="FALSE",
    )

    users_results = user_group.objects.filter(
        is_deleted="FALSE",
        group_id__in=project_group.objects.filter(
            is_deleted="FALSE",
            project_id=project_id,
        ).values('group_id'))\
        .exclude(username_id__in=assigned_results.values('user_id'))\
        .values(
            'username_id',
            'username',
            'username_id__first_name',
            'username_id__last_name',)\
        .distinct()


    #Load template
    t = loader.get_template('NearBeach/project_information/project_assigned_users.html')

    # context
    c = {
        'users_results': users_results,
        'assigned_results': assigned_results.values(
            'user_id__id',
            'user_id',
            'user_id__username',
            'user_id__first_name',
            'user_id__last_name',
        ).distinct(),
        'project_permissions': permission_results['project'],
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def information_project_delete_assigned_users(request, project_id, location_id):
    assigned_users_save = assigned_user.objects.filter(
        project_id=project_id,
        user_id=location_id,
    )
    assigned_users_save.update(is_deleted="TRUE")

    #Load template
    t = loader.get_template('NearBeach/blank.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))
"""


@login_required(login_url='login')
def information_project_costs(request, project_id):
    project_groups_results = object_assignment.objects.filter(
        is_deleted="FALSE",
        project_id=project.objects.get(project_id=project_id),
    ).values('group_id_id')

    permission_results = return_user_permission_level(request, project_groups_results,'project')

    if request.method == "POST":
        form = information_project_cost_form(request.POST, request.FILES)
        if form.is_valid():
            cost_description = form.cleaned_data['cost_description']
            cost_amount = form.cleaned_data['cost_amount']
            if ((not cost_description == '') and ((cost_amount <= 0) or (cost_amount >= 0))):
                submit_cost = cost(
                    project_id=project.objects.get(pk=project_id),
                    cost_description=cost_description,
                    cost_amount=cost_amount,
                    change_user=request.user,
                )
                submit_cost.save()

    #Get data
    """
    Cost results and running total.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Due to Django not having the ability to have a runnning total, I needed to extract all the costs and manually create
    the running total as a separate array. Now I need to combine both sets of data into one loop. To do that we use a 
    zip function to bring them together. Then we can just use a simple
    for a,b in zip_results
    """
    costs_results = cost.objects.filter(project_id=project_id, is_deleted='FALSE')

    #Get running totals
    running_total = []
    grand_total = 0 #use to calculate the grand total through the look
    for line_item in costs_results:
        grand_total = grand_total + float(line_item.cost_amount)
        running_total.append(grand_total)

    cost_zip_results = zip(costs_results,running_total)

    #Load template
    t = loader.get_template('NearBeach/project_information/project_costs.html')

    # context
    c = {
        'information_project_cost_form': information_project_cost_form(),
        'cost_zip_results':cost_zip_results,
        'project_permissions': permission_results['project'],
        'grand_total': grand_total,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_project_customer(request, project_id):
    project_groups_results = object_assignment.objects.filter(
        is_deleted="FALSE",
        project_id=project.objects.get(project_id=project_id),
    ).values('group_id')

    permission_results = return_user_permission_level(request, project_groups_results,'project')

    if request.method == "POST":
        # The user has tried adding a customer
        customer_id = int(request.POST.get("add_customer_select"))

        submit_customer = project_customer(
            project_id=project.objects.get(pk=project_id),
            customer_id=customer.objects.get(pk=customer_id),
            change_user=request.user,
        )
        submit_customer.save()

    #Get data
    project_results = project.objects.get(project_id=project_id)

    #Obtain a list of customer not already added to this task
    new_customers_results = customer.objects.filter(
        organisation_id=project_results.organisation_id,
        is_deleted="FALSE",
    ).exclude(
        customer_id__in=project_customer.objects.filter(
            project_id=project_results.project_id
        ).values('customer_id')
    )

    project_customers_results = project_customer.objects.filter(
        is_deleted="FALSE",
        project_id=project_id,

    )

    t = loader.get_template('NearBeach/project_information/project_customers.html')

    # context
    c = {
        'project_results': project_results,
        'new_customers_results': new_customers_results,
        'project_customers_results': project_customers_results,
        'project_permissions': permission_results['project'],
    }

    return HttpResponse(t.render(c, request))




@login_required(login_url='login')
def information_project_history(request, project_id):
    project_groups_results = object_assignment.objects.filter(
        is_deleted="FALSE",
        project_id=project.objects.get(project_id=project_id),
    ).values('group_id_id')

    permission_results = return_user_permission_level(request, project_groups_results,['project','project_history'])

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
        'project_history_results': project_history_results,
        'project_id': project_id,
        'project_permissions': permission_results['project'],
        'project_history_permissions': permission_results['project_history'],
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def project_readonly(request, project_id):
    project_groups_results = object_assignment.objects.filter(
        is_deleted="FALSE",
        project_id=project.objects.get(project_id=project_id),
    ).values('group_id_id')

    permission_results = return_user_permission_level(request, project_groups_results, ['project', 'project_history'])

    #Get data
    project_results = project.objects.get(project_id=project_id)
    to_do_results = to_do.objects.filter(
        is_deleted="FALSE",
        project_id=project_id,
    )
    project_history_results = project_history.objects.filter(
        is_deleted="FALSE",
        project_id=project_id,
    )
    email_results = email_content.objects.filter(
        is_deleted="FALSE",
        email_content_id__in=email_contact.objects.filter(
            Q(project=project_id) &
            Q(is_deleted="FALSE") &
            Q(
                Q(is_private=False) |
                Q(change_user=request.user)
            )
        ).values('email_content_id')
    )

    associated_tasks_results = project_task.objects.filter(
        is_deleted="FALSE",
        project_id=project_id,
    )

    project_customers_results = project_customer.objects.filter(
        is_deleted="FALSE",
        project_id=project_id,

    )

    costs_results = cost.objects.filter(
        project_id=project_id,
        is_deleted='FALSE'
    )

    quote_results = quote.objects.filter(
        is_deleted="FALSE",
        project_id=project_id,
    )

    bug_results = bug.objects.filter(
        is_deleted="FALSE",
        project_id=project_id,
    )

    assigned_results = assigned_user.objects.filter(
        project_id=project_id,
        is_deleted="FALSE",
    ).values(
        'user_id__id',
        'user_id',
        'user_id__username',
        'user_id__first_name',
        'user_id__last_name',
    ).distinct()

    group_list_results = project_group.objects.filter(
        is_deleted="FALSE",
        project_id=project_id,
    )

    """
    We want to bring through the project history's tinyMCE widget as a read only. However there are 
    most likely multiple results so we will create a collective.
    """
    project_history_collective =[]
    for row in project_history_results:
        #First deal with the datetime
        project_history_collective.append(
            project_history_readonly_form(
                initial={
                    'project_history': row.project_history,
                    'submit_history': row.user_infomation + " - " + str(row.user_id) + " - "\
                                      + row.date_created.strftime("%d %B %Y %H:%M.%S"),
                },
                project_history_id=row.project_history_id,
            )
        )


    #Get Template
    t = loader.get_template('NearBeach/project_information/project_readonly.html')

    # context
    c = {
        'project_id': project_id,
        'project_results': project_results,
        'project_readonly_form': project_readonly_form(
            initial={'project_description': project_results.project_description}
        ),
        'to_do_results': to_do_results,
        'project_history_collective': project_history_collective,
        'email_results': email_results,
        'associated_tasks_results': associated_tasks_results,
        'project_customers_results': project_customers_results,
        'costs_results': costs_results,
        'quote_results': quote_results,
        'bug_results': bug_results,
        'assigned_results': assigned_results,
        'group_list_results': group_list_results,
        'project_permissions': permission_results['project'],
        'project_history_permissions': permission_results['project_history'],
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],

    }

    return HttpResponse(t.render(c, request))