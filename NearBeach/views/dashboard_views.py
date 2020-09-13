# Import Forms
from ..forms import *

# Import Django Libraries
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


# Import Python Libraries
import json, urllib.parse, random

# Import user permission library
from ..user_permissions import return_user_permission_level

@login_required(login_url='login',redirect_field_name="")
def dashboard(request):
    """
    Due to a bug - if the user goes to /admin/ and logs in there, they will by pass this one session request. It is
    placed here to make sure. :)
    """
    request.session['is_superuser'] = request.user.is_superuser

    #Get user's default permissions
    permission_results = return_user_permission_level(request, None, 'project')

    # Load the template
    t = loader.get_template('NearBeach/dashboard/dashboard.html')

    # context
    c = {
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))