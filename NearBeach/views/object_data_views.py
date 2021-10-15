from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum, Q, Min, CharField, Value as V
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from NearBeach.forms import AddBugForm, AddCustomerForm, AddGroupForm, AddObjectLinkForm, AddNoteForm, AddTagsForm, AddUserForm, User, DeleteTagForm, SearchForm, QueryBugClientForm
from NearBeach.views.tools.internal_functions import set_object_from_destination, project, task, requirement, requirement_item, get_object_from_destination, opportunity, organisation
from NearBeach.models import bug, object_assignment, group, object_note, tag, tag_assignment, permission_set, bug_client, customer, user_group, list_of_requirement_status, list_of_requirement_item_status


import json
import urllib
import urllib3

@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_bug(request, destination, location_id):
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
    submit_bug = set_object_from_destination(submit_bug, destination, location_id)

    # Save
    submit_bug.save()

    # Get new bug to send back to use
    bug_results = bug.objects.filter(bug_id=submit_bug.bug_id)

    # Return the JSON data
    return HttpResponse(serializers.serialize('json', bug_results), content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_customer(request, destination, location_id):
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


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_group(request, destination, location_id):
    # ADD IN CHECK PERMISSIONS THAT USES THE DESTINATION AND LOCATION!

    # Get data from form
    form = AddGroupForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # We loop through the responses and add them to the destination's object association
    group_list = request.POST.getlist('group_list')

    for single_group in group_list:
        # Get group instance
        group_instance = group.objects.get(group_id=single_group)

        # Construct the object assignment
        submit_object_assignment = object_assignment(
            group_id=group_instance,
            change_user=request.user,
        )
        submit_object_assignment = set_object_from_destination(submit_object_assignment, destination, location_id)

        # Save the data
        submit_object_assignment.save()

    # Get the new group list data
    group_results = get_group_list(destination, location_id)

    return HttpResponse(serializers.serialize('json', group_results), content_type='application/json')

@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_link(request, destination, location_id):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    # ADD IN CHECKER FOR USER PERMISSIONS

    # Get the data
    form = AddObjectLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Start saving the data
    object_assignment_submit = object_assignment(
        change_user=request.user,
    )

    # Add the destination/location_id to the object
    object_assignment_submit = link_object(object_assignment_submit, destination, location_id)

    # Loop through the results and add them in.
    for row in request.POST.getlist("project"):
        submit_object_assignment = object_assignment(
            project=project.objects.get(project_id=row),
            change_user=request.user,
        )
        set_object_from_destination(submit_object_assignment, destination, location_id)
        submit_object_assignment.save()

    for row in request.POST.getlist("task"):
        submit_object_assignment = object_assignment(
            task=task.objects.get(task_id=row),
            change_user=request.user,
        )
        set_object_from_destination(submit_object_assignment, destination, location_id)
        submit_object_assignment.save()

    for row in request.POST.getlist("requirement"):
        submit_object_assignment = object_assignment(
            requirement=requirement.objects.get(requirement_id=row),
            change_user=request.user,
        )
        set_object_from_destination(submit_object_assignment, destination, location_id)
        submit_object_assignment.save()

    for row in request.POST.getlist("requirement_item"):
        submit_object_assignment = object_assignment(
            requirement_item=requirement_item.objects.get(requirement_item_id=row),
            change_user=request.user,
        )
        set_object_from_destination(submit_object_assignment, destination, location_id)
        submit_object_assignment.save()
    return HttpResponse("Success")

@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_notes(request, destination, location_id):
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

    return HttpResponse(serializers.serialize('json', note_resuts), content_type='application.json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_tags(request, destination, location_id):
    #Check the data against the form
    form = AddTagsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Loop throgh each tag
    tag_list = request.POST.getlist("tag_id")

    for single_tag in tag_list:
        # Grab the tag instance
        tag_instance = tag.objects.get(tag_id=single_tag)

        submit_tag_assignment = tag_assignment(
            tag=tag_instance,
            object_enum=destination,
            object_id=location_id,
            change_user=request.user,
        )
        submit_tag_assignment.save()

    # Return all tags associated with the destination/locationid
    tag_results = tag.objects.filter(
        is_deleted=False,
        tag_id__in=tag_assignment.objects.filter(
            is_deleted=False,
            object_enum=destination,
            object_id=location_id,
        ).values('tag_id')
    )

    return HttpResponse(
        serializers.serialize('json', tag_results),
        content_type='application/json',
    )


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_user(request, destination, location_id):
    # ADD IN A CHECK TO CHECK USER'S PERMISSION!

    # Check the data against the form
    form = AddUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extract the list of users from the POST data
    user_list = request.POST.getlist('user_list')

    # Loop through them and add them to the object assignment
    for single_user in user_list:
        # Get user instance
        user_instance = User.objects.get(id=single_user)

        # Create object assignment
        submit_object_assignment = object_assignment(
            change_user=request.user,
            assigned_user=user_instance,
        )
        submit_object_assignment = set_object_from_destination(submit_object_assignment, destination, location_id)

        # Save
        submit_object_assignment.save()

    # Get the data to return to the user
    user_results = get_user_list(destination, location_id)

    return HttpResponse(user_results, content_type='application/json')

@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def admin_add_user(request):
    """
    :param request:
    :return:
    """
    # Make sure user has permissions
    # Get data
    group_results = group.objects.filter(
        is_deleted=False,
    ).values()

    permission_set_results = permission_set.objects.filter(
        is_deleted=False,
    ).values()

    user_results = User.objects.filter(
        is_active=True,
    ).values()

    # Convert data to json format
    group_results = json.dumps(list(group_results), cls=DjangoJSONEncoder)
    permission_set_results = json.dumps(list(permission_set_results), cls=DjangoJSONEncoder)
    user_results = json.dumps(list(user_results), cls=DjangoJSONEncoder)

    return_data = {
        'group_results': json.loads(group_results),
        'permission_set_results': json.loads(permission_set_results),
        'user_results': json.loads(user_results),
    }

    return JsonResponse(return_data)


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def associated_objects(request, destination, location_id):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    # Organisations have a special method. We will return the results directly from this method to the user.
    if destination == 'organisation':
        return associated_objects_organisations(location_id)

    # Get the data
    object_assignment_results = object_assignment.objects.filter(
        is_deleted=False,
    )
    object_assignment_results = get_object_from_destination(object_assignment_results, destination, location_id)

    opportunity_results = opportunity.objects.filter(
        is_deleted=False,
        opportunity_id__in=object_assignment_results.filter(
            opportunity_id__isnull=False
        ).values('opportunity_id')
    ).values()

    project_results = project.objects.filter(
        is_deleted=False,
        project_id__in=object_assignment_results.filter(
            project_id__isnull=False
        ).values('project_id')
    ).values()

    requirement_results = requirement.objects.filter(
        is_deleted=False,
        requirement_id__in=object_assignment_results.filter(
            requirement_id__isnull=False
        ).values('requirement_id')
    ).values()

    task_results = task.objects.filter(
        is_deleted=False,
        task_id__in=object_assignment_results.filter(
            task_id__isnull=False
        ).values('task_id')
    ).values()

    # Return the JSON Response back - which will return strait to the user
    return JsonResponse({
        'opportunity': list(opportunity_results),
        'project': list(project_results),
        'requirement': list(requirement_results),
        'task': list(task_results),
    })


# Internal Functions
def associated_objects_organisations(location_id):
    """
    Due to organisation's links being connected to the objects directly. We will need to query all the objects that
    can be related to an organisation, and combine them into one JSON output.

    Please note - opportunities are the exception here - hence they are utilising the object assignment table.

    To make it JSON friendly, we have to add .values() to each object lookup, and then simple list them in the JSON
    return function below.
    :param location_id:
    :return:
    """
    # Get the data
    opportunity_results = opportunity.objects.filter(
        is_deleted=False,
        opportunity_id__in=object_assignment.objects.filter(
            is_deleted=False,
            opportunity_id__isnull=False,
            organisation_id=location_id,
        ).values('opportunity_id')
    ).values()

    project_results = project.objects.filter(
        is_deleted=False,
        organisation__in=location_id,
    ).values()

    requirement_results = requirement.objects.filter(
        is_deleted=False,
        organisation__in=location_id,
    ).values()

    task_results = task.objects.filter(
        is_deleted=False,
        organisation__in=location_id,
    ).values()

    # Return the JSON Response back - which will return strait to the user
    return JsonResponse({
        'opportunity': list(opportunity_results),
        'project': list(project_results),
        'requirement': list(requirement_results),
        'task': list(task_results),
    })


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def bug_client_list(request):
    bug_client_results = bug_client.objects.filter(
        is_deleted=False,
    )

    return HttpResponse(serializers.serialize('json', bug_client_results), content_type='application/json')

@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def bug_list(request, destination, location_id):
    # Obtain the data dependent on the destination
    bug_list = bug.objects.filter(
        is_deleted=False,
    )
    bug_list = get_object_from_destination(bug_list, destination, location_id)

    # Limit to certain values
    bug_list = bug_list.values(
        'bug_client',
        'bug_client__list_of_bug_client',
        'bug_client__list_of_bug_client__bug_client_name',
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


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def customer_list(request, destination, location_id):
    customer_results = get_customer_list(destination, location_id)

    return HttpResponse(serializers.serialize('json', customer_results), content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def customer_list_all(request, destination, location_id):
    # Get the organisation dependant on the destination source
    if destination == "requirement":
        organisation_results = organisation.objects.get(
            organisation_id=requirement.objects.get(
                is_deleted=False,
                requirement_id=location_id,
            ).organisation_id
        )
    elif destination == "requirement_item":
        organisation_results = organisation.objects.get(
            organisation_id=requirement.objects.get(
                is_deleted=False,
                requirement_id=requirement_item.objects.get(
                    requirement_item_id=location_id
                ).requirement_id,
            ).organisation_id
        )
    elif destination == "project":
        organisation_results = organisation.objects.get(
            organisation_id=project.objects.get(
                is_deleted=False,
                project_id=location_id,
            ).organisation_id
        )
    elif destination == "task":
        organisation_results = organisation.objects.get(
            organisation_id=task.objects.get(
                is_deleted=False,
                task_id=location_id,
            ).organisation_id
        )
    else:
        # There is no destination that could match this. Send user to errors
        return HttpResponseBadRequest("Sorry - there was an error getting the Customer List")

    customer_results = customer.objects.filter(
        is_deleted=False,
        organisation_id=organisation_results.organisation_id
    )

    return HttpResponse(serializers.serialize('json', customer_results), content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def delete_tag(request):
    # Get form data
    form = DeleteTagForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update/Delete tag associations
    tag_assignment.objects.filter(
        is_deleted=False,
        tag_id=form.cleaned_data['tag'],
        object_enum=form.cleaned_data['object_enum'],
        object_id=form.cleaned_data['object_id']
    ).update(
        is_deleted=True,
    )

    # Ok - return blank
    return HttpResponse("")


# Internal function
def get_customer_list(destination, location_id):
    # Get a list of all objects assignments dependant on the destination
    object_customers = object_assignment.objects.filter(
        is_deleted=False,
        customer_id__isnull=False,
    )
    object_customers = get_object_from_destination(object_customers, destination, location_id)

    return customer.objects.filter(
        is_deleted=False,
        customer_id__in=object_customers.values('customer_id')
    )

# Internal function
def get_group_list(destination, location_id):
    object_results = object_assignment.objects.filter(
        is_deleted=False,
    )
    object_results = get_object_from_destination(
        object_results,
        destination,
        location_id
    )

    # Now return the groups
    return group.objects.filter(
        is_deleted=False,
        group_id__in=object_results.values('group_id')
    )


# Internal Function
def get_user_list(destination, location_id):
    # Get the data we want
    object_results = object_assignment.objects.filter(
        is_deleted=False,
        assigned_user_id__isnull=False,
    )
    object_results = get_object_from_destination(
        object_results,
        destination,
        location_id
    )

    # Get the user details
    user_results = User.objects.filter(
        id__in=object_results.values('assigned_user_id')
    ).values(
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )

    return json.dumps(list(user_results), cls=DjangoJSONEncoder)


# Internal Function
def get_user_list_all(destination, location_id):
    # Get a list of users we want to exclude
    object_results = object_assignment.objects.filter(
        is_deleted=False,
        assigned_user_id__isnull=False,
    )
    object_results = get_object_from_destination(
        object_results,
        destination,
        location_id
    )

    # Get a list of all the groups associated with this destination
    group_results = object_assignment.objects.filter(
        is_deleted=False,
        group_id__isnull=False,
    )
    group_results = get_object_from_destination(group_results, destination, location_id)

    # Get a list of users who are associated with these groups & not in the excluded list
    user_results = User.objects.filter(
        id__in=user_group.objects.filter(
            is_deleted=False,
            group_id__in=group_results.values('group_id'),
        ).values('username_id'),
        is_active=True,
    ).exclude(
        id__in=object_results.values('assigned_user_id')
    )

    # Send the results back
    return user_results


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def group_list(request, destination, location_id):
    # Get the data dependant on the object lookup
    group_results = get_group_list(destination, location_id)

    # Return the data
    return HttpResponse(serializers.serialize('json', group_results), content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def group_list_all(request, destination, location_id):
    # ADD CHECKS FOR USER PERMISSIONS!

    # Obtain data
    group_existing_results = object_assignment.objects.filter(
        is_deleted=False,
        group_id__isnull=False,
    )
    group_existing_results = get_object_from_destination(group_existing_results, destination, location_id)

    group_results = group.objects.filter(
        is_deleted=False,
    ).exclude(
        group_id__in=group_existing_results.values('group_id')
    )

    # Return data as json
    return HttpResponse(serializers.serialize('json', group_results), content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def lead_user_list(request):
    """
    :param request:
    :return:
    """
    # Get the data
    search_form = SearchForm(request.POST)
    if not search_form.is_valid():
        return HttpResponseBadRequest(search_form.errors)

    # First we create a search string and annotate it onto our results
    user_results = User.objects.annotate(
        search_string=Concat(
            'username', V(' '), 'first_name', V(' '), 'last_name', V(' '), 'email',
            output_field=CharField()
        )
    ).filter(
        is_active=True,
    )

    for split_row in search_form.cleaned_data['search'].split(' '):
        """
        """
        user_results.filter(
            search_string__icontains=split_row,
        )

    # Return the json data
    return HttpResponse(serializers.serialize('json', user_results[:25]), content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def link_list(request, destination, location_id, object_lookup):
    # Get the data dependent on the object lookup
    if object_lookup == 'project':
        data_results = project.objects.filter(
            is_deleted=False,
        ).exclude(
            project_status='Closed',
        )
    elif object_lookup == "task":
        data_results = task.objects.filter(
            is_deleted=False,
        ).exclude(
            task_status='Closed',
        )
    elif object_lookup == "requirement":
        data_results = requirement.objects.filter(
            is_deleted=False,
            requirement_status_id__in=list_of_requirement_status.objects.filter(
                is_deleted=False,
                requirement_status_is_closed=False,
            ).values('requirement_status_id'),
        )
    elif object_lookup == "requirement_item":
        data_results = requirement_item.objects.filter(
            is_deleted=False,
            requirement_item_status_id__in=list_of_requirement_item_status.objects.filter(
                is_deleted=False,
                status_is_closed=False,
            ).values('requirement_item_status_id'),
            requirement_id__in=requirement.objects.filter(
                is_deleted=False,
                requirement_status_id__in=list_of_requirement_status.objects.filter(
                    is_deleted=False,
                    requirement_status_is_closed=False,
                ).values('requirement_status_id')
            ).values('requirement_id'),
        )
    else:
        # There is an error.
        return HttpResponseBadRequest("Sorry - but that object lookup does not exist")

    # Send the data to the user
    return HttpResponse(serializers.serialize('json', data_results), content_type='application/json')


# Internal function
def link_object(object_assignment_submit, destination, location_id):
    """
    This is an internal function - depending on the destination, depends on what we are linking in the
    object_association_submit
    :param object_assignment_submit:
    :param destination:
    :param location_id:
    :return:
    """
    if destination == "project":
        object_assignment_submit.project = project.objects.get(project_id=location_id)
    elif destination == "requirement":
        object_assignment_submit.requirement = requirement.objects.get(requirement_id=location_id)
    elif destination == "requirement_item":
        object_assignment_submit.requirement_item = requirement_item.objects.get(requirement_item_id=location_id)
    elif destination == "task":
        object_assignment_submit.task = task.objects.get(task_id=location_id)

    # Return the results
    return object_assignment_submit


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def note_list(request, destination, location_id):
    # Everyone should have access to the notes section.

    # Get the notes dependent on the user destination and location
    note_results = object_note.objects.filter(
        is_deleted=False,
    )

    # Filter by destination and location_id
    note_results = get_object_from_destination(note_results, destination, location_id)

    # Return JSON results
    return HttpResponse(serializers.serialize('json', note_results), content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def object_link_list(request, destination, location_id):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    object_assignment_results = object_assignment.objects.filter(
        is_deleted=False,
    )
    object_assignment_results = get_object_from_destination(object_assignment_results, destination, location_id)

    object_assignment_results = object_assignment_results.filter(
        Q(project__isnull=False) |
        Q(requirement__isnull=False) |
        Q(requirement_item__isnull=False) |
        Q(task__isnull=False)
    ).values(
        'project_id',
        'project_id__project_name',
        'project_id__project_status',
        'task_id',
        'task_id__task_short_description',
        'task_id__task_status',
        'requirement_id',
        'requirement_id__requirement_title',
        'requirement_id__requirement_status__requirement_status',
        'requirement_item_id',
        'requirement_item_id__requirement_item_title',
        'requirement_item_id__requirement_item_status__requirement_item_status',
    )

    """
    As explained on stack overflow here - https://stackoverflow.com/questions/7650448/django-serialize-queryset-values-into-json#31994176
    We need to Django's serializers can't handle a ValuesQuerySet. However, you can serialize by using a standard 
    json.dumps() and transforming your ValuesQuerySet to a list by using list().[sic]
    """

    # Send back json data
    json_results = json.dumps(list(object_assignment_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def query_bug_client(request, destination, location_id):
    # Insert data into form
    form = QueryBugClientForm(request.POST)

    # Check to make sure everything is fine with the form
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extract the information from the form
    bug_client_instance = form.cleaned_data['bug_client_id']
    _ = form.cleaned_data['search']

    # Get existing bugs that we want to extract out
    existing_bugs = bug.objects.filter(
        is_deleted=False,
        bug_client_id=bug_client_instance.bug_client_id,
    )
    existing_bugs = get_object_from_destination(existing_bugs, destination, location_id)

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
        r = http.request('GET', url)

        # Extract the data
        json_data = json.loads(r.data.decode('utf-8'))
    else:
        raise ValueError from None

    # Send back the JSON data
    return JsonResponse(json_data['bugs'], safe=False)


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def tag_list(request, destination, location_id):
    # Get the data we want
    tag_results = tag.objects.filter(
        is_deleted=False,
        tag_id__in=tag_assignment.objects.filter(
            is_deleted=False,
            object_enum=destination,
            object_id=location_id,
        ).values('tag_id')
    )

    return HttpResponse(
        serializers.serialize('json', tag_results),
        content_type='application/json',
    )


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def tag_list_all(request):
    # Get the data we want
    tag_results = tag.objects.filter(
        is_deleted=False,
    )

    return HttpResponse(
        serializers.serialize('json', tag_results),
        content_type='application/json',
    )


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def user_list(request, destination, location_id):
    # Get the data we want
    user_results = get_user_list(destination, location_id)

    return HttpResponse(user_results, content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def user_list_all(request, destination, location_id):
    # ADD IN PERMISSIONS LATER

    # Get Data we want
    user_results = get_user_list_all(destination, location_id)

    return HttpResponse(serializers.serialize('json', user_results), content_type='application/json')
