from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.user_permissions import return_user_permission_level

import json

@login_required(login_url='login',redirect_field_name="")
def bug_list(request,destination,location_id):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through psot")

    # Obtain the data dependent on the destination
    if destination == "project":
        bug_list = bug.objects.filter(
            is_deleted="FALSE",
            project_id=location_id,
        )
    elif destination == "requirement":
        bug_list = bug.objects.filter(
            is_deleted="FALSE",
            requirement_id=location_id,
        )
    elif destination ==  "task":
        bug_list = bug.objects.filter(
            is_deleted="FALSE",
            task_id=location_id,
        )
    else:
        # Oh there was an issue
        return HttpResponseBadRequest("Sorry - there was an issue getting the bugs")

    bug_list = bug_list.values(
        'bug_client',
        'bug_client__list_of_bug_client',
        'bug_client__bug_client_name',
        'bug_client__bug_client_url',
        'bug_code',
        'bug_description',
        'bug_status',
        "project_id",
        "requirement_id",
        "task_id",
    )

    """
    As explained on stack overflow here - https://stackoverflow.com/questions/7650448/django-serialize-queryset-values-into-json#31994176
    We need to Django's serializers can't handle a ValuesQuerySet. However, you can serialize by using a standard 
    json.dumps() and transforming your ValuesQuerySet to a list by using list().[sic]
    """

    # Send back json data
    json_results = json.dumps(list(bug_list), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def customer_list(request,destination,location_id):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through psot")

    # Get a list of all objects assignments dependant on the destination
    if destination == "requirement":
        object_customers = object_assignment.objects.filter(
            is_deleted="FALSE",
            customer_id__isnull=False,
            requirement_id=location_id,
        )
    elif destination == "project":
        object_customers = object_assignment.objects.filter(
            is_deleted="FALSE",
            customer_id__isnull=False,
            project_id=location_id,
        )
    elif destination == "task":
        object_customers = object_assignment.objects.filter(
            is_deleted="FALSE",
            customer_id__isnull=False,
            task_id=location_id,
        )
    else:
        # There is no destination that could match this. Send user to errors
        return HttpResponseBadRequest("Sorry - there was an error getting the Customer List")

    customer_results = customer.objects.filter(
        is_deleted="FALSE",
        customer_id__in=object_customers.values('customer_id')
    )

    return HttpResponse(serializers.serialize('json',customer_results), content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def link_list(request,destination,location_id,object_lookup):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through post")

    # Get the data dependent on the object lookup
    if object_lookup == 'project':
        data_results = project.objects.filter(
            is_deleted="FALSE",
        ).exclude(
            project_status='Closed',
        )
    elif object_lookup == "task":
        data_results = task.objects.filter(
            is_deleted="FALSE",
        ).exclude(
            task_status='Closed',
        )
    elif object_lookup == "opportunity":
        data_results = opportunity.objects.filter(
            is_deleted="FALSE",
            opportunity_stage_id__opportunity_closed="FALSE",
        )
    else:
        # There is an error.
        return HttpResponseBadRequest("Sorry - but that object lookup does not exist")

    # Send the data to the user
    return HttpResponse(serializers.serialize('json',data_results), content_type='application/json')
