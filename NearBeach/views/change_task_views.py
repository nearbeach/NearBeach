from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404

from NearBeach.forms import ChangeTaskIsDowntimeForm, ChangeTaskStatusForm, ChangeTaskForm, ChangeTaskDescriptionForm, ChangeTaskRequiredByForm
from NearBeach.models import ChangeTask, RequestForChange, User
from NearBeach.views.theme_views import get_theme

from NearBeach.decorators.check_user_permissions import check_change_task_permissions

import json


@login_required(login_url="login", redirect_field_name="")
@check_change_task_permissions(min_permission_level=1)
def change_task_information(request, change_task_id, *args, **kwargs):
    """
    Render the Change Task information page

    :param request:
    :param change_task_id: the change task ID
    :return: Change Task information page
    """
    # Get Change Task Information
    change_task_results = get_object_or_404(
        ChangeTask,
        change_task_id=change_task_id,
        is_deleted=False,
    )

    rfc_results = RequestForChange.objects.get(
        rfc_id=change_task_results.request_for_change_id
    )

    # Load the template
    t = loader.get_template("NearBeach/change_task/change_task_information.html")

    user_list = User.objects.filter(is_active=True,).values(
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
    )

    # Change from ORM to json
    user_list = json.dumps(list(user_list), cls=DjangoJSONEncoder)

    # Context
    c = {
        "change_task_id": change_task_id,
        "change_task_results": serializers.serialize("json", [change_task_results]),
        "need_tinymce": True,
        "nearbeach_title": f"Change Task {change_task_id}",
        "rfc_status": rfc_results.rfc_status,
        "user_level": kwargs["user_level"],
        "user_list": user_list,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_change_task_permissions(min_permission_level=4)
def change_task_delete(request, change_task_id, *args, **kwargs):
    """
    A simple function to delete the change task
    :param: change_task_id: The change task to delete
    :return: Success 200
    """
    change_task_update = ChangeTask.objects.get(change_task_id=change_task_id)

    # Update the change task is deleted to true
    change_task_update.is_deleted = True
    change_task_update.save()

    # Send back success
    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_change_task_permissions(min_permission_level=2)
def change_task_save(request, change_task_id, *args, **kwargs):
    """
    A simple POST function where the user can save the change task data
    :param: change_task_id: The change task we are updating
    :return: Success 200
    """
    # Get form data
    form = ChangeTaskForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the instance
    change_task_update = ChangeTask.objects.get(change_task_id=change_task_id)

    # Update the values
    change_task_update.change_task_title = form.cleaned_data["change_task_title"]
    change_task_update.change_task_description = form.cleaned_data[
        "change_task_description"
    ]
    change_task_update.change_task_start_date = form.cleaned_data[
        "change_task_start_date"
    ]
    change_task_update.change_task_end_date = form.cleaned_data["change_task_end_date"]
    change_task_update.change_task_seconds = form.cleaned_data["change_task_seconds"]
    change_task_update.change_task_required_by = form.cleaned_data[
        "change_task_required_by"
    ]
    change_task_update.is_downtime = form.cleaned_data["is_downtime"]
    change_task_update.change_task_qa_user = form.cleaned_data["change_task_qa_user"]
    change_task_update.change_task_assigned_user = form.cleaned_data[
        "change_task_assigned_user"
    ]

    change_task_update.save()

    # Send back empty but successful data
    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_change_task_permissions(min_permission_level=1)
def get_change_task_list(request, change_task_id, *args, **kwargs):
    """
    A POST node to get a list of all change tasks assigned to an RFC
     - the RFC is linked to the change task id
    :param request:
    : param change_task_id: the change task id which we will obtain the RFC from
    : return: List of all Change Tasks assigned to this RFC
    """
    change_task_instance = ChangeTask.objects.get(change_task_id=change_task_id)

    change_task_results = ChangeTask.objects.filter(
        is_deleted=False,
        request_for_change_id=change_task_instance.request_for_change_id,
    ).exclude(
        change_task_id=change_task_id,
    )

    # Send data to user
    return HttpResponse(
        serializers.serialize("json", change_task_results), content_type="application/json"
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_change_task_permissions(min_permission_level=2)
def update_description(request, change_task_id, *args, **kwargs):
    """
    A POST node to update the change task description
    :param request:
    :param change_task_id: the change task id to update the description
    : return: Success 200
    """
    form = ChangeTaskDescriptionForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get change task
    change_task_results = ChangeTask.objects.get(change_task_id=change_task_id)

    # Update the change task results
    change_task_results.change_task_description = form.cleaned_data['change_task_description']
    change_task_results.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_change_task_permissions(min_permission_level=2)
def update_is_downtime(request, change_task_id, *args, **kwargs):
    form = ChangeTaskIsDowntimeForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the change task
    change_task_results = ChangeTask.objects.get(change_task_id=change_task_id)

    # Update the change task results
    change_task_results.is_downtime = form.cleaned_data['is_downtime']
    change_task_results.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_change_task_permissions(min_permission_level=2)
def update_required_by(request, change_task_id, *args, **kwargs):
    form = ChangeTaskRequiredByForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the change task
    change_task_results = ChangeTask.objects.get(change_task_id=change_task_id)

    # Update the change task results
    change_task_results.change_task_required_by = form.cleaned_data['change_task_required_by']
    change_task_results.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_change_task_permissions(min_permission_level=2)
def update_status(request, change_task_id, *args, **kwargs):
    """
    A POST node to update the change task status
    :param request:
    :param change_task_id: the change task id to update
    :return: Success 200
    """
    # Get form data
    form = ChangeTaskStatusForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get change task
    change_task_results = ChangeTask.objects.get(change_task_id=change_task_id)

    # Double check RFC is still open - otherwise send back a 423
    rfc_results = RequestForChange.objects.get(
        rfc_id=change_task_results.request_for_change_id
    )
    if not rfc_results.rfc_status_id == 4:
        return HttpResponse(
            "RFC Currently Locked - not in start mode",
            status = 423  # Locked
        )

    # Update the change task results
    change_task_results.change_task_status = form.cleaned_data["change_task_status"]
    change_task_results.save()

    return HttpResponse("")
