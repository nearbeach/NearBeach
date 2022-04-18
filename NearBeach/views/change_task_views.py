from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.forms import ChangeTaskStatusForm, ChangeTaskForm
from NearBeach.models import change_task, User

import json


@login_required(login_url='login', redirect_field_name="")
def change_task_information(request, change_task_id, *args, **kwargs):
    """
    """
    # Get Change Task Information
    change_task_results = change_task.objects.filter(
        is_deleted=False,
        change_task_id=change_task_id,
    )

    # If the change task has been deleted or does not exist, go to 404
    if len(change_task_results) == 0:
        raise Http404()

    # Load the template
    t = loader.get_template('NearBeach/request_for_change/change_task_information.html')

    user_list = User.objects.filter(
        is_active=True,
        # id__in=user_group.objects.filter(
        #     is_deleted=False,
        #     group_id__in=object_assignment.objects.filter(
        #         is_deleted=False,
        #         request_for_change_id=rfc_id,
        #     ).values('group_id')
        # ).values('username_id')
    ).values(
        'id',
        'email',
        'first_name',
        'last_name',
        'username',
    )
    
    #Change from ORM to json
    user_list = json.dumps(list(user_list), cls=DjangoJSONEncoder)

    # Context
    c = {
        'change_task_results': serializers.serialize('json', change_task_results),
        'user_list': user_list,
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def change_task_save(request, change_task_id):
    """
    """
    # Get form data
    form  = ChangeTaskForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the instance
    change_task_update = change_task.objects.get(change_task_id=change_task_id)

    # Update the values
    change_task_update.change_task_title = form.cleaned_data['change_task_title']
    change_task_update.change_task_description = form.cleaned_data['change_task_description']
    change_task_update.change_task_start_date = form.cleaned_data['change_task_start_date']
    change_task_update.change_task_end_date = form.cleaned_data['change_task_end_date']
    change_task_update.change_task_seconds = form.cleaned_data['change_task_seconds']
    change_task_update.change_task_required_by = form.cleaned_data['change_task_required_by']
    change_task_update.is_downtime = form.cleaned_data['is_downtime']
    change_task_update.change_task_qa_user = form.cleaned_data['change_task_qa_user']
    change_task_update.change_task_assigned_user = form.cleaned_data['change_task_assigned_user']

    change_task_update.save()

    # Send back empty but successful data
    return HttpResponse("")


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def update_status(request, change_task_id):
    """
    :param request:
    :param change_task_id:
    :return:
    """
    # Get form data
    form = ChangeTaskStatusForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get change task
    change_task_results = change_task.objects.get(change_task_id=change_task_id)

    # Update the change task results
    change_task_results.change_task_status = form.cleaned_data['change_task_status']
    change_task_results.save()

    return HttpResponse("")
