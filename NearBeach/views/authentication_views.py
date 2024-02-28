# Import Forms
from django.contrib.auth import get_user_model
from ..forms import PermissionSet, Group, LoginForm
from ..models import UserGroup, Notification, Organisation
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
            kanban_card=4,
            organisation=4,
            project=4,
            requirement=4,
            task=4,
            tag=4,
            document=1,
            kanban_comment=1,
            project_history=1,
            task_history=1,
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
            kanban_comment=1,
            project_history=1,
            task_history=1,
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
            kanban_comment=1,
            project_history=1,
            task_history=1,
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
            kanban_comment=1,
            project_history=1,
            task_history=1,
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


def check_recaptcha(post_data):
    """
    Determine if the user has setup the recaptcha in the settings.py file, and then check the result against google.
    :param post_data: data from user's POST
    :return:
    """
    if hasattr(settings, "RECAPTCHA_PUBLIC_KEY") and hasattr(
        settings, "RECAPTCHA_PRIVATE_KEY"
    ):
        RECAPTCHA_PRIVATE_KEY = settings.RECAPTCHA_PRIVATE_KEY
    else:
        # User has not setup recaptcha - return true
        return True

    """
    As the Google documentation states. I have to send the request back to
    the given URL. It gives back a JSON object, which will contain the
    success results.

    Method
    ~~~~~~
    1.) Collect the variables
    2.) With the data - encode the variables into URL format
    3.) Send the request to the given URL
    4.) The response will open and store the response from GOOGLE
    5.) The results will contain the JSON Object
    """
    recaptcha_response = post_data.get("g-recaptcha-response")
    url = "https://www.google.com/recaptcha/api/siteverify"
    values = {"secret": RECAPTCHA_PRIVATE_KEY, "response": recaptcha_response}

    """
    SECURITY ISSUE
    ~~~~~~~~~~~~~~
    The URL could contain a file. Which we do not want executed by mistake. So we just make sure that the URL starts
    with a http instead of ftp or file.

    We place the  at the end of the json_data because we have checked the field. This should be just a json
    response. If it is not at this point then it will produce a server issue.
    """
    if url.lower().startswith("http"):
        req = urllib.request.Request(url)
    else:
        raise ValueError from None

    with urllib.request.urlopen(
        req, urllib.parse.urlencode(values).encode("utf8")
    ) as response:  # nosec
        result = json.load(response)

    # Check to see if the user is a robot. Success = human
    if result["success"]:
        return True
    return False


def login(request):
    """
    Will either log user in (if POST is submitted) or take the user to the login screen.

    The form is declared at the start and filled with either the POST data OR nothing. If this
    process is called in POST, then the form will be checked and if it passes the checks, the
    user will be logged in.

    If the form is not in POST (aka GET) OR fails the checks, then it will create the form with
    the relevant errors.
    """
    error_message = ""

    form = LoginForm(request.POST or None)

    # POST
    if request.method == "POST" and form.is_valid():
        # Create empty user - it will be false
        user = False

        # Check if user passes recaptcha
        if check_recaptcha(request.POST) is True:
            # Looks like we can authenticate the user
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Check to see if user exists AND has more than one group assigned
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)

        # Just double-checking. :)
        if request.user.is_authenticated:
            # Check to make sure it isn't first time login -> need to setup functionalities
            check_first_time_login(request)

            # Check how many groups user is in
            user_group_count = len(
                UserGroup.objects.filter(
                    is_deleted=False,
                    username=user,
                )
            )

            # if user_group_count == 0:
            #     return HttpResponseRedirect(reverse('logout'))
            if user_group_count > 0:
                return HttpResponseRedirect(reverse("dashboard"))

            # User has actually failed to log in. We will purposly log them out
            # And make sure we tell them why
            auth.logout(request)
            error_message = "Please contact your System Administrator. You do not have any associated Groups"
        else:
            # User is not logged in - tell the front end
            error_message = "Username or Password is incorrect. Please try again"

    # Get recaptcha public key
    if hasattr(settings, "RECAPTCHA_PUBLIC_KEY") and hasattr(
        settings, "RECAPTCHA_PRIVATE_KEY"
    ):
        RECAPTCHA_PUBLIC_KEY = settings.RECAPTCHA_PUBLIC_KEY
    else:
        RECAPTCHA_PUBLIC_KEY = ""

    # load template
    t = loader.get_template("NearBeach/authentication/login.html")

    # Get notification results
    notification_results = Notification.objects.filter(
        Q(
            is_deleted=False,
            notification_start_date__lte=datetime.datetime.now().date(),
            notification_end_date__gte=datetime.datetime.now().date(),
        )
        & Q(Q(notification_location="all") | Q(notification_location="login"))
    )

    # Get random number
    cryptogen = SystemRandom()

    # context
    c = {
        "error_message": error_message,
        "LoginForm": form,
        "nearbeach_title": "NearBeach Login",
        "notification_results": notification_results,
        "RECAPTCHA_PUBLIC_KEY": RECAPTCHA_PUBLIC_KEY,
        "image_number": f"{1 + cryptogen.randrange(1, 19):03.0f}",
    }

    return HttpResponse(t.render(c, request))


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
