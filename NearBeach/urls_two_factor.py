from django.apps.registry import apps
from django.urls import include, path

from two_factor.views import (
    BackupTokensView,
    DisableView,
    ProfileView,
    QRGeneratorView,
    SetupCompleteView,
)

from .views.authentication.two_factor_backup_tokens_view import TwoFactorBackupTokensView
from .views.authentication.two_factor_disable_view import TwoFactorDisableView
from .views.authentication.two_factor_profile_view import TwoFactorProfileView
from .views.authentication.two_factor_setup_view import TwoFactorSetupView
from .views.authentication.two_factor_setup_complete_view import TwoFactorSetupCompleteView

core = [
    path(
        'profile_information/two_factor/setup/',
        # SetupView.as_view(),
        TwoFactorSetupView.as_view(),
        name='setup',
    ),
    path(
        'profile_information/two_factor/qrcode/',
        QRGeneratorView.as_view(),
        name='qr',
    ),
    path(
        'profile_information/two_factor/setup/complete/',
        # SetupCompleteView.as_view(),
        TwoFactorSetupCompleteView.as_view(),
        name='setup_complete',
    ),
    path(
        'profile_information/two_factor/backup/tokens/',
        # BackupTokensView.as_view(),
        TwoFactorBackupTokensView.as_view(),
        name='backup_tokens',
    ),
]

profile = [
    path(
        'profile_information/two_factor/',
        # ProfileView.as_view(),
        TwoFactorProfileView.as_view(),
        name='profile',
    ),
    path(
        'profile_information/two_factor/disable/',
        # DisableView.as_view(),
        TwoFactorDisableView.as_view(),
        name='disable',
    ),
]

plugin_urlpatterns = []
for app_config in apps.get_app_configs():
    if app_config.name.startswith('two_factor.plugins.'):
        # Phonenumber used to be include in the two_factor core. Because we
        # don't want to change the url names and break backwards compatibility
        # we keep the urls of the phonenumber plugin in the core two_factor
        # namespace.
        if app_config.name == 'two_factor.plugins.phonenumber':
            namespace = None
        else:
            namespace = app_config.label
        try:
            plugin_urlpatterns.append(
                path(
                    f'account/two_factor/{app_config.url_prefix}/',
                    include(f'{app_config.name}.urls', namespace)
                ),
            )
        except AttributeError:
            pass

urlpatterns = (core + profile + plugin_urlpatterns, 'two_factor')
