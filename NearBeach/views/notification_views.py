from django.http import HttpResponse
from django.template import loader
from NearBeach.views.theme_views import get_theme
from NearBeach.models import Notification


def new_notification(request):
    """
    :param request:
    :return:
    """
    t = loader.get_template("NearBeach/notifications/new_notification.html")

    # Context
    c = {
        "need_tinymce": False,
        "nearbeach_title": "New Notification",
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


def new_notification_save(request):
    return HttpResponse("")


def notification_information(request, notification_id):
    return HttpResponse("")


def notification_information_save(request, notification_id):
    return HttpResponse("")


