from django.urls import path, include
from rest_framework.routers import SimpleRouter
from NearBeach.views.api import (
    coffee_api_view,
    kanban_board_api_view,
    project_api_view,
    requirement_api_view,
    request_for_change_api_view,
    sprint_api_view,
    task_api_view,
)
from NearBeach.views.api.available_data import (
    customer_list_api_view,
    sprint_list_api_view,
    tag_list_api_view,
)
from NearBeach.views.api.object_data import (
    group_and_user_api_view,
    link_api_view,
    note_api_view,
    object_sprint_api_view,
    tag_api_view,
)


# Create the router for our view sets
router = SimpleRouter()
router.register(r'available_data/customer_list', customer_list_api_view.CustomerListViewSet, basename='customer_list')
router.register(r'available_data/sprint_list', sprint_list_api_view.SprintListViewSet, basename='sprint_list')
router.register(r'available_data/tag_list', tag_list_api_view.TagListViewSet, basename='tag_list')
router.register(r'coffee', coffee_api_view.CoffeeViewSet, basename='coffee')
router.register(r'kanban_board', kanban_board_api_view.KanbanBoardViewSet, basename='kanban_board')
router.register(r'project', project_api_view.ProjectViewSet, basename='project')
router.register(r'requirement', requirement_api_view.RequirementViewSet, basename='requirement')
router.register(r'request_for_change', request_for_change_api_view.RequirementViewSet, basename='request_for_change')
router.register(r'sprint', sprint_api_view.SprintViewSet, basename='sprint')
router.register(r'task', task_api_view.TaskViewSet, basename='task')
router.register(r'(?P<destination>[\w]+)/(?P<location_id>[0-9]+)/group_and_user', group_and_user_api_view.GroupAndUserViewSet, basename='group_and_user')
router.register(r'(?P<destination>[\w]+)/(?P<location_id>[0-9]+)/link', link_api_view.LinkViewSet, basename='link')
router.register(r'(?P<destination>[\w]+)/(?P<location_id>[0-9]+)/note', note_api_view.NoteViewSet, basename='note')
router.register(r'(?P<destination>[\w]+)/(?P<location_id>[0-9]+)/object_sprint', object_sprint_api_view.ObjectSprintViewSet, basename='object_sprint')
router.register(r'(?P<destination>[\w]+)/(?P<location_id>[0-9]+)/tag', tag_api_view.TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]