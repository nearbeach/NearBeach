from django.urls import path, include
from NearBeach.views.api_v1.authentication import (
    authentication_api_view,
    forgotten_password_api_view,
    two_factor_api_view,
)
from NearBeach.views.api_v1.page_not_found_api_view import PageNotFoundView


urlpatterns = [
    path('authentication/', authentication_api_view.AuthenticationView.as_view(), name='authentication'),
    path('authentication/forgotten-password/', forgotten_password_api_view.ForgottenPasswordView.as_view(), name='authentication'),
    path('authentication/two-factor/', two_factor_api_view.TwoFactorView.as_view(), name='authentication'),
    path("<path:_>", PageNotFoundView.as_view(), name="page_not_found"),
]
