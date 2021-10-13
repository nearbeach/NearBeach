import urllib
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum, Q, Min
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from NearBeach.decorators.check_user_permissions import check_user_permissions
from NearBeach.forms import NewTaskForm, TaskInformationForm
from NearBeach.models import group, user_group, object_assignment
from NearBeach.views.tools.internal_functions import task, organisation

import json
import urllib3


@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=3, object_lookup='task_id')
def new_task(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # ADD IN PERMISSIONS CHECKER

    # Template
    t = loader.get_template('NearBeach/tasks/new_task.html')

    # Get data
    group_results = group.objects.filter(
        is_deleted=False,
    )

    # Get list of user groups
    user_group_results = user_group.objects.filter(
        is_deleted=False,
        username=request.user,
    ).values(
        'group_id',
        'group__group_name',
    ).distinct()

    # Context
    c = {
        'nearbeach_title': 'New Task',
        'group_results': serializers.serialize('json', group_results),
        'user_group_results': json.dumps(list(user_group_results), cls=DjangoJSONEncoder),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name='')
@check_user_permissions(min_permission_level=3, object_lookup='task_id')
def new_task_save(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # ADD IN USER PERMISSIONS

    # Get form data
    form = NewTaskForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create the new task
    task_submit = task(
        change_user=request.user,
        creation_user=request.user,
        task_short_description=form.cleaned_data['task_short_description'],
        task_long_description=form.cleaned_data['task_long_description'],
        task_start_date=form.cleaned_data['task_start_date'],
        task_end_date=form.cleaned_data['task_end_date'],
        organisation=form.cleaned_data['organisation'],
    )
    task_submit.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = object_assignment(
            group_id=group_instance,
            task=task_submit,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Send back requirement_information URL
    return HttpResponse(reverse('task_information', args={task_submit.task_id}))


@login_required(login_url='login', redirect_field_name="")
@check_user_permissions(min_permission_level=1, object_lookup='task_id')
def task_information(request, task_id, *args, **kwargs):
    """
    :param request:
    :param task_id:
    :return:
    """
    user_level = kwargs['user_level']

    # Template
    t = loader.get_template('NearBeach/tasks/task_information.html')

    # Get Data
    task_results = task.objects.get(task_id=task_id)
    task_status = task_results.task_status

    organisation_results = organisation.objects.filter(
        is_deleted=False,
        organisation_id=task_results.organisation_id,
    )

    # Context
    c = {
        'nearbeach_title': 'Task Information %s' % task_id,
        'organisation_results': serializers.serialize('json', organisation_results),
        'user_level': user_level,
        'task_id': task_id,
        'task_results': serializers.serialize('json', [task_results]),
        'task_status': task_status,
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name='')
@check_user_permissions(min_permission_level=2, object_lookup='task_id')
def task_information_save(request, task_id, *args, **kwargs):
    """
    :param request:
    :param task_id:
    :return:
    """
    # Form
    form = TaskInformationForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the instance
    update_task = task.objects.get(task_id=task_id)

    # Update the values
    update_task.task_short_description = form.cleaned_data['task_short_description']
    update_task.task_long_description = form.cleaned_data['task_long_description']
    update_task.task_start_date = form.cleaned_data['task_start_date']
    update_task.task_end_date = form.cleaned_data['task_end_date']
    update_task.task_status = form.cleaned_data['task_status']

    update_task.save()

    return HttpResponse("")
