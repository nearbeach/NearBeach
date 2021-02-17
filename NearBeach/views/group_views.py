from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers

from NearBeach.forms import SearchForm, NewGroupForm
from NearBeach.models import *


@login_required(login_url='login', redirect_field_name='')
@require_http_methods(['POST'])
def check_group_name(request):
    """

    :param request:
    :return:
    """

    # Check user form
    form = SearchForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Check to see if the group name exists
    group_name_results = group.objects.filter(
        is_deleted=False,
        group_name=form.cleaned_data['search'],
    )

    # Send back data
    return HttpResponse(serializers.serialize('json', group_name_results), content_type='application/json')


@login_required(login_url='login',redirect_field_name="")
def group_information(request, group_id):
    """

    :param request:
    :param group_id:
    :return:
    """
    return HttpResponse("")


@login_required(login_url='login',redirect_field_name="")
def new_group(request):
    """

    :param request:
    :return:
    """

    # CHeck user permissions

    # Get the template
    t = loader.get_template('NearBeach/groups/new_group.html')

    # Get group data
    group_results = group.objects.filter(
        is_deleted=False,
    )

    # Get the context
    c = {
        'group_results': serializers.serialize('json', group_results),
    }

    # Return
    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name='')
def new_group_save(request):
    """

    :param request:
    :return:
    """

    # Check user permissions

    # Get form data
    form = NewGroupForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create the new group
    group_submit = group(
        group_name=form.cleaned_data['group_name'],
        parent_group=form.cleaned_data['parent_group'],
        change_user=request.user,
    )
    group_submit.save()

    # Send back the URL for the group
    return HttpResponse(reverse('group_information',args={group_submit.group_id}))
