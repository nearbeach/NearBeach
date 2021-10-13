from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.forms import User, UpdateUserForm
# from NearBeach.models import *

import json


@login_required(login_url='login', redirect_field_name="")
def profile_information(request):
    """
    """
    # Get user data
    user_results = User.objects.filter(
        username=request.user
    ).values(
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )

    # Get template
    t = loader.get_template('NearBeach/profile/profile_information.html')

    # Construct Context
    c = {
        'user_results': json.dumps(list(user_results), cls=DjangoJSONEncoder),
        'username': request.user.id,
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def update_data(request):
    """
    """
    # Get form data
    form = UpdateUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Extract out the user results
    user_update = request.user
    user_update.first_name = form.cleaned_data['first_name']
    user_update.last_name = form.cleaned_data['last_name']
    user_update.save()

    return HttpResponse("")
