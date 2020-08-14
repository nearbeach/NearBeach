from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.user_permissions import return_user_permission_level

@login_required(login_url='login',redirect_field_name="")
def bug_list(request,destination,location_id):
    if not request.method == "POST":
        # Needs to be post
        return HttpResponseBadRequest("Sorry - needs to be done through psot")

    return HttpResponse("Hello World")