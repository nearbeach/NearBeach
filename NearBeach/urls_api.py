from django.urls import path, include
from rest_framework.routers import DefaultRouter
from NearBeach.views.api import project_api_view


# Create the router for our view sets
router = DefaultRouter()
router.register(r'projects', project_api_view.ProjectViewSet, basename='project'),

urlpatterns = [
    path('', include(router.urls)),
]