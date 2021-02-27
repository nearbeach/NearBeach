from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.models import *

import json


@login_required(login_url='login',redirect_field_name="")
def permission_set_information(request, permission_set_id):
    """

    :param request:
    :param permission_set_id:
    :return:
    """

    # Add in permission checks

    # Import template
    t = loader.get_template('NearBeach/permission_sets/permission_set_information.html')

    # Get data
    permission_set_results = permission_set.objects.get(permission_set_id=permission_set_id)

    user_list_results = user_group.objects.filter(
        is_deleted=False,
        permission_set_id=permission_set_id,
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
        'permission_set_results': serializers.serialize('json', [permission_set_results]),
        'user_list_results': user_list_results,
        'permission_set_id': permission_set_id,
        'permission_boolean': json.dumps(PERMISSION_BOOLEAN),
        'permission_level': json.dumps(PERMISSION_LEVEL),
    }

    return HttpResponse(t.render(c, request))
