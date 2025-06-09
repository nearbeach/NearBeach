# Import Django Libraries
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from NearBeach.decorators.check_user_permissions.permission_denied import check_permission_denied
from NearBeach.utils.admin import initalize_base_values


User = get_user_model()


def check_first_time_login(request):
    """Will initalize values if they do not exist
        These values consist of
            - Permission Sets
            - Admin Group
            - Admin UserGroup
            - "No Organisation" Organisation
    """
    initalize_base_values(request.user)
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
