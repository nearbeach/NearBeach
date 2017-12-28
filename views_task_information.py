"""
VIEWS - task information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the TASK INFORMATION MODULES. This is to help keep the VIEWS
file clean from AJAX (spray and wipe).
"""

from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import  loader
from NearBeach.forms import *
from .models import *
from .namedtuplefetchall import *


@login_required(login_url='login')
def information_task_assigned_users(request, task_id):
    #Load template
    t = loader.get_template('NearBeach/task_information/task_assigned_users.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_costs(request, task_id):
    #Load template
    t = loader.get_template('NearBeach/task_information/task_costs.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_customers(request, task_id):
    #Load template
    t = loader.get_template('NearBeach/task_information/task_customers.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_task_history(request, task_id):
    #Load template
    t = loader.get_template('NearBeach/task_information/task_history.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))



