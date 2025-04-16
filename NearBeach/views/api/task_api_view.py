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


class TaskViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer

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

        # Gather instances
        organisation_instance = Organisation.objects.get(
            organisation_id=serializer.data.get("organisation_id"),
        )

        # Get first task status
        task_status = ListOfTaskStatus.objects.filter(
            is_deleted=False
        ).order_by(
            "task_status_sort_order",
        )

        task_submit = Task(
            task_short_description=serializer.data.get("task_short_description"),
            task_long_description=serializer.data.get("task_long_description"),
            organisation=organisation_instance,
            task_start_date=serializer.data.get("task_start_date"),
            task_end_date=serializer.data.get("task_end_date"),
            task_status=task_status.first(),
            change_user=request.user,
            creation_user=request.user,

        )
        task_submit.save()

        # Assign task to the groups
        for single_group in group_list:
            group_instance = Group.objects.get(
                group_id=single_group,
            )

            # Save the group against the new task
            submit_object_assignment = ObjectAssignment(
                group_id=group_instance,
                change_user=request.user,
                task=task_submit,
            )
            submit_object_assignment.save()

        # Transfer any images to the new task id
        transfer_new_object_uploads(
            "task",
            task_submit.task_id,
            serializer.data.get("uuid")
        )

        return Response(
            data={ "task_id": task_submit.task_id },
            status=status.HTTP_201_CREATED,
        )

    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_deleted = True
        task.change_user = request.user
        task.save()
        return Response(data='task deleted')

    @check_user_api_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        # Setup Attributes
        page_size = int(request.query_params.get("page_size", 100))
        page_size = page_size if page_size <= 1000 else 1000
        page = int(request.query_params.get("page", 1))

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
        )[(page - 1) * page_size : page * page_size]

        serializer = TaskSerializer(task_results, many=True)

        return Response(serializer.data)

    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Task.objects.all()
        task_results = get_object_or_404(
            queryset,
            pk=pk
        )
        serializer = TaskSerializer(task_results)
        return Response(serializer.data)

    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Obtain Instances
        task_status_instance = ListOfTaskStatus.objects.get(
            task_status_id=serializer.data["task_status"],
        )

        # Update task
        update_task = Task.objects.get(pk=pk)
        update_task.task_short_description = serializer.data["task_short_description"]
        update_task.task_long_description = serializer.data["task_long_description"]
        update_task.task_start_date = serializer.data["task_start_date"]
        update_task.task_end_date = serializer.data["task_end_date"]
        update_task.task_status = task_status_instance
        update_task.task_priority = serializer.data["task_priority"]
        update_task.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

