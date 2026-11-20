from rest_framework import status

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Exists, OuterRef, QuerySet, Q, F
from django.utils import timezone

from NearBeach.models.requirement.requirement import Requirement
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.user import UserGroup, Group
from NearBeach.serializers.requirement_serializer import RequirementSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse,
)
from NearBeach.services.AuditService import AuditService
from NearBeach.utils.api.check_group_list import check_group_list


class RequirementService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete requirement objects"""

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        """Method for creating a new requirement"""
        serializer = RequirementSerializer(
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

        # Create the requirement - and its audit entry in the same transaction
        with transaction.atomic():
            created_requirement = serializer.save(
                change_user=request.user, creation_user=request.user
            )
            AuditService.record_create(request, self.destination, created_requirement)

        # Re-serialize the created requirement so it is in the same shape for the user
        serializer = RequirementSerializer(created_requirement, many=False)

        return serializer.data, status.HTTP_201_CREATED

    # TODO - returns a bare status code, which the view treats as truthy, so destroy always answers 204
    def delete(self, request: AuthenticatedRequest, _: None) -> int:  # type: ignore[override]
        requirement = Requirement.objects.filter(
            pk=self.location_id,
            is_deleted=False,
        )

        if len(requirement) == 0:
            return status.HTTP_400_BAD_REQUEST

        with transaction.atomic():
            requirement.update(
                is_deleted=True,
                change_user=request.user,
                date_modified=timezone.now(),
            )
            AuditService.record_delete(request, self.destination, self.location_id)

        return status.HTTP_204_NO_CONTENT

    # The view paginates the queryset itself, so this returns the queryset rather than a ServiceResponse
    def get_list(self, request: AuthenticatedRequest) -> QuerySet[Requirement]:  # type: ignore[override]
        # Correlated EXISTS rather than id__in - on MySQL the IN form walks every requirement the user can see
        # before filtering, where EXISTS lets the database walk requirements and check each one
        object_assignment_results = ObjectAssignment.objects.filter(
            requirement_id=OuterRef("pk"),
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values(
                "group_id",
            ),
        )

        requirement_results = Requirement.objects.filter(
            Exists(object_assignment_results),
            is_deleted=False,
        )

        # Filter by search parameter in the query string
        search = request.query_params.get("search", None)
        if search is not None:
            # Translate search to id
            search_id = int(search) if str.isdigit(search) else None

            # Apply search filter
            requirement_results = requirement_results.filter(
                Q(title__icontains=search) | Q(id=search_id)
            )

        show_closed = request.query_params.get("show_closed", None)
        if not show_closed == "true":
            # Hide all the closed
            requirement_results = requirement_results.exclude(
                status__higher_order_status="Closed",
            )

        return requirement_results

    def retrieve(self, request: AuthenticatedRequest) -> ServiceResponse:
        requirement_results = Requirement.objects.filter(
            is_deleted=False,
            pk=self.location_id,
        ).first()
        if requirement_results is None:
            return "Requirement does not exist", status.HTTP_404_NOT_FOUND

        # Get assigned object
        object_assignments = ObjectAssignment.objects.filter(
            is_deleted=False,
            requirement_id=self.location_id,
        )

        # Define groups list
        # group_list and user_list are extra attributes the serializer reads
        requirement_results.group_list = Group.objects.filter(
            is_deleted=False,
            id__in=object_assignments.filter(
                group_id__isnull=False,
            ).values("group_id"),
        )

        # Define user list
        requirement_results.user_list = User.objects.filter(
            pk__in=object_assignments.filter(
                assigned_user__isnull=False,
            ).values("assigned_user_id"),
        ).annotate(profile_picture=F("userprofilepicture__document_id__key"))

        # Append extra data

        # Create the serializer
        serializer = RequirementSerializer(
            requirement_results,
            context={
                "request": request,
                "method": "GET",
            },
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, _: None) -> ServiceResponse:
        # Get requirement
        requirement = Requirement.objects.get(pk=self.location_id)

        # Setup serializer
        serializer = RequirementSerializer(
            requirement,
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
            requirement = Requirement.objects.select_for_update().get(pk=self.location_id)
            serializer.instance = requirement
            before = AuditService.snapshot(requirement)
            serializer.save(change_user=request.user)
            AuditService.record_update(request, self.destination, before, requirement)

        return serializer.data, status.HTTP_200_OK
