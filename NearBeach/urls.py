"""URL patterns for NearBeach - root level"""
from django.urls import path

from .views.application.application_views import ApplicationView

urlpatterns = [

    # Fallback urls to the frontend
    path("<path:_>", ApplicationView.as_view(), name="application"),
    path("", ApplicationView.as_view(), name="application"),
]
