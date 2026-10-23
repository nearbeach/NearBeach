"""URL patterns for NearBeach - root level"""
from django.urls import path, include

from NearBeach.views.application.application_views import ApplicationView
from NearBeach.views.authentication.authentication_views import AuthenticationView
from NearBeach.views.authentication.reset_password_view import ResetPasswordView
from NearBeach.views.authentication.logout_views import LogoutView
from NearBeach.views.private_document.private_document_views import PrivateDocumentView
from NearBeach.views.public_link.public_link_view import PublicLinkView

urlpatterns = [
    # API
    path('api/v1/', include('NearBeach.urls.api_public')),
    path('api/v1/', include('NearBeach.urls.api_internal')),

    # Authentication views
    path('login/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path("login/<path:_>/", AuthenticationView.as_view(), name="login"),
    path('login/', AuthenticationView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Private
    path("private/<uuid:document_key>/", PrivateDocumentView.as_view(), name="private_document"),

    # Public Links
    path("public_link/<uuid:public_link_id>/", PublicLinkView.as_view(), name="public_link"),

    # Fallback urls to the frontend
    path("<path:_>", ApplicationView.as_view(), name="application"),
    path("", ApplicationView.as_view(), name="application"),
]
