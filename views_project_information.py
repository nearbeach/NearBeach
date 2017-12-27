"""
VIEWS - project information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the PROJECT INFORMATION MODULES. This is to help keep the VIEWS
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


@login_required(login_url='login')
def information_project_history(request, project_id):
    print("Information Project History")
    if request.method == "POST":
        form = information_project_history_form(request.POST, request.FILES)
        if form.is_valid():
            project_history_results = form.cleaned_data['project_history']

            if not project_history_results == '':
                current_user = request.user

                project_id_instance = project.objects.get(pk=project_id)

                data = project_history(
                    project_id=project_id_instance,
                    user_id=current_user,
                    project_history=project_history_results,
                    user_infomation=current_user.id,
                    change_user = request.user,
                )
                data.save()
        else:
            print(form.errors)

    project_history_results = project_history.objects.filter(
        project_id=project_id,
        is_deleted="FALSE",
    )

    #Return a blank page for fun
    t = loader.get_template('NearBeach/project_information/project_history.html')

    # context
    c = {
        'information_project_history_form': information_project_history_form(),
        'project_history_results': project_history_results,
        'project_id': project_id,
    }

    return HttpResponse(t.render(c, request))
    #SoMuchFun

