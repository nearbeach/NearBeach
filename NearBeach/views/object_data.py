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
    submit_bug = set_object_from_destination(submit_bug,destination,location_id)

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
    submit_object_assignment = set_object_from_destination(
        submit_object_assignment,
        destination,
        location_id
    )

    # Save the data
    submit_object_assignment.save()

    customer_results = get_customer_list(destination, location_id)

    return HttpResponse(serializers.serialize('json', customer_results), content_type='application/json')

@login_required(login_url='login',redirect_field_name="")
def add_notes(request,destination,location_id):
    # Checks that this is done in POST
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - this needs to be in post")

    # ADD IN PERMISSIONS HERE!

    # Fill out the form
    form = AddNoteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # SAVE DATA
    submit_object_note = object_note(
        change_user = request.user,
        object_note = form.cleaned_data['note']
    )
    submit_object_note = set_object_from_destination(
        submit_object_note,
        destination,
        location_id
    )

    submit_object_note.save()

    # Get data to send back to user
    note_resuts = object_note.objects.filter(object_note_id=submit_object_note.object_note_id)

    return HttpResponse(serializers.serialize('json',note_resuts),content_type='application.json')


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
    bug_list = bug.objects.filter(
        is_deleted="FALSE",
    )
    bug_list = get_object_from_destination(bug_list,destination,location_id)

    # Limit to certain values
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

    customer_results = get_customer_list(destination, location_id)

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
def get_customer_list(destination,location_id):
    # Get a list of all objects assignments dependant on the destination
    object_customers = object_assignment.objects.filter(
        is_deleted="FALSE",
        customer_id__isnull=False,
    )
    object_customers = get_object_from_destination(object_customers,destination,location_id)

    return customer.objects.filter(
        is_deleted="FALSE",
        customer_id__in=object_customers.values('customer_id')
    )

# Internal function
def get_object_from_destination(input_object,destination,location_id):
    """
    To stop the repeat code of finding specific objects using destination and location_id - we will import
    the object filter for it here - before returning it.
    :param object: The object we want to filter
    :param destination: The destination we are interested in
    :param location_id: The location_id
    :return:
    """
    if destination == "requirement":
        input_object = input_object.filter(
            requirement_id=location_id,
        )
    elif destination == "project":
        input_object = input_object.filter(
            project_id=location_id,
        )
    elif destination == "task":
        input_object = input_object.filter(
            task_id=location_id,
        )

    # Just send back the array
    return input_object


@login_required(login_url='login',redirect_field_name="")
def group_list(request,destination,location_id):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through post")

    # Get the data dependant on the object lookup
    object_results = object_assignment.objects.filter(
        is_deleted="FALSE",
    )
    object_results = get_object_from_destination(
        object_results,
        destination,
        location_id
    )

    # Now get the groups
    group_results = group.objects.filter(
        is_deleted="FALSE",
        group_id__in=object_results.values('group_id')
    )

    # Return the data
    return HttpResponse(serializers.serialize('json',group_results),content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def group_list_all(request,destination,location_id):
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - this request needs to be done through post")

    # ADD CHECKS FOR USER PERMISSIONS!

    # Obtain data
    group_existing_results = object_assignment.objects.filter(
        is_deleted="FALSE",
        group_id__isnull=False,
    )
    group_existing_results = get_object_from_destination(group_existing_results,destination,location_id)

    group_results = group.objects.filter(
        is_deleted="FALSE",
    ).exclude(
        group_id__in=group_existing_results.values('group_id')
    )

    # Return data as json
    return HttpResponse(serializers.serialize('json',group_results),content_type='application/json')

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
def note_list(request,destination,location_id):
    # Check to make sure method is POST
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - you need to do this as a POST")

    # Everyone should have access to the notes section.

    # Get the notes dependent on the user destination and location
    note_results = object_note.objects.filter(
        is_deleted="FALSE",
    )

    # Filter by destination and location_id
    note_results = get_object_from_destination(note_results,destination,location_id)

    # Return JSON results
    return HttpResponse(serializers.serialize('json',note_results),content_type='application/json')


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
    existing_bugs = get_object_from_destination(existing_bugs,destination,location_id)

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


# Internal function
def set_object_from_destination(input_object,destination,location_id):
    """
    This function is used to set data against an object using the destination and location data.
    :param input_object: The input object that we are setting data for
    :param destination: The destination we are interested in
    :param location_id: The location we are interested in
    :return:
    """
    if destination == "project":
        input_object.project = project.objects.get(project_id=location_id)
    elif destination == "task":
        input_object.task = task.objects.get(task_id=location_id)
    elif destination == "requirement":
        input_object.requirement = requirement.objects.get(requirement_id=location_id)

    # Return what we have
    return input_object

@login_required(login_url='login',redirect_field_name="")
def user_list(request,destination,location_id):
    # Make sure it is in post
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - needs to be in POST")

    # Get the data we want
    object_results = object_assignment.objects.filter(
        is_deleted="FALSE",
        assigned_user_id__isnull=False,
    )
    object_results = get_object_from_destination(
        object_results,
        destination,
        location_id
    )

    # Get the user details
    user_results = User.objects.filter(id__in=object_results.values('assigned_user_id'))

    return HttpResponse(serializers.serialize('json',user_results),content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def user_list_all(request,destination,location):
    # Make sure it is in post
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - needs to be in POST")

    # ADD IN PERMISSIONS LATER

    # Get exclusion list first
    user_exclude = object_assignment.objects.filter(
        is_deleted="FALSE",
        assigned_user__isnull=False,
    )
    user_exclude = get_object_from_destination(user_exclude, destination, location)

    # Limit to these groups
    group_results = object_assignment.objects.filter(
        is_deleted="FALSE",
        group_id__isnull=False,
    )
    group_results = get_object_from_destination(group_results, destination, location)

    # Extract the users connected to the list
    return HttpResponse("WILL DO THIS TOMORROW")