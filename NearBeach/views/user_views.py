from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from knox.models import AuthToken

from NearBeach.decorators.check_user_permissions.admin_permissions import check_user_admin_permissions
from NearBeach.forms import NewUserForm, PasswordResetForm, UpdateUserForm, UserRemovePermissionForm
from NearBeach.models import UserGroup
from NearBeach.views.tools.internal_functions import get_user_permissions
from NearBeach.views.theme_views import get_theme

import json


@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_user")
def new_user(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Add in user permissions

    # Get template
    t = loader.get_template("NearBeach/users/new_user.html")

    # Get context
    c = {
        "nearbeach_title": "New User",
        "need_tinymce": False,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(3, "administration_create_user")
def new_user_save(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # CHECK USER PERMISSSIONS

    # Get form data
    form = NewUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create the new user
    submit_user = User(
        username=form.cleaned_data["username"],
        email=form.cleaned_data["email"],
        first_name=form.cleaned_data["first_name"],
        last_name=form.cleaned_data["last_name"],
        is_active=True,
    )

    # Set the user password
    submit_user.set_password(form.cleaned_data["password1"])

    # Save
    submit_user.save()

    return HttpResponse(reverse("user_information", args=[submit_user.id]))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def update_password(request, *args, **kwargs):
    """ """
    # Get form data
    form = PasswordResetForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_json())

    # Check to make sure we are updating ONLY the current user
    if not form.cleaned_data["username"] == request.user:
        return HttpResponseBadRequest("Unknown Error")

    # Get the User object
    user_update = form.cleaned_data["username"]
    user_update.set_password(form.cleaned_data["password"])
    user_update.save()

    # Refresh user's hash
    update_session_auth_hash(request, form.cleaned_data["username"])

    return HttpResponse("")


@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(1, "administration_create_user")
def user_information(request, username, *args, **kwargs):
    """
    :param request:
    :param permission_set_id:
    :return:
    """
    # check user permissions

    # Import template
    t = loader.get_template("NearBeach/users/user_information.html")

    # Get user data
    user_results = User.objects.get(id=username)

    user_list_results = get_user_permissions("username", username)
    user_list_results = json.dumps(list(user_list_results), cls=DjangoJSONEncoder)

    # Get API results
    # api_results = APIKeyMeta.objects.filter(
    #     user=user_results,
    # )
    # api_results = json.dumps(list(api_results), cls=DjangoJSONEncoder)

    # Create the context
    c = {
        "nearbeach_title": f"User Information {username}",
        "user_list_results": user_list_results,
        "user_results": serializers.serialize("json", [user_results]),
        "username": username,
        "need_tinymce": False,
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(2, "administration_create_user")
def user_information_save(request, username, *args, **kwargs):
    """
    :param request:
    :param username:
    :return:
    """
    # Add in user permissions

    # Get form
    form = UpdateUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get user
    update_user = User.objects.get(id=username)

    # Update the user
    update_user.first_name = form.cleaned_data["first_name"]
    update_user.last_name = form.cleaned_data["last_name"]
    update_user.email = form.cleaned_data["email"]
    update_user.is_active = form.cleaned_data["is_active"]
    update_user.is_superuser = form.cleaned_data["is_superuser"]

    # Save
    update_user.save()

    # Send back blank 200
    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(4, "administration_create_user")
def user_remove_permission(request, *args, **kwargs):
    # Get the form data
    form = UserRemovePermissionForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    user_group_id = form.cleaned_data['user_group_id']

    user_group_update = UserGroup.objects.get(
        user_group_id = user_group_id.user_group_id,
    )

    user_group_update.is_deleted = True
    user_group_update.save()

    # Send back success
    return HttpResponse()
