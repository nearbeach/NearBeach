from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@login_required(login_url='login', redirect_field_name="")
def new_request_for_change(request):
    """

    :param request:
    :return:
    """

    # CHECK USER PERMISSIONS

    # Get template
    t = loader.get_template('NearBeach/request_for_change/new_request_for_change.html')

    # Context
    c = {}

    return HttpResponse(t.render(c,request))