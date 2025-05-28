from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from NearBeach.models import (
    Requirement,
    RequirementItem,
)
from NearBeach.serializers.requirement_item_serializer import RequirementItemSerializer
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions


class RequirementItemViewSet(viewsets.ModelViewSet):
    queryset = RequirementItem.objects.filter(
        is_deleted=False,
    )
    serializer_class = RequirementItemSerializer

    @check_user_api_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = RequirementItemSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Setup data
        serializer.save(change_user=request.user, requirement_id=kwargs["requirement_id"])

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
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
