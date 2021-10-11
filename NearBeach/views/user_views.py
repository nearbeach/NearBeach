from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User

from NearBeach.forms import NewUserForm, PasswordResetForm, UpdateUserForm
from NearBeach.models import user_group

import json

@login_required(login_url='login', redirect_field_name="")
def new_user(request):
    """
    :param request:
    :return:
    """
    # Add in user permissions

    # Get template
    t = loader.get_template('NearBeach/users/new_user.html')

    # Get context
    c = {
        'nearbeach_title': 'New User',
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def new_user_save(request):
    """
    :param request:
    :return:
    """
    # CHECK USER PERMISSSIONS

    # Get form data
    form = NewUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create the new user
    submit_user = User(
        username=form.cleaned_data['username'],
        email=form.cleaned_data['email'],
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        is_active=True,
    )

    # Set the user password
    submit_user.set_password(form.cleaned_data['password1'])

    # Save
    submit_user.save()

    return HttpResponse(reverse('user_information', args={submit_user.id}))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def update_password(request):
    """
    """
    # Get form data
    form = PasswordResetForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Check to make sure we are updating ONLY the current user
    if not form.cleaned_data['username'] == request.user:
        return HttpResponseBadRequest("Unknown Error")

    # Get the User object
    user_update = form.cleaned_data['username']
    user_update.set_password(form.cleaned_data['password'])
    user_update.save()

    return HttpResponse("")


@login_required(login_url='login', redirect_field_name="")
def user_information(request, username):
    """
    :param request:
    :param permission_set_id:
    :return:
    """
    # check user permissions

    # Import template
    t = loader.get_template('NearBeach/users/user_information.html')

    # Get user data
    user_results = User.objects.get(id=username)

    user_list_results = user_group.objects.filter(
        is_deleted=False,
        username=username,
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
    user_list_results = json.dumps(list(user_list_results), cls=DjangoJSONEncoder)

    # Create the context
    c = {
        'nearbeach_title': 'User Information %s' % username,
        'user_list_results': user_list_results,
        'user_results': serializers.serialize('json', [user_results]),
        'username': username,
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def user_information_save(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    # Add in user permissions

    # Get form
    form = UpdateUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get user
    update_user = User.objects.get(id=username)

    # Update the user
    update_user.first_name = form.cleaned_data['first_name']
    update_user.last_name = form.cleaned_data['last_name']
    update_user.email = form.cleaned_data['email']
    update_user.is_active = form.cleaned_data['is_active']
    update_user.is_superuser = form.cleaned_data['is_superuser']

    # Save
    update_user.save()

    # Send back blank 200
    return HttpResponse("")
