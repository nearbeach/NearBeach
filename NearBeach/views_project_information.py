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


@login_required(login_url='login',redirect_field_name="")
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
            is_deleted="FALSE",
            project_id=project_results.project_id,
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




@login_required(login_url='login',redirect_field_name="")
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



