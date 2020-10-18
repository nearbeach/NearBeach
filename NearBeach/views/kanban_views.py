import urllib

from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.views.tools.internal_functions import *
from NearBeach.user_permissions import return_user_permission_level

import json, urllib3


def new_kanban(request):
    """

    :param request:
    :return:
    """

    # Check user permissions

    # Get tempalte
    t = loader.get_template('NearBeach/kanban/new_kanban.html')

    # Context
    c = {}

    return HttpResponse(t.render(c,request))


def new_kanban_save(request):
    """

    :param request:
    :return:
    """
    return HttpResponseBadRequest("HELLO WORLD")