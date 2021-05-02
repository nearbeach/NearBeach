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
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from NearBeach.decorators.check_user_permissions import check_user_permissions

import json


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=2, object_lookup='requirement_id')
def add_requirement_link(request, requirement_id, *args, **kwargs):
    # Check user form is valid
    form = AddRequirementLinkForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the requirement instnace
    requirement_instance = requirement.objects.get(requirement_id=requirement_id)

    # Get the project list from the form
    for row in request.POST.getlist("project"):
        submit_object_assignment = object_assignment(
            requirement=requirement_instance,
            project=project.objects.get(project_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    for row in request.POST.getlist("task"):
        submit_object_assignment = object_assignment(
            requirement=requirement_instance,
            task=task.objects.get(task_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    for row in request.POST.getlist("opportunity"):
        submit_object_assignment = object_assignment(
            requirement=requirement_instance,
            opportunity=opportunity.objects.get(opportunity_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    return HttpResponse("Success")


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup='requirement_id')
def get_requirement_item_links(request, requirement_id, *args, **kwargs):
    # Get the requirement information
    requirement_results = requirement.objects.get(requirement_id=requirement_id)

    # Use object_assignment to get the requirme
    link_results = object_assignment.objects.filter(
        Q(
            is_deleted=False,
            requirement_item_id__in=requirement_item.objects.filter(
                is_deleted=False,
                requirement_id=requirement_id,
            ).values('requirement_item_id')
        ) & Q(
            Q(opportunity_id__isnull=False) |
            Q(quote_id__isnull=False) |
            Q(project_id__isnull=False) |
            Q(task_id__isnull=False)
        )
    ).values(
        'opportunity_id',
        'opportunity_id__opportunity_name',
        'opportunity_id__opportunity_stage_id__opportunity_stage_description',
        'quote_id',
        'quote_id__quote_title',
        'quote_id__quote_stage_id__quote_stage',
        'project_id',
        'project_id__project_name',
        'project_id__project_status',
        'task_id',
        'task_id__task_short_description',
        'task_id__task_status',
        'requirement_item_id',
        'requirement_item_id__requirement_item_title',
    )

    """
    As explained on stack overflow here - https://stackoverflow.com/questions/7650448/django-serialize-queryset-values-into-json#31994176
    We need to Django's serializers can't handle a ValuesQuerySet. However, you can serialize by using a standard 
    json.dumps() and transforming your ValuesQuerySet to a list by using list().[sic]
    """

    # Send back json data
    json_results = json.dumps(list(link_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup='requirement_id')
def get_requirement_item_status_list(request, requirement_id, *args, **kwargs):
    # Get all status - even deleted ones.
    status_list = list_of_requirement_item_status.objects.all()

    # Send back json data
    json_results = serializers.serialize('json', status_list)

    return HttpResponse(json_results, content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup='requirement_id')
def get_requirement_item_type_list(request, requirement_id, *args, **kwargs):
    # Get all status - even deleted ones.
    type_list = list_of_requirement_item_type.objects.all()

    # Send back json data
    json_results = serializers.serialize('json', type_list)

    return HttpResponse(json_results, content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup='requirement_id')
def get_requirement_items(request, requirement_id, *args, **kwargs):
    # Get all the requirement items assigned to the requirement
    requirement_item_results = requirement_item.objects.filter(
        is_deleted=False,
        requirement_id=requirement_id,
    )

    # Send back json data
    json_results = serializers.serialize('json', requirement_item_results)

    return HttpResponse(json_results, content_type='application/json')


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup='requirement_id')
def get_requirement_links_list(request, requirement_id, *args, **kwargs):
    # Get the requirement information
    requirement_results = requirement.objects.get(requirement_id=requirement_id)

    # Use object_assignment to get the requirme
    link_results = object_assignment.objects.filter(
        Q(
            is_deleted=False,
            requirement_id=requirement_id,
        ) & Q(
            Q(quote_id__isnull=False) |
            Q(project_id__isnull=False) |
            Q(task_id__isnull=False)
        )
    ).values(
        'project_id',
        'project_id__project_name',
        'project_id__project_status',
        'task_id',
        'task_id__task_short_description',
        'task_id__task_status',
        'requirement_item_id',
        'requirement_item_id__requirement_item_title',
    )

    """
    As explained on stack overflow here - https://stackoverflow.com/questions/7650448/django-serialize-queryset-values-into-json#31994176
    We need to Django's serializers can't handle a ValuesQuerySet. However, you can serialize by using a standard 
    json.dumps() and transforming your ValuesQuerySet to a list by using list().[sic]
    """

    # Send back json data
    json_results = json.dumps(list(link_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=3, object_lookup='requirement_id')
def new_requirement(request, *args, **kwargs):
    """
    Loads the new requirement page
    :param request:
    :param location_id:
    :param destination:
    :return:
    """
    # Extract Data
    status_list = list_of_requirement_status.objects.filter(
        is_deleted=False,
        requirement_status_is_closed=False,
    )

    type_list = list_of_requirement_type.objects.filter(
        is_deleted=False,
    )

    group_results = group.objects.filter(
        is_deleted=False,
    )

    # Load template
    t = loader.get_template('NearBeach/requirements/new_requirements.html')

    # context
    c = {
        'status_list': serializers.serialize("json", status_list),
        'type_list': serializers.serialize("json", type_list),
        'group_results': serializers.serialize("json", group_results),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name='')
@check_user_permissions(min_permission_level=3, object_lookup='requirement_id')
def new_requirement_save(request, *args, **kwargs):
    # Get the data and place into the form
    form = NewRequirementForm(request.POST)
    if not form.is_valid():
        # Something went wrong with the form.
        return HttpResponseBadRequest("There was something wrong with the form")

    # Save the form
    submit_requirement = requirement(
        requirement_title=form.cleaned_data['requirement_title'],
        requirement_scope=form.cleaned_data['requirement_scope'],
        organisation=form.cleaned_data['organisation'],
        requirement_status=form.cleaned_data['requirement_status'],
        requirement_type=form.cleaned_data['requirement_type'],
        change_user=request.user,
        creation_user=request.user,
    )
    submit_requirement.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = object_assignment(
            group_id=group_instance,
            requirement=submit_requirement,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Send back requirement_information URL
    return HttpResponse(reverse('requirement_information', args={submit_requirement.requirement_id}))


@login_required(login_url='login', redirect_field_name='')
@check_user_permissions(min_permission_level=1, object_lookup='requirement_id')
def requirement_information(request, requirement_id, *args, **kwargs):
    """
    Loads the requirement information.
    :param request:
    :param requirement_id:
    :return:
    """
    # TODO: Check if I need to have a separate read only tempalte now.
    requirement_results = requirement.objects.get(requirement_id=requirement_id)

    # If the requirement has been closed - send user to the read only section
    if requirement_results.requirement_status.requirement_status == "Completed":
        return HttpResponseRedirect(reverse('requirement_readonly', args={requirement_id}))

    # Load template
    t = loader.get_template('NearBeach/requirements/requirement_information.html')

    # Get any extra data required
    organisation_results = organisation.objects.get(
        organisation_id=requirement_results.organisation_id,
    )

    status_list = list_of_requirement_status.objects.filter(
        is_deleted=False,
        requirement_status_is_closed=False,
    )

    type_list = list_of_requirement_type.objects.filter(
        is_deleted=False,
    )

    group_results = group.objects.filter(
        is_deleted=False,
    )

    requirement_item_results = requirement_item.objects.filter(
        is_deleted=False,
        requirement_id=requirement_id,
    )

    # context
    c = {
        'group_results': serializers.serialize("json", group_results),
        'organisation_results': serializers.serialize("json", [organisation_results]),
        'requirement_results': serializers.serialize("json", [requirement_results]),
        'requirement_id': requirement_id,
        'requirement_item_results': serializers.serialize("json", requirement_item_results),
        'status_list': serializers.serialize("json", status_list),
        'type_list': serializers.serialize("json", type_list),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=2, object_lookup='requirement_id')
def requirement_information_save(request, requirement_id, *args, **kwargs):
    """

    :param request:
    :param requirement_id:
    :return:
    """
    # Insert POST into form
    form = UpdateRequirementForm(request.POST)

    # If there is an error - notify the user
    if not form.is_valid():
        return HttpResponseBadRequest("Sorry, there is an error with the form: %s" % form.errors)

    # Get the requirement
    requirement_result = requirement.objects.get(requirement_id=requirement_id)

    # Update all the fields
    requirement_result.requirement_title = form.cleaned_data['requirement_title']
    requirement_result.requirement_scope = form.cleaned_data['requirement_scope']
    requirement_result.requirement_status = form.cleaned_data['requirement_status']
    requirement_result.requirement_type = form.cleaned_data['requirement_type']

    requirement_result.save()

    # Return a success
    return HttpResponse("Requirement Saved")
