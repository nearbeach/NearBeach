from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from NearBeach.models import ChangeTask
from NearBeach.serializers.change_task_serializer import ChangeTaskSerializer
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.views.request_for_change_views import update_rfc_dates


class ChangeTaskViewSet(viewsets.ModelViewSet):
    queryset = ChangeTask.objects.filter(is_deleted=False)
    serializer_class = ChangeTaskSerializer

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

        # Flat pack variables
        request_for_change_id = kwargs["request_for_change_id"]
        start_date = serializer.validated_data["change_task_start_date"]
        end_date = serializer.validated_data["change_task_end_date"]
        task_seconds = int((end_date - start_date ).total_seconds())

        is_downtime = False
        if "is_downtime" in serializer.data:
            is_downtime = serializer.validated_data["is_downtime"]

        change_task_required_by = "Stakeholder(s)"
        if "change_task_required_by" in serializer.data:
            change_task_required_by = serializer.validated_data["change_task_required_by"]

        change_task_description = ""
        if "change_task_description" in serializer.data:
            change_task_description = serializer.validated_data["change_task_description"]

        # Create the change task
        submit_change_task = ChangeTask(
            request_for_change_id=kwargs["request_for_change_id"],
            change_task_title=serializer.validated_data["change_task_title"],
            change_task_start_date=start_date,
            change_task_end_date=end_date,
            change_task_seconds=task_seconds,
            change_task_assigned_user=serializer.validated_data["change_task_assigned_user"],
            change_task_qa_user=serializer.validated_data["change_task_qa_user"],
            change_task_status=1,
            change_task_description=change_task_description,
            change_user=request.user,
            creation_user=request.user,
            is_downtime=is_downtime,
            change_task_required_by=change_task_required_by,
        )
        submit_change_task.save()

        update_rfc_dates(request_for_change_id)

        serializer = ChangeTaskSerializer(
            ChangeTask.objects.get(change_task_id=submit_change_task.change_task_id)
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
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

    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = ChangeTask.objects.filter(is_deleted=False)
        change_task_results = get_object_or_404(
            queryset,
            pk=pk
        )

        serializer = ChangeTaskSerializer(change_task_results)
        return Response(serializer.data)

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

        # Get the change task item
        change_task_update = ChangeTask.objects.filter(
            is_deleted=False,
            request_for_change_id=kwargs["request_for_change_id"],
            change_task_id=pk,
        )
        if change_task_update is None or len(change_task_update) == 0:
            return Response(
                data={"Can not find change task"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        change_task_update = change_task_update[0]

        # Flat pack variables
        start_date = serializer.validated_data["change_task_start_date"]
        end_date = serializer.validated_data["change_task_end_date"]
        task_seconds = int((end_date - start_date).total_seconds())

        # Update the change task values
        change_task_update.change_task_title = serializer.validated_data["change_task_title"]
        change_task_update.change_task_start_date = start_date
        change_task_update.change_task_end_date = end_date
        change_task_update.change_task_seconds=task_seconds
        change_task_update.change_task_assigned_user = serializer.validated_data["change_task_assigned_user"]
        change_task_update.change_task_qa_user = serializer.validated_data["change_task_qa_user"]
        change_task_update.change_user_id = request.user

        if "is_downtime" in serializer.data:
            value = serializer.validated_data["is_downtime"]
            change_task_update.is_downtime = value.lower() == "true"

        if "change_task_required_by" in serializer.data:
            change_task_update.change_task_required_by = serializer.validated_data["change_task_required_by"]

        if "change_task_description" in serializer.data:
            change_task_update.change_task_description = serializer.validated_data["change_task_description"]

        change_task_update.save()

        update_rfc_dates(kwargs["request_for_change_id"])

        serializer = ChangeTaskSerializer(change_task_update)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
