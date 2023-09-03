from NearBeach.models import UserSetting


# Internal function
def get_theme(request):
    user_setting_results = UserSetting.objects.filter(
        username=request.username,
        setting_type="theme",
    ).first()

    if user_setting_results is None:
        return ""

    # Data structure should be { theme: <string> "" }
    return user_setting_results.setting_data['theme']
