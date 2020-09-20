from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.user_permissions import return_user_permission_level
from django.views.decorators.http import require_http_methods


import json


@login_required(login_url='login',redirect_field_name="")
def new_customer(request):
    """

    :param request:
    :return:
    """
    # Get user permission

    # Get templates
    t = loader.get_template('NearBeach/customers/new_customers.html')

    # Get Context
    c = {}

    return HttpResponse(t.render(c,request))