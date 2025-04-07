from two_factor.views import SetupView
from NearBeach.views.theme_views import get_theme

# TODO: Fix the templates for the profile information two factor


class TwoFactorSetupView(SetupView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["theme"] = get_theme(self.request)
        return context
