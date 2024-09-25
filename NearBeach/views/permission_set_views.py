from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from NearBeach.decorators.check_user_permissions.admin_permissions import check_user_admin_permissions
from NearBeach.forms import NewPermissionSetForm, PermissionSetForm, SearchForm
from NearBeach.models import (
    PermissionSet,
    PERMISSION_BOOLEAN,
    PERMISSION_LEVEL,
    UserGroup,
)
from NearBeach.views.tools.internal_functions import get_user_permissions
from NearBeach.views.theme_views import get_theme

import json


@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_permission_set")
def check_permission_set_name(request, *args, **kwargs):
    form = SearchForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Check to see if the permission set name exists
    permission_set_results = PermissionSet.objects.filter(
        is_deleted=False,
        permission_set_name__iexact=form.cleaned_data["search"],
    )

    # Send back data
    return HttpResponse(
        serializers.serialize("json", permission_set_results),
        content_type="application/json",
    )


@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_permission_set")
def new_permission_set(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Check user permissions

    # Get template
    t = loader.get_template("NearBeach/permission_sets/new_permission_set.html")

    # Get context
    c = {
        "nearbeach_title": "New Permission Set",
        "need_tinymce": False,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_permission_set")
def new_permission_set_save(request, *args, **kwargs):
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
    submit_permission_set = PermissionSet(
        permission_set_name=form.cleaned_data["permission_set_name"],
        change_user=request.user,
    )

    submit_permission_set.save()

    # Return back the permission set information URL
    return HttpResponse(
        reverse(
            "permission_set_information", args={submit_permission_set.permission_set_id}
        )
    )


@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(1, "administration_create_permission_set")
def permission_set_information(request, permission_set_id, *args, **kwargs):
    """
    :param request:
    :param permission_set_id:
    :return:
    """
    # Add in permission checks

    # Import template
    t = loader.get_template("NearBeach/permission_sets/permission_set_information.html")

    # Get data
    permission_set_results = PermissionSet.objects.get(
        permission_set_id=permission_set_id
    )

    user_list_results = get_user_permissions("permission_set_id", permission_set_id)
    user_list_results = json.dumps(list(user_list_results), cls=DjangoJSONEncoder)

    # Create the context
    c = {
        "nearbeach_title": f"Permission Set {permission_set_id}",
        "need_tinymce": False,
        "permission_set_results": serializers.serialize(
            "json", [permission_set_results]
        ),
        "permission_set_id": permission_set_id,
        "permission_boolean": json.dumps(PERMISSION_BOOLEAN),
        "permission_level": json.dumps(PERMISSION_LEVEL),
        "theme": get_theme(request),
        "user_list_results": user_list_results,
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(4, "administration_create_permission_set")
def permission_set_information_delete(request, permission_set_id, *args, **kwargs):
    if permission_set_id == 1:
        return HttpResponseBadRequest("Can not delete admin permission set")

    # Delete permission set
    PermissionSet.objects.filter(
        permission_set_id=permission_set_id,
    ).update(
        is_deleted=True,
    )

    # Delete any user permissions with this permission set
    UserGroup.objects.filter(
        permission_set_id=permission_set_id,
    ).update(
        is_deleted=True,
    )

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(2, "administration_create_permission_set")
def permission_set_information_save(request, permission_set_id, *args, **kwargs):
    """
    :param request:
    :param permission_set_id:
    :return:
    """
    # Check to make sure nothing changes for the administration permissions
    if permission_set_id == 1:
        return HttpResponseBadRequest("Error - can not edit administration")

    # Get form data
    form = PermissionSetForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the object
    update_permission_set = PermissionSet.objects.get(
        permission_set_id=permission_set_id
    )

    # Update the object
    update_permission_set.permission_set_name = form.cleaned_data["permission_set_name"]
    update_permission_set.administration_assign_user_to_group = form.cleaned_data[
        "administration_assign_user_to_group"
    ]
    update_permission_set.administration_create_group = form.cleaned_data[
        "administration_create_group"
    ]
    update_permission_set.administration_create_permission_set = form.cleaned_data[
        "administration_create_permission_set"
    ]
    update_permission_set.administration_create_user = form.cleaned_data[
        "administration_create_user"
    ]
    update_permission_set.bug_client = form.cleaned_data["bug_client"]
    update_permission_set.customer = form.cleaned_data["customer"]
    update_permission_set.kanban_board = form.cleaned_data["kanban_board"]
    update_permission_set.kanban_card = form.cleaned_data["kanban_card"]
    update_permission_set.organisation = form.cleaned_data["organisation"]
    update_permission_set.project = form.cleaned_data["project"]
    update_permission_set.requirement = form.cleaned_data["requirement"]
    update_permission_set.request_for_change = form.cleaned_data["request_for_change"]
    update_permission_set.task = form.cleaned_data["task"]
    update_permission_set.tag = form.cleaned_data["tag"]
    update_permission_set.document = form.cleaned_data["document"]
    update_permission_set.kanban_note = form.cleaned_data["kanban_note"]
    update_permission_set.project_note = form.cleaned_data["project_note"]
    update_permission_set.task_note = form.cleaned_data["task_note"]
    update_permission_set.requirement_note = form.cleaned_data["requirement_note"]
    update_permission_set.requirement_item_note = form.cleaned_data["requirement_item_note"]
    update_permission_set.organisation_note = form.cleaned_data["organisation_note"]

    update_permission_set.save()

    return HttpResponse("")
