import urllib

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


import json, urllib3

@login_required(login_url='login',redirect_field_name="")
def add_bug(request,destination,location_id):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through psot")

    #ADD IN CHECK PERMISSIONS THAT USES THE DESTINATION AND LOCATION!

    # Get data from form
    form = AddBugForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    submit_bug = bug(
        bug_client=form.cleaned_data['bug_client'],
        bug_code=form.cleaned_data['bug_id'],
        bug_description=form.cleaned_data['bug_description'],
        bug_status=form.cleaned_data['bug_status'],
        change_user=request.user,
    )

    # Connect to the correct destination
    if destination == "project":
        submit_bug.project_id = location_id
    elif destination == "task":
        submit_bug.task_id = location_id
    elif destination == "requirement":
        submit_bug.requirement_id = location_id
    else:
        return HttpResponseBadRequest("Sorry - something went wrong")

    # Save
    submit_bug.save()

    # Get new bug to send back to use
    bug_results = bug.objects.filter(bug_id=submit_bug.bug_id)

    # Return the JSON data
    return HttpResponse(serializers.serialize('json',bug_results),content_type='application/json')



@login_required(login_url='login',redirect_field_name="")
def add_customer(request,destination,location_id):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through psot")

    #ADD IN CHECK PERMISSIONS THAT USES THE DESTINATION AND LOCATION!

    # Get data from form
    form = AddCustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Obtain the data dependent on the destination
    submit_object_assignment = object_assignment(
        change_user=request.user,
        customer=form.cleaned_data['customer']
    )
    if destination == "project":
        submit_object_assignment.project_id=project.objects.get(project_id=location_id)
    elif destination == "requirement":
        submit_object_assignment.requirement_id=requirement.objects.get(requirement_id=location_id)
    elif destination == "task":
        submit_object_assignment.task_id=task.objects.get(task_id=location_id)
    else:
        # Oh there was an issue
        return HttpResponseBadRequest("Sorry - there was an issue getting the bugs")

    # Save the data
    submit_object_assignment.save()

    customer_results = get_customer_list(request, destination, location_id)

    return HttpResponse(serializers.serialize('json', customer_results), content_type='application/json')

@login_required(login_url='login',redirect_field_name="")
def bug_client_list(request):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through post")

    bug_client_results = bug_client.objects.filter(
        is_deleted="FALSE",
    )

    return HttpResponse(serializers.serialize('json',bug_client_results), content_type='application/json')

@login_required(login_url='login',redirect_field_name="")
def bug_list(request,destination,location_id):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through post")

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
        return HttpResponseBadRequest("Sorry - needs to be done through post")

    customer_results = get_customer_list(request, destination, location_id)

    return HttpResponse(serializers.serialize('json', customer_results), content_type='application/json')

@login_required(login_url='login',redirect_field_name="")
def customer_list_all(request,destination,location_id):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through POST")

    # Get the organisation dependant on the destination source
    if destination == "requirement":
        organisation_results = organisation.objects.get(
            organisation_id=requirement.objects.get(
                is_deleted="FALSE",
                requirement_id=location_id,
            ).organisation_id
        )
    elif destination == "project":
        organisation_results = organisation.objects.get(
            organisation_id=project.objects.get(
                is_deleted="FALSE",
                project_id=location_id,
            ).organisation_id
        )
    elif destination == "task":
        organisation_results = organisation.objects.get(
            organisation_id=task.objects.get(
                is_deleted="FALSE",
                task_id=location_id,
            )
        )
    else:
        # There is no destination that could match this. Send user to errors
        return HttpResponseBadRequest("Sorry - there was an error getting the Customer List")

    customer_results = customer.objects.filter(
        is_deleted="FALSE",
        organisation_id=organisation_results.organisation_id
    )

    return HttpResponse(serializers.serialize('json',customer_results), content_type='application/json')

# Internal function
def get_customer_list(request,destination,location_id):
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

    return customer.objects.filter(
        is_deleted="FALSE",
        customer_id__in=object_customers.values('customer_id')
    )




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


@login_required(login_url='login',redirect_field_name="")
def query_bug_client(request,destination,location_id):
    # Check to make sure method is POST
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - you need to do this as a POST")

    # Insert data into form
    form = QueryBugClientForm(request.POST)

    # Check to make sure everything is fine with the form
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extract the information from the form
    bug_client_instance = form.cleaned_data['bug_client_id']
    search_terms = form.cleaned_data['search']

    # Get existing bugs that we want to extract out
    existing_bugs = bug.objects.filter(
        is_deleted="FALSE",
        bug_client_id=bug_client_instance.bug_client_id,
    )

    if destination == "project":
        existing_bugs = existing_bugs.filter(
            project_id=location_id,
        )
    elif destination == "task":
        existing_bugs = existing_bugs.filter(
            task_id=location_id,
        )
    elif destination == "requirement":
        existing_bugs = existing_bugs.filter(
            requirement_id=location_id,
        )
    else:
        return HttpResponseBadRequest("Sorry - it looks like that destination does not exist.")

    # The values in the URL
    f_bugs = ''
    o_notequals = ''
    v_values = ''

    # The for loop
    for idx, row in enumerate(existing_bugs):
        nidx = str(idx + 1)
        f_bugs = f_bugs + "&f" + nidx + "=bug_id"
        o_notequals = o_notequals + "&o" + nidx + "=notequals"
        v_values = v_values + "&v" + nidx + "=" + str(row.bug_code)

    exclude_url = f_bugs + o_notequals + v_values

    url = bug_client_instance.bug_client_url \
          + bug_client_instance.list_of_bug_client.bug_client_api_url \
          + bug_client_instance.list_of_bug_client.api_search_bugs \
          + urllib.parse.quote(form.cleaned_data['search']) \
          + exclude_url

    """
    SECURITY ISSUE
    ~~~~~~~~~~~~~~
    The URL could contain a file. Which we do not want executed by mistake. So we just make sure that the URL starts
    with a http instead of ftp or file.

    We place the  at the end of the json_data because we have checked the field. This should be just a json 
    response. If it is not at this point then it will produce a server issue.
    """
    if url.lower().startswith('http'):
        # setup the pool manager for urllib3
        http = urllib3.PoolManager()

        # Plug in the url
        r = http.request('GET',url)

        # Extract the data
        json_data = json.loads(r.data.decode('utf-8'))
    else:
        raise ValueError from None

    # Send back the JSON data
    return JsonResponse(json_data['bugs'], safe=False)