from two_factor.views import BackupTokensView
from NearBeach.views.theme_views import get_theme


class TwoFactorBackupTokensView(BackupTokensView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["theme"] = get_theme(self.request)
        return context
