from NearBeach.utils.enums.kanban_board_enums import KanbanBoardStatusChoice
from rest_framework import status

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Exists, OuterRef, QuerySet, Q, F
from django.utils import timezone

from NearBeach.models.kanban_board.kanban_board import KanbanBoard
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.user import UserGroup, Group
from NearBeach.serializers.kanban_board.kanban_board_serializer import KanbanBoardSerializer
from NearBeach.services.abstraction.object_services_abstraction import (
    AuthenticatedRequest,
    ObjectServiceAbstraction,
    ServiceResponse,
)
from NearBeach.services.AuditService import AuditService
from NearBeach.utils.api.check_group_list import check_group_list


class KanbanBoardService(ObjectServiceAbstraction):
    """Service to help create, read, update, and delete kanban_board objects"""

    def create(self, request: AuthenticatedRequest) -> ServiceResponse:
        """Method for creating a new kanban_board"""
        serializer = KanbanBoardSerializer(
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

        # Create the kanban_board - and its audit entry in the same transaction
        with transaction.atomic():
            created_kanban_board = serializer.save(
                change_user=request.user, creation_user=request.user
            )
            AuditService.record_create(request, self.destination, created_kanban_board)

        # Re-serialize the created kanban_board so it is in the same shape for the user
        serializer = KanbanBoardSerializer(created_kanban_board, many=False)

        return serializer.data, status.HTTP_201_CREATED

    def delete(self, request: AuthenticatedRequest, _: None) -> ServiceResponse:
        kanban_board = KanbanBoard.objects.filter(
            pk=self.location_id,
            is_deleted=False,
        )

        if len(kanban_board) == 0:
            return "KanbanBoard does not exist", status.HTTP_404_NOT_FOUND

        with transaction.atomic():
            kanban_board.update(
                is_deleted=True,
                change_user=request.user,
                date_modified=timezone.now(),
            )
            AuditService.record_delete(request, self.destination, self.location_id)

        return {}, status.HTTP_204_NO_CONTENT

    # The view paginates the queryset itself, so this returns the queryset rather than a ServiceResponse
    def get_list(self, request: AuthenticatedRequest) -> QuerySet[KanbanBoard]:  # type: ignore[override]
        # Correlated EXISTS rather than id__in - on MySQL the IN form walks every kanban_board the user can see
        # before filtering, where EXISTS lets the database walk kanban_boards and check each one
        object_assignment_results = ObjectAssignment.objects.filter(
            kanban_board_id=OuterRef("pk"),
            is_deleted=False,
            group_id__in=UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            ).values(
                "group_id",
            ),
        )

        kanban_board_results = KanbanBoard.objects.filter(
            Exists(object_assignment_results),
            is_deleted=False,
        )

        # Filter by search parameter in the query string
        search = request.query_params.get("search", None)
        if search is not None:
            # Translate search to id
            search_id = int(search) if str.isdigit(search) else None

            # Apply search filter
            kanban_board_results = kanban_board_results.filter(
                Q(title__icontains=search) | Q(id=search_id)
            )

        show_closed = request.query_params.get("show_closed", None)
        if not show_closed == "true":
            # Hide all the closed
            kanban_board_results = kanban_board_results.exclude(
                status=KanbanBoardStatusChoice.CLOSED,
            )

        return kanban_board_results

    def retrieve(self, request: AuthenticatedRequest) -> ServiceResponse:
        kanban_board_results = KanbanBoard.objects.filter(
            is_deleted=False,
            pk=self.location_id,
        ).first()
        if kanban_board_results is None:
            return "KanbanBoard does not exist", status.HTTP_404_NOT_FOUND

        # Get assigned object
        object_assignments = ObjectAssignment.objects.filter(
            is_deleted=False,
            kanban_board_id=self.location_id,
        )

        # Define groups list
        # group_list and user_list are extra attributes the serializer reads
        kanban_board_results.group_list = Group.objects.filter(
            is_deleted=False,
            id__in=object_assignments.filter(
                group_id__isnull=False,
            ).values("group_id"),
        )

        # Define user list
        kanban_board_results.user_list = User.objects.filter(
            pk__in=object_assignments.filter(
                assigned_user__isnull=False,
            ).values("assigned_user_id"),
        ).annotate(profile_picture=F("userprofilepicture__document_id__key"))

        # Append extra data

        # Create the serializer
        serializer = KanbanBoardSerializer(
            kanban_board_results,
            context={
                "request": request,
                "method": "GET",
            },
        )

        return serializer.data, status.HTTP_200_OK

    def update(self, request: AuthenticatedRequest, _: None) -> ServiceResponse:
        # Get kanban_board
        kanban_board = KanbanBoard.objects.get(pk=self.location_id)

        # Setup serializer
        serializer = KanbanBoardSerializer(
            kanban_board,
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
            kanban_board = KanbanBoard.objects.select_for_update().get(pk=self.location_id)
            serializer.instance = kanban_board
            before = AuditService.snapshot(kanban_board)
            serializer.save(change_user=request.user)
            AuditService.record_update(request, self.destination, before, kanban_board)

        return serializer.data, status.HTTP_200_OK
