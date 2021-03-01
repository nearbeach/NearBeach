from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.db.models import Q

# Import Forms
from NearBeach.forms import *

import json


# Internal Function
def get_object_search_data(search_form):
    """
    The following internal function will search the following objects using the form's data;
    - Request for Change
    - Requirements
    - Projects
    - Tasks
    It will combine them into a single JSON array and send back to the previous function
    :param form: Contains all the data we require.
    :return:
    """

    # Get instance data for all objects
    rfc_results = request_for_change.objects.filter(is_deleted=False).values(
        'rfc_id',
        'rfc_title',
        'rfc_status',
    )
    requirement_results = requirement.objects.filter(is_deleted=False).values(
        'requirement_id',
        'requirement_title',
        'requirement_status__requirement_status',
    )
    project_results = project.objects.filter(is_deleted=False).values(
        'project_id',
        'project_name',
        'project_status',
    )
    task_results = task.objects.filter(is_deleted=False).values(
        'task_id',
        'task_short_description',
        'task_status',
    )
    kanban_results = kanban_board.objects.filter(is_deleted=False).values(
        'kanban_board_id',
        'kanban_board_name',
        'kanban_board_status',
    )

    # Check to see if we are searching for closed objects
    include_closed = search_form.cleaned_data['include_closed']

    # If we are NOT including closed - then we will limit to those with status is_deleted=False
    if not include_closed:
        ### NEED TO PROGRAM IN THE REAL CLOSED VALUES!!! ###
        rfc_results = rfc_results.filter(is_deleted=False)
        requirement_results = requirement_results.filter(is_deleted=False)
        project_results = project_results.filter(is_deleted=False)
        task_results = task_results.filter(is_deleted=False)
        kanban_results = kanban_results.filter(is_deleted=False)

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data['search'].split(' '):
        # Update the each instance with the split row results
        rfc_results = rfc_results.filter(
            Q(rfc_title__icontains=split_row)
        )
        requirement_results = requirement_results.filter(
            Q(requirement_title__icontains=split_row)
        )
        project_results = project_results.filter(
            Q(project_name__icontains=split_row)
        )
        task_results = task_results.filter(
            Q(task_short_description__icontains=split_row)
        )
        kanban_results = kanban_results.filter(
            Q(kanban_board_name__icontains=split_row)
        )

        # If the split row is a number - also check against the id
        if split_row.isnumeric():
            rfc_results = rfc_results.filter(
                Q(rfc_id=split_row)
            )
            requirement_results = requirement_results.filter(
                Q(requirement_id=split_row)
            )
            project_results = project_results.filter(
                Q(project_id=split_row)
            )
            task_results = task_results.filter(
                Q(task_id=split_row)
            )
            kanban_results = kanban_results.filter(
                Q(kanban_board_id=split_row)
            )


    # Only have 25 results and order by alphabetical order
    rfc_results.order_by('rfc_title')[:25]
    requirement_results.order_by('requirement_title')[:25]
    project_results.order_by('project_name')[:25]
    task_results.order_by('task_short_description').values()[:25]
    kanban_results.order_by('kanban_board_name').values()[:25]

    """
    The pain point
    ~~~~~~~~~~~~~~
    Due to Django wanting to send converted json data as a string, we have to;
    1. Apply serialisation
    2. Apply a json.loads function
    3. Compile data and send back.
    
    Note to Django developers - there has to be a better way
    """
    rfc_results = json.dumps(list(rfc_results), cls=DjangoJSONEncoder)
    requirement_results = json.dumps(list(requirement_results), cls=DjangoJSONEncoder)
    project_results = json.dumps(list(project_results), cls=DjangoJSONEncoder)
    task_results = json.dumps(list(task_results), cls=DjangoJSONEncoder)
    kanban_results = json.dumps(list(kanban_results), cls=DjangoJSONEncoder)

    # Send back a JSON array with JSON arrays inside
    return {
        'request_for_change': json.loads(rfc_results),
        'requirement': json.loads(requirement_results),
        'project': json.loads(project_results),
        'task': json.loads(task_results),
        'kanban': json.loads(kanban_results),
    }


