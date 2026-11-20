from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter
from NearBeach.views.api_v1 import (
    coffee_api_view,
    customer_api_view,
    kanban_board_api_view,
    kanban_card_api_view,
    organisation_api_view,
    project_api_view,
    public_link_api_view,
    task_api_view,
    requirement_api_view,
    requirement_item_api_view,
)
from NearBeach.views.api_v1.search import (
    potential_object_links,
)

# Create the router for our view sets
router = SimpleRouter()
router.register(r'coffee', coffee_api_view.CoffeeViewSet, basename='coffee')
router.register(r'data/potential_object_links', potential_object_links.PotentialObjectLinksViewSet, basename='potential_object_links')
router.register(r'kanban_board/(?P<kanban_board_id>\d+)/kanban_card', kanban_card_api_view.KanbanCardViewSet, basename='kanban_card')
router.register(r'kanban_board', kanban_board_api_view.KanbanBoardViewSet, basename="kanban_board")
router.register(r'organisation/(?P<organisation_id>\d+)/customer', customer_api_view.CustomerViewSet, basename='customer')
router.register(r'organisation', organisation_api_view.OrganisationViewSet, basename='organisation')
router.register(r'project', project_api_view.ProjectViewSet, basename='project')
router.register(r'public_link', public_link_api_view.PublicLinkViewSet, basename='public_link')
router.register(r'requirement/(?P<requirement_id>\d+)/requirement_item', requirement_item_api_view.RequirementItemViewSet, basename='requirement_item')
router.register(r'requirement', requirement_api_view.RequirementViewSet, basename='requirement')
router.register(r'task', task_api_view.TaskViewSet, basename='task')

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]