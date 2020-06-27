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
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.template import loader
from NearBeach.forms import *
from .models import *
from django.db.models import Q
from .misc_functions import *
from .user_permissions import return_user_permission_level
from django.shortcuts import get_object_or_404

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
def whiteboard_information(request,whiteboard_id):
    """
    Whiteboard information
    ~~~~~~~~~~~~~~~~~~~~~~
    Permission: We need to get the groups connected to the whiteboard. For example if the whiteboard is connected to a
    task - we need to get that task's group ID.
    :param request:
    :return:
    """
    document_results = document.objects.get(
        is_deleted="FALSE",
        whiteboard_id=whiteboard_id
    )

    document_permission_results = document_permission.objects.filter(
        is_deleted="FALSE",
        document_key=document_results,
    )

    whiteboard_group_results = object_assignment.objects.filter(
        Q(
            is_deleted="FALSE",
            #group_id__isnull=False,
        ) & Q(
            Q(
                #Get the groups from task id
                task_id__in=document_permission_results.filter(
                    task_id__isnull=False,
                ).values('task_id')
            ) | Q(
                #Get the groups from project
                project_id__in=document_permission_results.filter(
                    project_id__isnull=False,
                ).values('project_id')
            ) | Q(
                #Get the groups from requirements
                requirement_id__in=document_permission_results.filter(
                    requirement_id__isnull=False,
                ).values('requirement_id')
            ) | Q(
                #Get the groups from RFC
                request_for_change__in=document_permission_results.filter(
                    request_for_change__isnull=False,
                ).values('request_for_change')
            ) | Q(
                #Get the groups from opportunity
                opportunity_id__in=document_permission_results.filter(
                    opportunity_id__isnull=False,
                ).values('opportunity_id')
            )
        )
    ).values('group_id')



    permission_results = return_user_permission_level(
        request,
        whiteboard_group_results,
        [
            'project',
            'task',
            'requirement',
            'request_for_change',
            'opportunity',
            'customer',
            'organisation',
        ]
    )

    # If whiteboard is connected to either customer or organisation - we do
    # not need to check the user permissions. As everyone should have access
    # to the whiteboard.
    bypass_permissions = len(object_assignment.objects.filter(
        Q(
            is_deleted="FALSE",
            whiteboard_id=whiteboard_id,
        ) & Q(
            Q(
                # Has customer associated
                customer_id__isnull=False,
            ) | Q(
                # Has organisation associated
                organisation_id__isnull=False,
            )
        )
    ))

    # If bypass_permissions > 0 - then we do not need to check
    # permissions as whiteboard is on customer or organisation
    if bypass_permissions == 0:
        #Check the permissions
        if permission_results['project'] == 0 and \
            permission_results['task'] == 0 and \
            permission_results['requirement'] == 0 and \
            permission_results['request_for_change'] == 0 and \
            permission_results['opportunity'] == 0:
            # Send them to permission denied!!
            return HttpResponseRedirect(reverse('permission_denied'))

    #Get whiteboard information
    whiteboard_results = get_object_or_404(whiteboard, whiteboard_id=whiteboard_id)

    #Load template
    t = loader.get_template('NearBeach/whiteboard/whiteboard_information.html')

    # context
    c = {
        'whiteboard_results': whiteboard_results,
        'whiteboard_id': whiteboard_id,
        'permission_results': permission_results,
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def whiteboard_save(request,whiteboard_id):
    if request.method == "POST":

        #ADD CODE - PERMISSIONS CHECK PERMISSIONS

        #Get the data we want to update

        whiteboard_update = whiteboard.objects.get(whiteboard_id=whiteboard_id)
        whiteboard_update.whiteboard_xml = request.POST['whiteboard_xml']
        whiteboard_update.save()

        #Return blank page

        t = loader.get_template('NearBeach/blank.html')

        c = {}

        return HttpResponse(t.render(c,request))
    else:
        return HttpResponseBadRequest("Sorry, this function only requests POST")



@login_required(login_url='login')
def whiteboard_toolbar_xml(request):
    print("Made contact with Whiteboard POST :)")

    #Load xml template
    t = loader.get_template('NearBeach/whiteboard/configuration/whiteboard_toolbar.xml')

    # context
    c = {}

    return HttpResponse(t.render(c,request), content_type='application/xhtml+xml')

