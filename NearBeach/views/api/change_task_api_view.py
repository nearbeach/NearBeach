from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from NearBeach.models import ChangeTask
from NearBeach.serializers.change_task_serializer import ChangeTaskSerializer
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.views.request_for_change_views import update_rfc_dates


@extend_schema(
    tags=["Change Tasks"],
)
class ChangeTaskViewSet(viewsets.ModelViewSet):
    queryset = ChangeTask.objects.filter(is_deleted=False)
    serializer_class = ChangeTaskSerializer

    @extend_schema(
        description="""
# 📌 Description

Create a Change Task against the Request for Change.

# 🧾 Parameters

- Change Task Title: The title of the change task
- Change Task Assigned User: The user id who will head the task
- Change Task QA User: The user id who will Quality Assure the task
- Change Task Start Date
- Change Task End Date
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new change task",
                value={
                    "change_task_title": "Backup database",
                    "change_task_assigned_user": 1,
                    "chagne_task_qa_user": 2,
                    "change_task_start_date": "2024-12-19 15:49:37",
                    "change_task_end_date": "2024-12-19 15:49:37",
                }
            )
        ],
    )
    @check_user_api_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = ChangeTaskSerializer(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_change_task = serializer.save(
            change_user=request.user,
            creation_user=request.user,
            request_for_change_id=kwargs["request_for_change_id"],
        )

        update_rfc_dates(kwargs["request_for_change_id"])

        serializer = ChangeTaskSerializer(create_change_task, many=False)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete change task.


# ✅ Notes

Users will need to have the permission to delete. This entails having the ability to edit a kanban board.
        """
    )
    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        change_task = self.get_object()
        change_task.is_deleted = True
        change_task.change_user = request.user
        change_task.save()
        return Response(
            data='change task deleted',
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all change tasks within the request for change.
    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        change_task_results = ChangeTask.objects.filter(
            request_for_change_id=kwargs["request_for_change_id"],
            is_deleted=False,
        )

        serializer = ChangeTaskSerializer(
            change_task_results,
            many=True,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single change task.

    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = ChangeTask.objects.filter(is_deleted=False)
        change_task_results = get_object_or_404(
            queryset,
            pk=pk
        )

        serializer = ChangeTaskSerializer(change_task_results)
        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Updates a single change task under the request for change

# 🧾 Parameters

- Change Task Title: The title of the change task
- Change Task Assigned User: The user id who will head the task
- Change Task QA User: The user id who will Quality Assure the task
- Change Task Start Date
- Change Task End Date
    """
    )
    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = ChangeTaskSerializer(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the change task
        update_change_task = get_object_or_404(
            queryset=ChangeTask.objects.filter(
                is_deleted=False,
                request_for_change_id=kwargs["request_for_change_id"],
            ),
            pk=pk,
        )

        # Update the change task
        update_change_task.change_user = request.user
        update_change_task.request_for_change_id = kwargs["request_for_change_id"]
        update_change_task = serializer.update(
            update_change_task,
            serializer.validated_data,
        )

        # Update dates
        update_rfc_dates(kwargs["request_for_change_id"])

        # Re-serialize
        serializer = ChangeTaskSerializer(update_change_task, many=False)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
