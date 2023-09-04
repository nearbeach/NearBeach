from NearBeach.forms import UserSettingsForm
from NearBeach.models import UserSetting
from NearBeach.views.user_setting_views import update_user_settings


# Internal function
def get_theme(request):
    user_setting_results = UserSetting.objects.filter(
        username=request.user,
        setting_type="theme",
    ).first()

    if user_setting_results is None:
        return ""

    # Data structure should be { theme: <string> "" }
    return user_setting_results.setting_data['theme']


# Internal function
def update_theme(request, theme):
    # Handles both creation and update
    # Create the form we require
    form = UserSettingsForm(
        initial={
            "setting_type": "theme",
            "setting_data": F"{{ 'theme': '{theme}' }}",
        }
    )

    # Send the data to update_user_settings
    # If we need to create a new setting - it is handled in the function
    return update_user_settings(request, form)

