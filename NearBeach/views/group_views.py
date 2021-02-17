from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.decorators import login_required


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

    # Get the context
    c = {}

    # Return
    return HttpResponse(t.render(c, request))

