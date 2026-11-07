from django.urls import path
from NearBeach.views.api_v1.authentication import (
    authentication_api_view,
    forgotten_password_api_view,
    oidc_api_view,
    password_reset_api_view,
)
from NearBeach.views.api_v1.user import (
    user_initial_data_api_view,
)
from NearBeach.views.api_v1.page_not_found_api_view import PageNotFoundView

urlpatterns = [
    path('authentication/', authentication_api_view.AuthenticationView.as_view(), name='authentication'),
    path('authentication/forgotten-password/', forgotten_password_api_view.ForgottenPasswordView.as_view(),
         name='authentication'),
    path('authentication/reset-password/', password_reset_api_view.PasswordResetView.as_view(), name='authentication'),
    path('authentication/oidc/providers/', oidc_api_view.OidcProvidersView.as_view(), name='oidc-providers'),
    path('authentication/oidc/<slug:slug>/login/', oidc_api_view.OidcLoginView.as_view(), name='oidc-login'),
    path('authentication/oidc/<slug:slug>/callback/', oidc_api_view.OidcCallbackView.as_view(), name='oidc-callback'),
    path('user/initial_data/', user_initial_data_api_view.UserInitialDataView.as_view(), name='user-initial-data'),
    path("<path:_>", PageNotFoundView.as_view(), name="page_not_found"),
]
