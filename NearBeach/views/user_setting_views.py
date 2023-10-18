from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http.response import HttpResponse, HttpResponseBadRequest
from NearBeach.forms import UserSettingsForm
from NearBeach.models import UserSetting


# Internal function
def create_user_settings(request, form):
    """

    """
    user_setting_create = UserSetting(
        username=request.user,
        setting_type=form.cleaned_data['setting_type'],
        setting_data=form.cleaned_data['setting_data'],
    )

    user_setting_create.save()


def delete_user_settings(request):
    # Get form data
    form = UserSettingsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Delete the data
    UserSetting.objects.filter(
        username=request.user,
        setting_type=form.cleaned_data['setting_type'],
    ).delete()

    return HttpResponse("")


# Internal function
def get_user_settings(request, setting_type):
    # Get form data

    # Get user settings data
    return UserSetting.objects.filter(
        username=request.user,
        setting_type=setting_type,
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def update_user_settings(request):
    # Get the form data from the request
    form = UserSettingsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the user data to update
    update_user_setting = UserSetting.objects.filter(
        username=request.user,
        setting_type=form.cleaned_data['setting_type'],
    )

    # Check to see if there is any data
    if len(update_user_setting) == 0:
        # The user settings don't exist. Make them instead of updating them
        create_user_settings(request, form)
        return HttpResponse("")

    update_user_setting.update(
        setting_data=form.cleaned_data['setting_data']
    )

    return HttpResponse("")

