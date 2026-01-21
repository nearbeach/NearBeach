"""URL patterns for NearBeach - root level"""
from django.urls import path, include

from NearBeach.views.application.application_views import ApplicationView
from NearBeach.views.application.authentication_views import AuthenticationView

urlpatterns = [
    # API
    path('api/v1/', include('NearBeach.urls.api_public')),
    path('api/v1/', include('NearBeach.urls.api_internal')),

    # Authentication views
    path('login', AuthenticationView.as_view(), name='login'),
    path('login/', AuthenticationView.as_view(), name='login'),
    path("login/<path:_>", AuthenticationView.as_view(), name="login"),

    # Fallback urls to the frontend
    path("<path:_>", ApplicationView.as_view(), name="application"),
    path("", ApplicationView.as_view(), name="application"),
]
