from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.forms import SearchForm, NewGroupForm
from NearBeach.models import group, user_group

import json


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
        group_name__icontains=form.cleaned_data['search'],
    )

    # Send back data
    return HttpResponse(serializers.serialize('json', group_name_results), content_type='application/json')


@login_required(login_url='login', redirect_field_name="")
def group_information(request, group_id):
    """
    :param request:
    :param group_id:
    :return:
    """
    # Get the template
    t = loader.get_template('NearBeach/groups/group_information.html')

    # Get the data we want
    group_results = group.objects.get(group_id=group_id)
    parent_group_results = group.objects.filter(
        is_deleted=False,
    )

    user_list_results = user_group.objects.filter(
        is_deleted=False,
        group_id=group_id,
    ).values(
        'username',
        'username__first_name',
        'username__last_name',
        'username__email',
        'group',
        'group__group_name',
        'permission_set',
        'permission_set__permission_set_name',
    ).order_by(
        'username__first_name',
        'username__last_name',
        'permission_set__permission_set_name',
    )

    # Convert into json
    user_list_results = json.dumps(list(user_list_results), cls=DjangoJSONEncoder)

    # Context
    c = {
        'group_id': group_id,
        'group_results': serializers.serialize('json', [group_results]),
        'nearbeach_title': 'Group Information %s' % group_id,
        'parent_group_results': serializers.serialize('json', parent_group_results),
        'user_list_results': user_list_results,
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name='')
def group_information_save(request, group_id):
    """
    :param request:
    :param group_id:
    :return:
    """
    # Check user permissions

    # Get Form Data
    form = NewGroupForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return HttpResponseBadRequest(form.errors)

    # Update the group's data
    group_update = group.objects.get(group_id=group_id)
    group_update.group_name = form.cleaned_data['group_name']
    group_update.parent_group = form.cleaned_data['parent_group']

    group_update.save()

    return HttpResponse("")


@login_required(login_url='login', redirect_field_name="")
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
    ).exclude(
        group_name__in=['Administration'],
    )

    # Get the context
    c = {
        'group_results': serializers.serialize('json', group_results),
        'nearbeach_title': 'New Group',
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
    return HttpResponse(reverse('group_information', args={group_submit.group_id}))
