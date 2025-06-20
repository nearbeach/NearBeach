from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.models import (
    Group,
    ListOfTaskStatus,
    ObjectAssignment,
    Organisation,
    Task,
    UserGroup,
)
from NearBeach.serializers.task_serializer import TaskSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.views.document_views import transfer_new_object_uploads
from NearBeach import event_hooks

event_hooks.register_event_type("task.create", Task)


@extend_schema(
    tags=["Tasks"],
    methods=["GET", "POST", "PUT", "DELETE"],
)
class TaskViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer

    @extend_schema(
        description="""
# 📌 Description

Create Tasks to help manage your tasks.

# 🧾 Parameters

- Task Short Description: The task's title. Should be short and under 255 characters.
- Task Long Description: The description of the project. Can have basic HTML
- Task Start Date
- Task End Date
- Organisation: The organisation that the project belongs too. Should be an int. Use the Organisation API to find the 
correct organisation id.
- Group List: All groups associated with this project. At least one of the user's groups will need to be included. The 
group id's can be found using the Group List API.
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new project",
                value={
                    "task_short_description": "My Project",
                    "task_long_description": "<h1>Hello World</h1>",
                    "task_start_date": "2024-12-19 15:49:37",
                    "task_end_date": "2024-12-19 15:49:37",
                    "organisation": 2,
                    "group_list": [1, 2],
                }
            )
        ],
    )
    @check_user_api_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        group_list = request.data.getlist('group_list', [])
        if group_list is None or len(group_list) == 0:
            return Response(
                "Groups are missing",
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_task = serializer.save(
            change_user=request.user,
            creation_user=request.user,
        )

        # Transfer any images to the new task id
        transfer_new_object_uploads(
            "task",
            created_task.task_id,
            serializer.data.get("uuid")
        )

        # Re-serialize the created task so it is in the same format as other API
        serializer = TaskSerializer(created_task, many=False)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete tasks.


# ✅ Notes

Users will need to have the permission to delete.
        """
    )
    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_deleted = True
        task.change_user = request.user
        task.save()
        return Response(
            data='task deleted',
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all tasks within NearBeach.


# ✅ Notes

- Pagination is enabled on this list. Use `?Page=` to navigate to the appropriate page.
    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        object_assignment_results = ObjectAssignment.objects.filter(
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values(
                "group_id",
            )
        )

        task_results = Task.objects.filter(
            is_deleted=False,
            task_id__in=object_assignment_results.values("task_id"),
        )

        # Handle pagination
        page = self.paginate_queryset(task_results)
        if page is not None:
            serializer = TaskSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TaskSerializer(task_results, many=True)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single task.

    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Task.objects.all()
        task_results = get_object_or_404(
            queryset,
            pk=pk
        )
        serializer = TaskSerializer(task_results)
        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Updates a single task.

# 🧾 Parameters

- Task Short Description: The project's name. Should be short and under 255 characters.
- Task Long Description: The description of the project. Can have basic HTML
- Task Start Date
- Task End Date
- Task Status: The status of the task.
- Task Priority: The priority of the task.
    - 0 = Highest
    - 1 = High
    - 2 = Normal
    - 3 = Low
    - 4 = Lowest
    """
    )
    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Double check the task exists
        queryset = Task.objects.filter(
            is_deleted=False,
        )
        update_task = get_object_or_404(
            queryset,
            pk=pk,
        )
        update_task.change_user = request.user
        update_task = serializer.update(
            update_task,
            serializer.data,
        )

        # Re-serialize the data to send back complete set to user
        serializer = TaskSerializer(
            update_task,
            many=False,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

