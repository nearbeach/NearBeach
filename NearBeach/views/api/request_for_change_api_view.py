from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.models import (
    ChangeTask,
    Group,
    ObjectAssignment,
    Organisation,
    RequestForChange,
    User,
    UserGroup, ListOfRFCStatus,
)
from NearBeach.serializers.request_for_change_serializer import RequestForChangeSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.views.document_views import transfer_new_object_uploads
import datetime


class RequirementViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = RequestForChange.objects.filter(is_deleted=False)
    serializer_class = RequestForChangeSerializer

    @check_user_api_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = RequestForChangeSerializer(data=request.data, context={'request': request})
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

        # Get Instances
        rfc_lead_instance = User.objects.get(
            pk=serializer.data.get("rfc_lead"),
        )

        # Setup the default dates for two weeks
        default_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Add two weeks onto each date
        default_date = default_date + datetime.timedelta(weeks=2)

        # Create the object
        request_for_change_submit = RequestForChange(
            rfc_title=serializer.data.get("rfc_title"),
            rfc_summary=serializer.data.get("rfc_summary"),
            rfc_type=serializer.data.get("rfc_type"),
            rfc_version_number=serializer.data.get("rfc_version_number"),
            rfc_lead=rfc_lead_instance,
            rfc_priority=serializer.data.get("rfc_priority"),
            rfc_risk=serializer.data.get("rfc_risk"),
            rfc_impact=serializer.data.get("rfc_impact"),
            rfc_risk_and_impact_analysis=serializer.data.get("rfc_risk_and_impact_analysis"),
            rfc_implementation_plan=serializer.data.get("rfc_implementation_plan"),
            rfc_backout_plan=serializer.data.get("rfc_backout_plan"),
            rfc_test_plan=serializer.data.get("rfc_test_plan"),
            rfc_implementation_start_date=default_date,
            rfc_implementation_end_date=default_date,
            rfc_implementation_release_date=default_date,
            change_user=request.user,
            creation_user=request.user,
            rfc_status=ListOfRFCStatus.objects.get(rfc_status_id=1),
        )
        request_for_change_submit.save()

        # Assign requirement to the groups
        for single_group in group_list:
            group_instance = Group.objects.get(
                group_id=single_group,
            )

            # Save the group against the new requirement
            submit_object_assignment = ObjectAssignment(
                group_id=group_instance,
                request_for_change=request_for_change_submit,
                change_user=request.user,
            )
            submit_object_assignment.save()

        # Transfer any images to the new requirement id
        transfer_new_object_uploads(
            "request_for_change",
            request_for_change_submit.rfc_id,
            serializer.data.get("uuid")
        )

        return Response(
            data={ "rfc_id": request_for_change_submit.rfc_id },
            status=status.HTTP_201_CREATED,
        )

    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        request_for_change = self.get_object()
        request_for_change.is_deleted = True
        request_for_change.change_user = request.user
        request_for_change.save()
        return Response(data='request for change deleted')

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

        request_for_change_results = RequestForChange.objects.filter(
            is_deleted=False,
            rfc_id__in=object_assignment_results.values("request_for_change_id"),
        )[(page - 1) * page_size : page * page_size]

        serializer = RequestForChangeSerializer(request_for_change_results, many=True)

        return Response(serializer.data)

    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = RequestForChange.objects.all()
        request_for_change_results = get_object_or_404(
            queryset,
            pk=pk
        )

        # Get Extra Attributes for the data
        request_for_change_results.change_task = ChangeTask.objects.filter(
            is_deleted=False,
            request_for_change_id=pk,
        )

        serializer = RequestForChangeSerializer(request_for_change_results)
        return Response(serializer.data)

    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = RequestForChangeSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update Requirement
        update_rfc = RequestForChange.objects.get(pk=pk)
        update_rfc.rfc_title = serializer.data["rfc_title"]
        update_rfc.rfc_summary = serializer.data["rfc_summary"]
        update_rfc.rfc_implementation_release_date = serializer.data["rfc_implementation_release_date"]
        update_rfc.rfc_version_number = serializer.data["rfc_version_number"]
        update_rfc.rfc_type = serializer.data["rfc_type"]
        update_rfc.date_modified = datetime.datetime.now()
        update_rfc.change_user = request.user
        update_rfc.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

