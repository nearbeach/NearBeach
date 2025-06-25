from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.models import (
    ChangeTask,
    Group,
    ObjectAssignment,
    RequestForChange,
    User,
    UserGroup,
)
from NearBeach.serializers.request_for_change_serializer import RequestForChangeSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.utils.enums.request_for_change_enums import RequestForChangeStatus
from NearBeach.views.document_views import transfer_new_object_uploads
import datetime


@extend_schema(
    tags=["Request For Change"],
)
class RequirementViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = RequestForChange.objects.filter(is_deleted=False)
    serializer_class = RequestForChangeSerializer

    @extend_schema(
        description="""
# 📌 Description

Create a Request for Change to help you with your deployment processes

# 🧾 Parameters

- Rfc Title: Title of the RFC
- RFC Summary: Summary of the Request for change
- Group List: The groups (ids) that are assigned to this Request for Change
- Rfc Version Number: The version of the RFC
- Rfc Risk and Impact Analysis
- Rfc Implementation Plan
- Rfc Backout Plan
- Rfc Task Plan
- Rfc Type
- Rfc Lead: The user who is leading the RFC
- Rfc Priority
- Rfc Risk
- Rfc Impact
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new request for change",
                value={
                    "group_list": [1, 2],
                    "rfc_version_number": "0.32.0",
                    "rfc_title": "Release of 0.32.0",
                    "rfc_summary": "<p>Hello World</p>",
                    "rfc_type": 1,
                    "rfc_risk_and_impact_analysis": "Risk and Impact Analysis",
                    "rfc_implementation_plan": "Implementation Plan",
                    "rfc_backout_plan": "Backout Plan",
                    "rfc_test_plan": "Test Plan",
                    "rfc_lead": 1,
                    "rfc_priority": 1,
                    "rfc_risk": 1,
                    "rfc_impact": 1,
                }
            )
        ],
    )
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

        # Setup the default dates for two weeks
        default_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Add two weeks onto each date
        default_date = default_date + datetime.timedelta(weeks=2)

        request_for_change_submit = serializer.save(
            rfc_implementation_start_date=default_date,
            rfc_implementation_end_date=default_date,
            rfc_implementation_release_date=default_date,
            change_user=request.user,
            creation_user=request.user,
            rfc_status=RequestForChangeStatus.DRAFT,
        )

        # Transfer any images to the new requirement id
        transfer_new_object_uploads(
            "request_for_change",
            request_for_change_submit.rfc_id,
            serializer.data.get("uuid")
        )

        # Re-serialize everything
        serializer = RequestForChangeSerializer(
            request_for_change_submit,
            many=False
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete request for change.


# ✅ Notes

Users will need to have the permission to delete. This entails having the ability to edit a kanban board.
        """
    )
    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        request_for_change = self.get_object()
        request_for_change.is_deleted = True
        request_for_change.change_user = request.user
        request_for_change.save()
        return Response(
            data='request for change deleted',
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all the Request for Changes.
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

        request_for_change_results = RequestForChange.objects.filter(
            is_deleted=False,
            rfc_id__in=object_assignment_results.values("request_for_change_id"),
        )

        # Handle pagination
        page = self.paginate_queryset(request_for_change_results)
        if page is not None:
            serializer = RequestForChangeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RequestForChangeSerializer(request_for_change_results, many=True)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single Request for Change.

    """
    )
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

    @extend_schema(
        description="""
# 📌 Description

Updates a request for change.

# 🧾 Parameters

- Rfc Title: Title of the RFC
- RFC Summary: Summary of the Request for change
- Rfc Version Number: The version of the RFC
- Rfc Type
- RFC Implementation Release Date
    """
    )
    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = RequestForChangeSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the request for change
        update_request_for_change = get_object_or_404(
            queryset=RequestForChange.objects.filter(
                is_deleted=False,
            ),
            pk=pk,
        )

        # Update the request for change
        update_request_for_change.date_modified = datetime.datetime.now()
        update_request_for_change.change_user = request.user
        update_request_for_change = serializer.update(
            update_request_for_change,
            serializer.validated_data,
        )

        # Re-serialize
        serializer = RequestForChangeSerializer(
            update_request_for_change,
            many=False,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

