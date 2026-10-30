from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter
from NearBeach.views.api_v1 import (
    coffee_api_view,
    organisation_api_view,
    project_api_view,
    public_link_api_view,
)
from NearBeach.views.api_v1.search import (
    potential_object_links,
)

# Create the router for our view sets
router = SimpleRouter()
router.register(r'coffee', coffee_api_view.CoffeeViewSet, basename='coffee')
router.register(r'organisation', organisation_api_view.OrganisationViewSet, basename='organisation')
router.register(r'project', project_api_view.ProjectViewSet, basename='project')
router.register(r'public_link', public_link_api_view.PublicLinkViewSet, basename='public_link')
router.register(r'data/potential_object_links', potential_object_links.PotentialObjectLinksViewSet, basename='potential_object_links')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]