from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.models import (
    Group,
    ListOfRequirementStatus,
    ListOfRequirementType,
    Requirement,
    RequirementItem,
    ObjectAssignment,
    Organisation,
    UserGroup,
)
from NearBeach.serializers.requirement_serializer import RequirementSerializer
from NearBeach.serializers.requirement_item_serializer import RequirementItemSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.views.document_views import transfer_new_object_uploads
import datetime


@extend_schema(
    tags=["Change Tasks"],
)
class RequirementViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Requirement.objects.filter(is_deleted=False)
    serializer_class = RequirementSerializer

    @extend_schema(
        description="""
# 📌 Description

Create a Requirement to gather user requirements.

# 🧾 Parameters

- Requirement Title
- Requirement Scope
- Requirement Status
- Requirement Type
- Organisation
- Group List
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new change task",
                value={
                    "requirement_title": "Requirement Title",
                    "requirement_scope": "<p>Hello World</p>",
                    "requirement_status": 5,
                    "requirement_type": 3,
                    "organisation": 1,
                    "group_list": [1, 2],
                }
            )
        ],
    )
    @check_user_api_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = RequirementSerializer(data=request.data, context={'request': request})
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

        # Create the requirement
        create_requirement = serializer.save(
            change_user=request.user,
            creation_user=request.user,
        )

        # Transfer any images to the new requirement id
        transfer_new_object_uploads(
            "requirement",
            create_requirement.requirement_id,
            serializer.data.get("uuid")
        )

        # Re-serialize
        serializer = RequirementSerializer(
            create_requirement,
            many=False
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete the requirements.


# ✅ Notes

Users will need to have the permission to delete.
        """
    )
    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        requirement = self.get_object()
        requirement.is_deleted = True
        requirement.change_user = request.user
        requirement.save()
        return Response(
            data='requirement deleted',
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all requirements
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

        requirement_results = Requirement.objects.filter(
            is_deleted=False,
            requirement_id__in=object_assignment_results.values("requirement_id"),
        )

        # Handle pagination
        page = self.paginate_queryset(requirement_results)
        if page is not None:
            serializer = RequirementSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RequirementSerializer(requirement_results, many=True)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single task.

    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Requirement.objects.all()
        requirement_results = get_object_or_404(
            queryset,
            pk=pk
        )

        # Get Extra Attributes for the data
        requirement_results.requirement_item = RequirementItem.objects.filter(
            is_deleted=False,
            requirement_id=pk,
        )

        serializer = RequirementSerializer(requirement_results)
        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Updates a single task.

# 🧾 Parameters

- Requirement Title
- Requirement Scope
- Requirement Status
- Requirement Type
- Organisation
- Group List
    """
    )
    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = RequirementSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the requirement
        update_requirement = get_object_or_404(
            queryset=Requirement.objects.filter(
                is_deleted=False,
            ),
            pk=pk,
        )

        # Update the requirement
        update_requirement.change_user = request.user
        update_requirement.date_modified = datetime.datetime.now()
        update_requirement = serializer.update(
            update_requirement,
            serializer.validated_data,
        )

        # Re-serialize the data
        serializer = RequirementSerializer(
            update_requirement,
            many=False
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

