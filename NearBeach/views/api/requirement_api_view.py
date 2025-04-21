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


class RequirementViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = Requirement.objects.filter(is_deleted=False)
    serializer_class = RequirementSerializer

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

        # Gather instances
        organisation_instance = Organisation.objects.get(
            organisation_id=serializer.data.get("organisation_id"),
        )

        # Get first requirement status
        requirement_status = ListOfRequirementStatus.objects.get(
            requirement_status_id=serializer.data["requirement_status"],
        )

        requirement_type = ListOfRequirementType.objects.get(
            requirement_type_id=serializer.data["requirement_type"],
        )

        # Create the object
        requirement_submit = Requirement(
            requirement_title=serializer.data.get("requirement_title"),
            requirement_scope=serializer.data.get("requirement_scope"),
            requirement_status=requirement_status,
            requirement_type=requirement_type,
            organisation=organisation_instance,
            change_user=request.user,
            creation_user=request.user,
        )
        requirement_submit.save()

        # Assign requirement to the groups
        for single_group in group_list:
            group_instance = Group.objects.get(
                group_id=single_group,
            )

            # Save the group against the new requirement
            submit_object_assignment = ObjectAssignment(
                group_id=group_instance,
                requirement=requirement_submit,
                change_user=request.user,
            )
            submit_object_assignment.save()

        # Transfer any images to the new requirement id
        transfer_new_object_uploads(
            "requirement",
            requirement_submit.requirement_id,
            serializer.data.get("uuid")
        )

        return Response(
            data={ "requirement_id": requirement_submit.requirement_id },
            status=status.HTTP_201_CREATED,
        )

    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        requirement = self.get_object()
        requirement.is_deleted = True
        requirement.change_user = request.user
        requirement.save()
        return Response(data='requirement deleted')

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

        requirement_results = Requirement.objects.filter(
            is_deleted=False,
            requirement_id__in=object_assignment_results.values("requirement_id"),
        )[(page - 1) * page_size : page * page_size]

        serializer = RequirementSerializer(requirement_results, many=True)

        return Response(serializer.data)

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

    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = RequirementSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Obtain Instances
        requirement_status_instance = ListOfRequirementStatus.objects.get(
            requirement_status_id=serializer.data["requirement_status"],
        )

        requirement_type_instance = ListOfRequirementType.objects.get(
            requirement_type_id=serializer.data["requirement_type"]
        )

        # Update Requirement
        update_requirement = Requirement.objects.get(pk=pk)
        update_requirement.requirement_title = serializer.data["requirement_title"]
        update_requirement.requirement_scope = serializer.data["requirement_scope"]
        update_requirement.requirement_status = requirement_status_instance
        update_requirement.requirement_type = requirement_type_instance
        update_requirement.date_modified = datetime.datetime.now()
        update_requirement.change_user = request.user
        update_requirement.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

