from django.urls import path, include
from rest_framework.routers import SimpleRouter
from NearBeach.views.api import (
    coffee_api_view,
    project_api_view,
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
router.register(r'object_data/group_and_user', group_and_user_api_view.GroupAndUserViewSet, basename='group_and_user')
router.register(r'object_data/link', link_api_view.LinkViewSet, basename='link')
router.register(r'object_data/note', note_api_view.NoteViewSet, basename='note')
router.register(r'object_data/object_sprint', object_sprint_api_view.ObjectSprintViewSet, basename='object_sprint')
router.register(r'object_data/tag', tag_api_view.TagViewSet, basename='tag')
router.register(r'project', project_api_view.ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]