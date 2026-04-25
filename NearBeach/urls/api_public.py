from django.urls import path, include
from rest_framework.routers import SimpleRouter
from NearBeach.views.api_v1 import (
    coffee_api_view,
    project_api_view,
)


# Create the router for our view sets
router = SimpleRouter()
router.register(r'coffee', coffee_api_view.CoffeeViewSet, basename='coffee')
router.register(r'project', project_api_view.ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]