from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_http_methods

from NearBeach.forms import (
    AdminAddUserForm,
    PasswordResetForm,
    UpdateGroupLeaderStatusForm,
)
from NearBeach.models import UserGroup
from NearBeach.views.tools.internal_functions import get_user_permissions

from NearBeach.decorators.check_user_permissions import check_user_admin_permissions

import itertools
import json


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_user")
def add_user(request, *args, **kwargs):
    '''
    Adds a user to either;
    - Multiple groups and/or
    - Multiple permission sets
    :param request:
    :return: Successful result
    '''
    form = AdminAddUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    '''
    We can assume that there are;
    - Single User
    - Multiple Groups
    - Multiple Permission Sets

    We need to loop through these permutations, and add them into the database
    '''

    group_results = form.cleaned_data["group"]
    permission_set_results = form.cleaned_data["permission_set"]
    user_results = form.cleaned_data["username"]

    # Loop through the results from itertools.product - and apply permissions
    for group_row, permission_set_row in itertools.product(group_results, permission_set_results):
        submit_user = UserGroup(
            username=user_results,
            permission_set=permission_set_row,
            group=group_row,
            change_user=request.user,
        )
        submit_user.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@check_user_admin_permissions(2, "administration_create_group")
def update_group_leader_status(request, destination, *args, **kwargs):
    '''
    This function will update the user's group leader status against a particular group.
    :param request: Normal stuff.
    :param destination: 
    :return:
    '''
    form = UpdateGroupLeaderStatusForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Start filtering the user_group
    user_group_update = UserGroup.objects.filter(
        is_deleted=False,
        username=form.cleaned_data["username"],
    )

    # Depending on the destination - depends what else we filter on
    if destination == "group":
        # Get group id
        group_id = form.cleaned_data["group"].first()

        # Update the user group
        user_group_update.filter(
            group=group_id,
        ).update(group_leader=form.cleaned_data["group_leader"])

        # Get new user_list_results
        user_list_results = get_user_permissions("group_id", group_id)
    elif destination == "permission_set":
        # Get Permission Set ID
        permission_set_id = form.cleaned_data["permission_set"].first()

        # Update the user group
        user_group_update.filter(
            permission_set=permission_set_id,
        ).update(group_leader=form.cleaned_data["group_leader"])

        # Get new user_list_results
        user_list_results = get_user_permissions("permission_set_id", permission_set_id)
    else:
        # Get group id
        group_id = form.cleaned_data["group"].first()

        # Update the user list
        user_group_update.filter(
            group=group_id,
        ).update(group_leader=form.cleaned_data["group_leader"])

        user_list_results = get_user_permissions(
            "username", form.cleaned_data["username"]
        )

    # Convert into json
    user_list_results = json.dumps(list(user_list_results), cls=DjangoJSONEncoder)

    return HttpResponse(
        user_list_results,
        content_type="application/json",
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(2, "administration_create_user")
def update_user_password(request, *args, **kwargs):
    '''Will update the users password''' 
    # Get form data
    form = PasswordResetForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the User object
    user_update = form.cleaned_data["username"]
    user_update.set_password(form.cleaned_data["password"])
    user_update.save()

    return HttpResponse("")
