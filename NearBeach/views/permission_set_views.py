from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.models import *
from NearBeach.forms import *

import json


@login_required(login_url='login',redirect_field_name="")
def new_permission_set(request):
    """

    :param request:
    :return:
    """

    # Check user permissions

    # Get template
    t = loader.get_template('NearBeach/permission_sets/new_permission_set.html')

    # Get context
    c = {}

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def new_permission_set_save(request):
    """

    :param request:
    :return:
    """

    # Check user permissions

    # Get form data
    form = NewPermissionSetForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    submit_permission_set = permission_set(
        permission_set_name=form.cleaned_data['permission_set_name'],
        change_user=request.user,
    )

    submit_permission_set.save()

    # Return back the permission set information URL
    return HttpResponse(reverse('permission_set_information',args={submit_permission_set.permission_set_id}))


@login_required(login_url='login',redirect_field_name="")
def permission_set_information(request, permission_set_id):
    """

    :param request:
    :param permission_set_id:
    :return:
    """

    # Add in permission checks

    # Import template
    t = loader.get_template('NearBeach/permission_sets/permission_set_information.html')

    # Get data
    permission_set_results = permission_set.objects.get(permission_set_id=permission_set_id)

    user_list_results = user_group.objects.filter(
        is_deleted=False,
        permission_set_id=permission_set_id,
    ).values(
        'username',
        'username__first_name',
        'username__last_name',
        'username__email',
        'group',
        'group__group_name',
        'permission_set',
        'permission_set__permission_set_name',
    ).order_by(
        'username__first_name',
        'username__last_name',
        'permission_set__permission_set_name',
    )
    user_list_results = json.dumps(list(user_list_results), cls=DjangoJSONEncoder)

    # Create the context
    c = {
        'permission_set_results': serializers.serialize('json', [permission_set_results]),
        'user_list_results': user_list_results,
        'permission_set_id': permission_set_id,
        'permission_boolean': json.dumps(PERMISSION_BOOLEAN),
        'permission_level': json.dumps(PERMISSION_LEVEL),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def permission_set_information_save(request, permission_set_id):
    """

    :param request:
    :param permission_set_id:
    :return:
    """

    # ADD IN USER PERMISSIONS LATER

    # Check to make sure nothing changes for the administration permissions
    if permission_set_id == 1:
        return HttpResponseBadRequest("Error - can not edit administration")

    # Get form data
    form = PermissionSetForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the object
    update_permission_set = permission_set.objects.get(permission_set_id=permission_set_id)

    # Update the object
    update_permission_set.permission_set_name = form.cleaned_data['permission_set_name']
    update_permission_set.administration_assign_user_to_group = form.cleaned_data['administration_assign_user_to_group']
    update_permission_set.administration_create_group = form.cleaned_data['administration_create_group']
    update_permission_set.administration_create_permission_set = form.cleaned_data[
        'administration_create_permission_set']
    update_permission_set.administration_create_user = form.cleaned_data['administration_create_user']
    update_permission_set.bug_client = form.cleaned_data['bug_client']
    update_permission_set.customer = form.cleaned_data['customer']
    update_permission_set.kanban = form.cleaned_data['kanban']
    update_permission_set.kanban_card = form.cleaned_data['kanban_card']
    update_permission_set.organisation = form.cleaned_data['organisation']
    update_permission_set.project = form.cleaned_data['project']
    update_permission_set.requirement = form.cleaned_data['requirement']
    update_permission_set.request_for_change = form.cleaned_data['request_for_change']
    update_permission_set.task = form.cleaned_data['task']
    update_permission_set.document = form.cleaned_data['document']
    update_permission_set.kanban_comment = form.cleaned_data['kanban_comment']
    update_permission_set.project_history = form.cleaned_data['project_history']
    update_permission_set.task_history = form.cleaned_data['task_history']

    update_permission_set.save()

    return HttpResponse("")
