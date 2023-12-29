from NearBeach.models import UserSetting


# Internal function
def get_theme(request):
    user_setting_results = UserSetting.objects.filter(
        username=request.user,
        setting_type="theme",
    ).first()

    if user_setting_results is None:
        return "light"

    # Data structure should be { theme: <string> "" }
    return user_setting_results.setting_data['theme']


# Internal function
def update_theme(request, theme):
    # Grab data we are going to update
    user_settings_update = UserSetting.objects.filter(
        username=request.user,
        setting_type="theme",
    )

    # If there is no data - create the data instead of update
    if len(user_settings_update) == 0:
        create_user_settings = UserSetting(
            username=request.user,
            setting_type="theme",
            setting_data={"theme": theme}
        )
        create_user_settings.save()

        # Nothing else to do - return
        return

    # Update the theme
    user_settings_update.update(
        setting_data={"theme": theme},
    )

    # Nothing else to do
    return
