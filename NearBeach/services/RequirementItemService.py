from rest_framework import status

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Exists, OuterRef, QuerySet, Q, F
from django.utils import timezone

from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.user import UserGroup, Group
from NearBeach.serializers.requirement_item_serializer import RequirementItemSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse,
)
from NearBeach.services.AuditService import AuditService
from NearBeach.utils.api.check_group_list import check_group_list


class RequirementItemService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete requirement_item objects"""

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        """Method for creating a new requirement_item"""
        serializer = RequirementItemSerializer(
            context={
                "request": request,
                "method": "POST",
            },
            data=request.data,
        )
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Check that there are groups
        group_list = serializer.validated_data.get("group_list", [])
        if not check_group_list(request.user, group_list):
            return "No Access to groups provided", status.HTTP_400_BAD_REQUEST

        # Create the requirement_item - and its audit entry in the same transaction
        with transaction.atomic():
            created_requirement_item = serializer.save(
                change_user=request.user, creation_user=request.user
            )
            AuditService.record_create(request, self.destination, created_requirement_item)

        # Re-serialize the created requirement_item so it is in the same shape for the user
        serializer = RequirementItemSerializer(created_requirement_item, many=False)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, requirement_item_pk: int) -> ServiceResponse:
        """Method to delete a requirement_item"""
        requirement_item = RequirementItem.objects.filter(
            is_deleted=False,
            pk=requirement_item_pk,
            requirement_id=self.location_id,
        )
        if not requirement_item.exists():
            return "Customer does not exist", status.HTTP_404_NOT_FOUND

        with transaction.atomic():
            requirement_item.update(
                is_deleted=True,
                change_user=request.user,
                date_modified=timezone.now(),
            )
            AuditService.record_delete(request, self.destination, self.location_id)

        return {}, status.HTTP_204_NO_CONTENT

    # The view paginates the queryset itself, so this returns the queryset rather than a ServiceResponse
    def get_list(self, request: AuthenticatedRequest) -> QuerySet[RequirementItem]:  # type: ignore[override]
        # Correlated EXISTS rather than id__in - on MySQL the IN form walks every requirement_item the user can see
        # before filtering, where EXISTS lets the database walk requirement_items and check each one
        object_assignment_results = ObjectAssignment.objects.filter(
            requirement_item_id=OuterRef("pk"),
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values(
                "group_id",
            ),
        )

        requirement_item_results = RequirementItem.objects.filter(
            Exists(object_assignment_results),
            is_deleted=False,
        )

        # Filter by search parameter in the query string
        search = request.query_params.get("search", None)
        if search is not None:
            # Translate search to id
            search_id = int(search) if str.isdigit(search) else None

            # Apply search filter
            requirement_item_results = requirement_item_results.filter(
                Q(title__icontains=search) | Q(id=search_id)
            )

        show_closed = request.query_params.get("show_closed", None)
        if not show_closed == "true":
            # Hide all the closed
            requirement_item_results = requirement_item_results.exclude(
                status__higher_order_status="Closed",
            )

        return requirement_item_results

    def retrieve(self, request: AuthenticatedRequest, pk: int) -> ServiceResponse:
        requirement_item_results = RequirementItem.objects.filter(
            is_deleted=False,
            requirement_id=self.location_id,
            pk=pk,
        ).first()
        if requirement_item_results is None:
            return "RequirementItem does not exist", status.HTTP_404_NOT_FOUND

        # Get assigned object
        object_assignments = ObjectAssignment.objects.filter(
            is_deleted=False,
            requirement_item_id=self.location_id,
        )

        # Define groups list
        # group_list and user_list are extra attributes the serializer reads
        requirement_item_results.group_list = Group.objects.filter(
            is_deleted=False,
            id__in=object_assignments.filter(
                group_id__isnull=False,
            ).values("group_id"),
        )

        # Define user list
        requirement_item_results.user_list = User.objects.filter(
            pk__in=object_assignments.filter(
                assigned_user__isnull=False,
            ).values("assigned_user_id"),
        ).annotate(profile_picture=F("userprofilepicture__document_id__key"))

        # Append extra data

        # Create the serializer
        serializer = RequirementItemSerializer(
            requirement_item_results,
            context={
                "request": request,
                "method": "GET",
            },
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, pk: int) -> ServiceResponse:
        # Get requirement_item
        requirement_item = RequirementItem.objects.get(
            requirement_id=self.location_id,
            pk=pk,
        )

        # Setup serializer
        serializer = RequirementItemSerializer(
            requirement_item,
            data=request.data,
            context={
                "request": request,
                "method": "PATCH",
            },
            partial=True,
        )
        if not serializer.is_valid():
            return serializer.errors, status.HTTP_400_BAD_REQUEST

        # Make sure we update the change user, and log what changed in the same transaction
        with transaction.atomic():
            # Lock the row first, then snapshot, so the audit records the state actually replaced
            # (select_for_update is a no-op on SQLite)
            requirement_item = RequirementItem.objects.select_for_update().get(pk=self.location_id)
            serializer.instance = requirement_item
            before = AuditService.snapshot(requirement_item)
            serializer.save(change_user=request.user)
            AuditService.record_update(request, self.destination, before, requirement_item)

        return serializer.data, status.HTTP_200_OK
