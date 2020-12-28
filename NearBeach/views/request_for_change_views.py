from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers

from NearBeach.models import *

@login_required(login_url='login', redirect_field_name="")
def new_request_for_change(request):
    """

    :param request:
    :return:
    """

    # CHECK USER PERMISSIONS

    # Get template
    t = loader.get_template('NearBeach/request_for_change/new_request_for_change.html')

    # Get data
    group_results = group.objects.filter(
        is_deleted=False,
    )

    user_results = User.objects.filter( #This should only be group leaders
        is_active=True,
    )

    # Context
    c = {
        'group_results': serializers.serialize('json', group_results),
        'user_results': serializers.serialize('json', user_results),
    }

    return HttpResponse(t.render(c,request))