from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.models import *

import json

@login_required(login_url='login',redirect_field_name="")
def user_information(request, username):
    """

    :param request:
    :param permission_set_id:
    :return:
    """

    # check user permissions

    # Import template
    t = loader.get_template('NearBeach/users/user_information.html')

    # Get user data
    user_results = User.objects.get(id=username)

    user_list_results = user_group.objects.filter(
        is_deleted=False,
        username=username,
    ).values(
        'username',
        'username__first_name',
        'username__last_name',
        'username__email',
        'group',
        'group__group_name',
        'permission_set',
        'permission_set__permission_set_name',
    ).order_by(
        'username__first_name',
        'username__last_name',
        'permission_set__permission_set_name',
    )
    user_list_results = json.dumps(list(user_list_results), cls=DjangoJSONEncoder)

    # Create the context
    c = {
        'user_list_results': user_list_results,
        'user_results': user_results,
        'username': username,
    }

    return HttpResponse(t.render(c, request))