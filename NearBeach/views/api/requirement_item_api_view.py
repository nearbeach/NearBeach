from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from NearBeach.models import (
    Requirement,
    RequirementItem,
)
from NearBeach.serializers.requirement_item_serializer import RequirementItemSerializer
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions


@extend_schema(
    tags=["Requirement Item"]
)
class RequirementItemViewSet(viewsets.ModelViewSet):
    queryset = RequirementItem.objects.filter(
        is_deleted=False,
    )
    serializer_class = RequirementItemSerializer

    @extend_schema(
        description="""
# 📌 Description

Create Requirement Item against the Requirement.

# 🧾 Parameters

- Requirement Item Title: Title of the requirement item
- Requirement Item Scope: Scope of the item - will be <html>
- Requirement Item Status: The status of the requirement item.
- Requirement Item Type: The type of the requirement item.
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new kanban board",
                value={
                    "requirement_item_status": 1,
                    "requirement_item_type": 2,
                    "requirement_item_scope": "<p>Hello World</p>",
                    "requirement_item_title": "Hello World",
                }
            )
        ],
    )
    @check_user_api_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = RequirementItemSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Setup data
        submit_requirement_item = serializer.save(
            change_user=request.user,
            requirement_id=kwargs["requirement_id"],
            requirement_item_story_point=1,
        )

        # Re-serialize the data
        serializer = RequirementItemSerializer(
            submit_requirement_item,
            many=False,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete the requirement item.


# ✅ Notes

Users will need to have the permission to delete. This entails having the ability to edit the requirement.
        """
    )
    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        requirement_item = self.get_object()
        requirement_item.is_deleted = True
        requirement_item.change_user = request.user
        requirement_item.save()
        return Response(
            data="Requirement Item Deleted",
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all requirement items within the requirement.
    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        requirement_item_results = RequirementItem.objects.filter(
            is_deleted=False,
            requirement_id=kwargs["requirement_id"],
        )

        serializer = RequirementItemSerializer(
            requirement_item_results,
            many=True,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single requirement item.

    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = RequirementItem.objects.filter(is_deleted=False)
        requirement_item_results = get_object_or_404(
            queryset,
            pk=pk,
        )

        serializer = RequirementItemSerializer(requirement_item_results)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        description="""
# 📌 Description

Updates a single requirement item under the requirement

# 🧾 Parameters

- Requirement Item Title: Title of the requirement item
- Requirement Item Scope: Scope of the item - will be <html>
- Requirement Item Status: The status of the requirement item.
- Requirement Item Type: The type of the requirement item.
- Requirement Item Priority: The priority of the item
- Requirement Item Story Points: Story points for this particular item
    """
    )
    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        if int(instance.requirement_id) != int(kwargs["requirement_id"]):
            return Response(
                data="Could not find requirement item",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RequirementItemSerializer(
            instance=instance,
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the item
        serializer.save(change_user=request.user)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
