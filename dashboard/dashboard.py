from NearBeach.models import *

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


@login_required(login_url='login')
def active_projects(request):
    #Get data


    # Load the template
    t = loader.get_template('NearBeach/active_projects.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def active_tasks(request):
    # Get data


    # Load the template
    t = loader.get_template('NearBeach/active_tasks.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))