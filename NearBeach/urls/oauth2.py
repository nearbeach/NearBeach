"""URL patterns for NearBeach's OAuth2 provider

Only the protocol endpoints are exposed. django-oauth-toolkit's own application management pages are left out on
purpose - they let any signed-in user register an application. Applications are managed in the Django admin site.
"""
from django.urls import path
from oauth2_provider import views

from NearBeach.utils.oauth2.views import ThrottledTokenView

app_name = "oauth2_provider"

urlpatterns = [
    path("authorize/", views.AuthorizationView.as_view(), name="authorize"),
    path("token/", ThrottledTokenView.as_view(), name="token"),
    path("revoke_token/", views.RevokeTokenView.as_view(), name="revoke-token"),
]
