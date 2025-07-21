from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.template import loader
from NearBeach.views.theme_views import get_theme
from NearBeach.models import Notification
from NearBeach.forms import NotificationForm, NotificationDeleteForm
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
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


@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def new_notification_save(request):
    """
    :param request:
    :return:
    """
    form = NotificationForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    submit_notification = Notification(
        notification_header=form.cleaned_data["notification_header"],
        notification_message=form.cleaned_data["notification_message"],
        notification_location=form.cleaned_data["notification_location"],
        notification_start_date=form.cleaned_data["notification_start_date"],
        notification_end_date=form.cleaned_data["notification_end_date"],
    )
    submit_notification.save()

    # Return notification url back to user
    return HttpResponse(
        reverse("notification_information", args=[submit_notification.notification_id])
    )


@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def notification_information(request, notification_id):
    # Get template
    t = loader.get_template("NearBeach/notifications/notification_information.html")

    # Notification data - 404 if does not exist
    notification_results = Notification.objects.filter(is_deleted=False)
    notification_results = get_object_or_404(
        notification_results,
        notification_id=notification_id,
    )

    # Context
    c = {
        "nearbeach_title": f"Notification {notification_id}",
        "need_tinymce": False,
        "notification_results": serializers.serialize("json",[notification_results]),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def notification_information_delete(request):
    form = NotificationDeleteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update the data
    notification_id = form.cleaned_data['notification_id']

    Notification.objects.filter(
        notification_id=notification_id.notification_id,
    ).update(
        is_deleted=True,
    )

    return HttpResponse("")


@user_passes_test(lambda u: u.is_superuser, login_url="/", redirect_field_name=None)
def notification_information_save(request, notification_id):
    form = NotificationForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    update_notification = Notification.objects.get(
        notification_id=notification_id,
    )

    # Update the data
    update_notification.notification_header = form.cleaned_data["notification_header"]
    update_notification.notification_message = form.cleaned_data["notification_message"]
    update_notification.notification_location = form.cleaned_data["notification_location"]
    update_notification.notification_start_date = form.cleaned_data["notification_start_date"]
    update_notification.notification_end_date = form.cleaned_data["notification_end_date"]
    update_notification.save()

    return HttpResponse("")


