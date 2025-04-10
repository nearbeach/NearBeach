from django.contrib.auth import get_user_model
from ...forms import PermissionSet, Group, LoginForm
from ...models import UserGroup, Notification, Organisation
from django.contrib.auth.models import User

# Import Django Libraries
from django.contrib import auth
from django.contrib.auth.decorators import login_required, settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from random import SystemRandom
from NearBeach.decorators.check_user_permissions.permission_denied import check_permission_denied

# Import Python Libraries
import json
import urllib.parse
import datetime

User = get_user_model()


def check_first_time_login(request):
    """
    The following function will check if it is the first time logged in by user. i.e. There are no permission sets.
    If there are no permission sets - this function will create it.

    If there are permission sets - nothing done.
    :return:

    The user has been authenticated. Now the system will store the user's permissions and group
    into cookies. :)

    First Setup
    ~~~~~~~~~~~
    If permission_set with id of 1 does not exist, go through first stage setup.
    """
    if not PermissionSet.objects.all():
        # Create administration permission_set
        submit_permission_set_1 = PermissionSet(
            permission_set_name="Administration Permission Set",
            administration_assign_user_to_group=4,
            administration_create_group=4,
            administration_create_permission_set=4,
            administration_create_user=4,
            bug_client=4,
            customer=4,
            kanban_board=4,
            kanban_card=4,
            organisation=4,
            project=4,
            request_for_change=4,
            requirement=4,
            task=4,
            tag=4,
            document=1,
            kanban_note=1,
            project_note=1,
            task_note=1,
            requirement_note=1,
            requirement_item_note=1,
            change_user=request.user,
        )
        submit_permission_set_1.save()

        submit_permission_set_2 = PermissionSet(
            permission_set_name="Power Permission Set",
            administration_assign_user_to_group=0,
            administration_create_group=0,
            administration_create_permission_set=0,
            administration_create_user=0,
            bug_client=4,
            customer=4,
            kanban_card=4,
            organisation=4,
            project=4,
            requirement=4,
            task=4,
            tag=4,
            document=1,
            kanban_note=1,
            project_note=1,
            task_note=1,
            requirement_note=1,
            requirement_item_note=1,
            change_user=request.user,
        )
        submit_permission_set_2.save()

        submit_permission_set_3 = PermissionSet(
            permission_set_name="Normal Permission Set",
            administration_assign_user_to_group=0,
            administration_create_group=0,
            administration_create_permission_set=0,
            administration_create_user=0,
            bug_client=3,
            customer=3,
            kanban_card=3,
            organisation=3,
            project=3,
            requirement=3,
            task=3,
            tag=3,
            document=1,
            kanban_note=1,
            project_note=1,
            task_note=1,
            requirement_note=1,
            requirement_item_note=1,
            change_user=request.user,
        )
        submit_permission_set_3.save()

        submit_permission_set_3 = PermissionSet(
            permission_set_name="Read Only Permission Set",
            administration_assign_user_to_group=0,
            administration_create_group=0,
            administration_create_permission_set=0,
            administration_create_user=0,
            bug_client=1,
            customer=1,
            kanban_card=1,
            organisation=1,
            project=1,
            requirement=1,
            task=1,
            tag=1,
            document=1,
            kanban_note=1,
            project_note=1,
            task_note=1,
            requirement_note=1,
            requirement_item_note=1,
            change_user=request.user,
        )
        submit_permission_set_3.save()

        # Create admin group
        submit_group = Group(
            group_name="Administration",
            change_user=request.user,
        )
        submit_group.save()

        # Add user to admin group
        submit_user_group = UserGroup(
            username=request.user,
            group=submit_group,
            permission_set=submit_permission_set_1,
            change_user=request.user,
        )
        submit_user_group.save()

        # Create no organisation
        submit_organisation = Organisation(
            organisation_name="No Organisation",
            organisation_website="https://nearbeach.org",
            organisation_email="noreply@nearbeach.org",
            change_user=request.user,
        )
        submit_organisation.save()

    request.session["is_superuser"] = request.user.is_superuser


def logout(request):
    # log the user out and go to login page
    auth.logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required(login_url="login", redirect_field_name="")
def permission_denied(request):
    # Load up the permission denied template and show user
    t = loader.get_template("NearBeach/authentication/permission_denied.html")

    # context
    c = {
        "nearbeach_title": "NearBeach Permission Denied",
    }

    return HttpResponse(t.render(c, request))


@check_permission_denied()
def test_permission_denied(request):
    """
    A simple test - ALWAYS respond with permission denied.
    This function will never return HttpResponse - because the decorator will raise PermissionDenied ALWAYS!!!
    """
    return HttpResponse("Hello World")
