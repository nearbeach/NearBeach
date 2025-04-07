from two_factor.views import ProfileView
from NearBeach.views.theme_views import get_theme


class TwoFactorProfileView(ProfileView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theme"] = get_theme(self.request)
        return context
