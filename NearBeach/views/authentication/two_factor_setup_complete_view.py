from two_factor.views import SetupCompleteView
from NearBeach.views.theme_views import get_theme


class TwoFactorSetupCompleteView(SetupCompleteView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context["theme"] = get_theme(self.request)
        return context
