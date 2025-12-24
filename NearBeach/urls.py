from django.urls import path

from .views.placeholder_view import PlaceholderView

urlpatterns = [
    path("", PlaceholderView.as_view(), name="dashboard"),
]
