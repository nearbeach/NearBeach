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


@login_required(login_url='login',redirect_field_name="")
def new_task(request):
    """

    :param request:
    :return:
    """
    # ADD IN PERMISSIONS CHECKER

    # Template
    t = loader.get_template('NearBeach/tasks/new_task.html')

    # Context
    c = {}

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name='')
def new_task_save(request):
    """

    :param request:
    :return:
    """
    return HttpResponseBadRequest("WRITE THIS CODE")


@login_required(login_url='login',redirect_field_name="")
def task_information(request,task_id):
    """

    :param request:
    :param task_id:
    :return:
    """
    # ADD IN PERMISSIONS CHECKER

    # Template
    t = loader.get_template('NearBeach/tasks/task_information.html')

    # Context
    c = {}

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name='')
def task_information_save(request,task_id):
    """

    :param request:
    :param task_id:
    :return:
    """
    return HttpResponseBadRequest("GOT TO WRITE THE CODE")