@login_required(login_url='login',redirect_field_name="")
def search(request):
    """

    :param request:
    :return:
    """
    form = SearchObjectsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Template
    t = loader.get_template('NearBeach/search/search.html')

    # Translate the include closed, from Python Boolean to JavaScript boolean
    if form.cleaned_data['include_closed']: #If exists and true
        include_closed = 'true'
    else:
        include_closed = 'false'

    # Context
    c = {
        'search_input': form.cleaned_data['search'],
        'include_closed': include_closed,
        'search_results': get_object_search_data(form),
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def search_data(request):
    """

    :param request:
    :return:
    """
    # Get the form data
    form = SearchObjectsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Return the JSON data
    return JsonResponse(get_object_search_data(form))


@login_required(login_url='login',redirect_field_name="")
def search_customer(request):
    """

    :param request:
    :return:
    """
    t = loader.get_template('NearBeach/search/search_customers.html')

    # Get the first 50 customers
    customer_results = customer.objects.filter(
        is_deleted=False,
    ).order_by('customer_last_name','customer_first_name')[:50]

    c = {
        'customer_results': serializers.serialize('json',customer_results)
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def search_customer_data(request):
    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    customer_results = customer.objects.filter(is_deleted=False)

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data['search'].split(' '):
        # Update the organisation results SQL
        customer_results = customer_results.filter(
            Q(customer_first_name__icontains=split_row) |
            Q(customer_last_name__icontains=split_row) |
            Q(organisation__organisation_name__icontains=split_row) # Might not work for freelancers
        )

    # Only have 50 results and order by alphabetical order
    customer_results.order_by('customer_last_name','customer_first_name')[:50]

    # Send back json data
    json_results = serializers.serialize('json', customer_results)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def search_group(request):
    """

    :param request:
    :return:
    """

    # ADD IN PERMISSIONS

    # Get template
    t = loader.get_template('NearBeach/search/search_groups.html')

    # Get user data
    group_results = group.objects.filter(
        is_deleted=False,
    ).order_by('group_name')[:25]

    # Get context
    c = {
        'group_results': serializers.serialize('json', group_results),
    }

    return HttpResponse(t.render(c, request))


# @require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def search_group_data(request):
    """

    :param request:
    :return:
    """

    # Obtain form data
    search_form = SearchForm(request.POST)
    if not search_form.is_valid():
        return HttpResponseBadRequest(search_form.errors)

    # Get the base group results
    group_results = group.objects.filter(
        is_deleted=False,
    )

    # Loop through the search results
    for split_row in search_form.cleaned_data['search'].split(' '):
        group_results = group_results.filter(
            group_name__icontains=split_row,
        )

    group_results.order_by('group_name')[:25]

    # Send back json data
    json_results = serializers.serialize('json', group_results)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def search_organisation(request):
    """

    :param request:
    :return:
    """
    t = loader.get_template('NearBeach/search/search_organisations.html')

    # Get the first 25 organisations
    organisation_results = organisation.objects.filter(
        is_deleted=False,
    ).order_by('organisation_name')[:25]

    c = {
        'organisation_results': serializers.serialize('json',organisation_results),
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def search_organisation_data(request):
    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    organisation_results = organisation.objects.filter(is_deleted=False)

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data['search'].split(' '):
        # Update the organisation results SQL
        organisation_results = organisation_results.filter(
            organisation_name__icontains=split_row
        )

    # Only have 25 results and order by alphabetical order
    organisation_results = organisation_results.order_by('organisation_name')[:25]

    # Send back json data
    json_results = serializers.serialize('json', organisation_results)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def search_permission_set(request):
    """

    :param request:
    :return:
    """

    # Add permissions

    # Get template
    t = loader.get_template('NearBeach/search/search_permission_sets.html')

    # Get data
    permission_set_results = permission_set.objects.filter(
        is_deleted=False,
    ).order_by('permission_set_name')[:25]

    # Get context
    c = {
        'permission_set_results': serializers.serialize('json', permission_set_results),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def search_permission_set_data(request):
    """

    :param request:
    :return:
    """

    # Check user permission

    # Get form data
    search_form = SearchForm(request.POST)
    if not search_form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get base data
    permission_set_results = permission_set.objects.filter(
        is_deleted=False,
    )

    # Loop through the search results
    for split_row in search_form.cleaned_data['search'].split(' '):
        permission_set_results = permission_set_results.filter(
            permission_set_name__icontains=split_row,
        )

    permission_set_results.order_by('permission_set_name')[:25]

    # Send back json data
    json_results = serializers.serialize('json', permission_set_results)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def search_user(request):
    """

    :param request:
    :return:
    """

    # Add permissions

    # Get template
    t = loader.get_template('NearBeach/search/search_users.html')

    # Get Data
    user_results = User.objects.filter(
    ).order_by('last_name','first_name')[:50]

    # Context
    c = {
        'user_results': serializers.serialize('json', user_results),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def search_user_data(request):
    # Get the data from request
    search_form = SearchForm(request.POST)

    # If there are errors - send 500
    if not search_form.is_valid():
        return HttpResponseBadRequest("There is an issue with the search functionality")

    # Get the base results
    user_results = User.objects.filter()

    # Split the space results - then apply the filter of each split value
    for split_row in search_form.cleaned_data['search'].split(' '):
        # Update the organisation results SQL
        user_results = user_results.filter(
            Q(first_name__icontains=split_row) |
            Q(last_name__icontains=split_row) |
            Q(username__icontains=split_row) |
            Q(email__icontains=split_row)
        )

    # Only have 50 results and order by alphabetical order
    user_results.order_by('last_name','first_name')[:50]

    # Send back json data
    json_results = serializers.serialize('json', user_results)

    return HttpResponse(json_results, content_type='application/json')