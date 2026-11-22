from rest_framework import status

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Exists, OuterRef, QuerySet, Q, F
from django.utils import timezone

from NearBeach.models.kanban_board.kanban_card import KanbanCard
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.user import UserGroup, Group
from NearBeach.serializers.kanban_board.kanban_card_serializer import KanbanCardSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse,
)
from NearBeach.services.AuditService import AuditService
from NearBeach.utils.api.check_group_list import check_group_list


class KanbanCardService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete kanban_card objects"""

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        """Method for creating a new kanban_card"""
        serializer = KanbanCardSerializer(
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

        # Create the kanban_card - and its audit entry in the same transaction
        with transaction.atomic():
            created_kanban_card = serializer.save(
                change_user=request.user, creation_user=request.user
            )
            AuditService.record_create(request, self.destination, created_kanban_card)

        # Re-serialize the created kanban_card so it is in the same shape for the user
        serializer = KanbanCardSerializer(created_kanban_card, many=False)

        return serializer.data, status.HTTP_201_CREATED

    # TODO - returns a bare status code, which the view treats as truthy, so destroy always answers 204
    def delete(self, request: AuthenticatedRequest, card_id: int) -> int:  # type: ignore[override]
        kanban_card = KanbanCard.objects.filter(
            pk=card_id,
            is_deleted=False,
            kanban_board_id=self.location_id,
        )

        if len(kanban_card) == 0:
            return status.HTTP_404_NOT_FOUND

        with transaction.atomic():
            kanban_card.update(
                is_deleted=True,
                change_user=request.user,
                date_modified=timezone.now(),
            )
            AuditService.record_delete(request, self.destination, self.location_id)

        return status.HTTP_204_NO_CONTENT

    # The view paginates the queryset itself, so this returns the queryset rather than a ServiceResponse
    def get_list(self, request: AuthenticatedRequest) -> QuerySet[KanbanCard]:  # type: ignore[override]
        # Correlated EXISTS rather than id__in - on MySQL the IN form walks every kanban_card the user can see
        # before filtering, where EXISTS lets the database walk kanban_cards and check each one
        object_assignment_results = ObjectAssignment.objects.filter(
            kanban_card_id=OuterRef("pk"),
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values(
                "group_id",
            ),
        )

        kanban_card_results = KanbanCard.objects.filter(
            Exists(object_assignment_results),
            is_deleted=False,
        )

        # Filter by search parameter in the query string
        search = request.query_params.get("search", None)
        if search is not None:
            # Translate search to id
            search_id = int(search) if str.isdigit(search) else None

            # Apply search filter
            kanban_card_results = kanban_card_results.filter(
                Q(title__icontains=search) | Q(id=search_id)
            )

        show_closed = request.query_params.get("show_closed", None)
        if not show_closed == "true":
            # Hide all the closed
            kanban_card_results = kanban_card_results.exclude(
                status__higher_order_status="Closed",
            )

        return kanban_card_results

    def retrieve(self, request: AuthenticatedRequest, kanban_card_id: int) -> ServiceResponse:
        kanban_card_results = KanbanCard.objects.filter(
            is_archived=False,
            is_deleted=False,
            kanban_board_id=self.location_id,
            pk=kanban_card_id,
        ).first()
        if kanban_card_results is None:
            return "KanbanCard does not exist", status.HTTP_404_NOT_FOUND

        # Get assigned object
        object_assignments = ObjectAssignment.objects.filter(
            is_deleted=False,
            kanban_card_id=self.location_id,
        )

        # Define groups list
        # group_list and user_list are extra attributes the serializer reads
        kanban_card_results.group_list = Group.objects.filter(
            is_deleted=False,
            id__in=object_assignments.filter(
                group_id__isnull=False,
            ).values("group_id"),
        )

        # Define user list
        kanban_card_results.user_list = User.objects.filter(
            pk__in=object_assignments.filter(
                assigned_user__isnull=False,
            ).values("assigned_user_id"),
        ).annotate(profile_picture=F("userprofilepicture__document_id__key"))

        # Append extra data

        # Create the serializer
        serializer = KanbanCardSerializer(
            kanban_card_results,
            context={
                "request": request,
                "method": "GET",
            },
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, object_id: int) -> ServiceResponse:
        # Get kanban_card
        kanban_card = KanbanCard.objects.get(
            is_deleted=False,
            pk=object_id,
            kanban_board_id=self.location_id,
        )

        # Setup serializer
        serializer = KanbanCardSerializer(
            kanban_card,
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
            kanban_card = KanbanCard.objects.select_for_update().get(pk=object_id)
            serializer.instance = kanban_card
            before = AuditService.snapshot(kanban_card)
            serializer.save(change_user=request.user)
            AuditService.record_update(request, "kanban_card", before, kanban_card)

        return serializer.data, status.HTTP_200_OK
