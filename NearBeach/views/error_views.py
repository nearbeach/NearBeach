from django.http import HttpResponseForbidden, Http404, HttpResponseServerError
from django.template import loader
from django.contrib.auth.decorators import login_required


@login_required(login_url='login', redirect_field_name="")
def error_403(request, exception):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    t = loader.get_template('403.html')

    c = {
        'nearbeach_title': 'NearBeach Forbidden',
    }

    return HttpResponseForbidden(t.render(c, request))


@login_required(login_url='login', redirect_field_name="")
def error_404(request, exception):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    t = loader.get_template('404.html')

    c = {
        'nearbeach_title': 'NearBeach Not Found',
    }

    return Http404(t.render(c, request))


@login_required(login_url='login', redirect_field_name="")
def error_500(request):
    """
    :param request:
    :param destination:
    :param location_id:
    :return:
    """
    t = loader.get_template('500.html')

    c = {
        'nearbeach_title': 'NearBeach Server Error',
    }

    return HttpResponseServerError(t.render(c, request))
