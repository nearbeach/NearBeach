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
from .misc_functions import *
from .user_permissions import return_user_permission_level

@login_required(login_url='login')
def whiteboard_common_xml(request):
    #Load xml template
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_common.xml')

    # context
    c = {}

    return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_graph_xml(request):
    #Load xml template
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_graph.xml')

    # context
    c = {}

    return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_editor_xml(request):
    #Load xml template
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_editor.xml')

    # context
    c = {}

    return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')


@login_required(login_url='login')
def whiteboard_information(request):

    #Load template
    t = loader.get_template('NearBeach/whiteboard/whiteboard_information.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def whiteboard_toolbar_xml(request):
    #Load xml template
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_toolbar.xml')

    # context
    c = {}

    return HttpResponse(t.render(c,request), content_type='application/xhtml+xml')

