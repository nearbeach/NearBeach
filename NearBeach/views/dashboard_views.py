# Import Forms
from ..forms import *

# Import Django Libraries
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count

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


@login_required(login_url='login',redirect_field_name="")
@require_http_methods(['POST'])
def get_bug_list(request):
    """

    :param request:
    :return:
    """
    bug_results = bug.objects.filter(
        is_deleted=False,
        # Add in ability to tell if bugs are opened or closed
    ).values('bug_status').annotate(Count("bug_status"))

    # Send back json data
    json_results = json.dumps(list(bug_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')

