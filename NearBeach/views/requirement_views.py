from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.user_permissions import return_user_permission_level

def get_user_requirement_permissions(requirement_id):
    """
    Use the requirement_id and find out if the user has access to this requirement
    :param requirement_id:
    :return:
    """
    requirement_groups = object_assignment.objects.filter(
        is_deleted="FALSE",
        requirement_id=requirement_id
    ).values('group_id')

    return return_user_permission_level(request, requirement_groups, ['requirement','requirement_link'])


@login_required(login_url='login',redirect_field_name="")
def new_requirement(request, location_id="", destination=""):
    """
    Loads the new requirement page
    :param request:
    :param location_id:
    :param destination:
    :return:
    """
    #Load template
    t = loader.get_template('NearBeach/requirements/new_requirements.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))

@login_required(login_url='login',redirect_field_name="")
def requirement_information(request, requirement_id):
    """
    Loads the requirement information.
    :param request:
    :param requirement_id:
    :return:
    """
    # Get the requirement information
    requirement_results = requirement.objects.get(requirement_id=requirement_id)

    # Check the permissions
    permission_results = get_user_requirement_permissions(requirement_id)

    # If user has no permissions to this requirement send them to the appropriate location
    if permission_results['requirement'] == 0:
        # Users who create the requirement get at least read only
        if requirement_results.creation_user == request.user:
            return HttpResponseRedirect(reverse('requirement_readonly', args={requirement_id}))

        # Users who did not create the requirement get sent to permission denied.
        return HttpResponseRedirect(reverse('permission_denied'))


    # If the requirement has been closed - send user to the read only section
    if requirement_results.requirement_status.requirement_status == "Completed":
        return HttpResponseRedirect(reverse('requirement_readonly', args={requirement_id}))


    #Load template
    t = loader.get_template('NearBeach/requirements/requirement_information.html')

    # context
    c = {
        'requirement_results': requirement_results,
        'requirement_id': requirement_id,
        'permission_results': permission_results,
    }

    return HttpResponse(t.render(c, request))