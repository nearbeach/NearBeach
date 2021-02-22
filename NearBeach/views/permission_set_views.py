from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from NearBeach.models import *


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name="")
def permission_set_information(request, permission_set_id):
    """

    :param request:
    :param permission_set_id:
    :return:
    """

    # Add in permission checks

    # Import template

