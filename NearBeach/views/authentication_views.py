# Import Forms
from ..forms import *

# Import Django Libraries
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from random import SystemRandom
from django.db.models import Count

# Import Python Libraries
import json, urllib.parse, random

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
    if not permission_set.objects.all():
        # Create administration permission_set
        submit_permission_set = permission_set(
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
            document=1,
            kanban_comment=1,
            project_history=1,
            task_history=1,
            change_user=request.user,
        )
        submit_permission_set.save()

        # Create admin group
        submit_group = group(
            group_name="Administration",
            change_user=request.user,
        )
        submit_group.save()

        # Add user to admin group
        submit_user_group = user_group(
            username=request.user,
            group=group.objects.get(group_id=1),
            permission_set=permission_set.objects.get(permission_set_id=1),
            change_user=request.user,
        )
        submit_user_group.save()

    request.session['is_superuser'] = request.user.is_superuser


def check_recaptcha(post_data):
    """
    Determine if the user has setup the recaptcha in the settings.py file, and then check the result against google.
    :param post_data:
    :return:
    """
    if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY') and hasattr(settings, 'RECAPTCHA_PRIVATE_KEY'):
        RECAPTCHA_PRIVATE_KEY = settings.RECAPTCHA_PRIVATE_KEY
    else:
        #User has not setup recaptcha - return true
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
    recaptcha_response = post_data.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': RECAPTCHA_PRIVATE_KEY,
        'response': recaptcha_response
    }

    """
    SECURITY ISSUE
    ~~~~~~~~~~~~~~
    The URL could contain a file. Which we do not want executed by mistake. So we just make sure that the URL starts
    with a http instead of ftp or file.

    We place the  at the end of the json_data because we have checked the field. This should be just a json 
    response. If it is not at this point then it will produce a server issue.
    """
    if url.lower().startswith('http'):
        req = urllib.request.Request(url)
    else:
        raise ValueError from None

    with urllib.request.urlopen(req, urllib.parse.urlencode(values).encode('utf8')) as response:  # nosec
        result = json.load(response)

        # Check to see if the user is a robot. Success = human
    if result['success']:
        return True
    else:
        return False

def login(request):
    """
	For some reason I can not use the varable "LoginForm" here as it is already being used.
	Instead I will use the work form.

	The form is declared at the start and filled with either the POST data OR nothing. If this
	process is called in POST, then the form will be checked and if it passes the checks, the
	user will be logged in.

	If the form is not in POST (aka GET) OR fails the checks, then it will create the form with
	the relevant errors.
	"""
    form = LoginForm(request.POST or None)

    # POST
    if request.method == 'POST':
        if form.is_valid():
            # Check if user passes recaptcha
            if check_recaptcha(request.POST) == True:
                # Looks like we can authenticate the user
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                # Check to see if user exists AND has more than one group assigned
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)

            # Just double checking. :)
            if request.user.is_authenticated:
                #Check to make sure it isn't first time login -> need to setup functionalities
                check_first_time_login(request)

                # Check how many groups user is in
                user_group_count = len(user_group.objects.filter(
                    is_deleted=False,
                    username_id=User.objects.get(username=username).id,
                ))

                if user_group_count == 0:
                    return HttpResponseRedirect(reverse('logout'))

                return HttpResponseRedirect(reverse('dashboard'))

    # Get recaptcha public key
    if hasattr(settings, 'RECAPTCHA_PUBLIC_KEY') and hasattr(settings, 'RECAPTCHA_PRIVATE_KEY'):
        RECAPTCHA_PUBLIC_KEY = settings.RECAPTCHA_PUBLIC_KEY
    else:
        RECAPTCHA_PUBLIC_KEY = ''

    # load template
    t = loader.get_template('NearBeach/authentication/login.html')

    # Get random number
    cryptogen = SystemRandom()

    # context
    c = {
        'LoginForm': form,
        'RECAPTCHA_PUBLIC_KEY': RECAPTCHA_PUBLIC_KEY,
        'image_number': '%(number)03d' % {'number': 1 + cryptogen.randrange(1,19)},
    }

    return HttpResponse(t.render(c, request))


def logout(request):
    # log the user out and go to login page
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login',redirect_field_name="")
def permission_denied(request):
    # Load the template
    t = loader.get_template('NearBeach/authentication/permission_denied.html')

    # context
    c = {
    }

    return HttpResponse(t.render(c, request))
