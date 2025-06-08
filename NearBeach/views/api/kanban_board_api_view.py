from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.generics import get_object_or_404
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach.models import (
    Group,
    KanbanBoard,
    KanbanCard,
    KanbanColumn,
    KanbanLevel,
    ObjectAssignment,
    Organisation,
    UserGroup,
)
from NearBeach.serializers.kanban_board_list_serializer import KanbanBoardListSerializer
from NearBeach.serializers.kanban_board_serializer import KanbanBoardSerializer
from NearBeach.serializers.kanban_card_serializer import KanbanCardSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.views.document_views import transfer_new_object_uploads


class KanbanBoardViewSet(viewsets.ModelViewSet):
    # Setup the queryset and serialiser class
    queryset = KanbanBoard.objects.filter(is_deleted=False)
    serializer_class = KanbanBoardSerializer

    @check_user_api_permissions(min_permission_level=3)
    def create(self, request, *args, **kwargs):
        serializer = KanbanBoardSerializer(data=request.data, context={'request': request})
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

        # Get the column and level data
        column_property_list = request.data.getlist("column_property", [])
        if column_property_list is None or len(column_property_list) == 0:
            return Response(
                "Column Properties are missing",
                status=status.HTTP_400_BAD_REQUEST,
            )

        column_title_list = request.data.getlist("column_title", [])
        if column_title_list is None or len(column_title_list) == 0:
            return Response(
                "Column Titles are missing",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not len(column_title_list) == len(column_property_list):
            return Response(
                "Column Title count does not match Column Property count",
                status=status.HTTP_400_BAD_REQUEST,
            )

        level_title_list = request.data.getlist("level_title", [])
        if level_title_list is None or len(level_title_list) == 0:
            return Response(
                "Level Titles are missing",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check to make sure the kanban_board_name is unique
        count_kanban_board_name = len(KanbanBoard.objects.filter(
            is_deleted=False,
            kanban_board_name=serializer.validated_data['kanban_board_name'],
        ))
        if count_kanban_board_name > 0:
            return Response(
                "Kanban Board Name is not unique. Please supply a unique name",
                status=status.HTTP_400_BAD_REQUEST,
            )

        kanban_board = serializer.save(change_user=request.user, creation_user=request.user)

        return Response(
            data=kanban_board,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete kanban boards.


# ✅ Notes

Users will need to have the permission to delete.
        """
    )
    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        kanban_board = self.get_object()
        kanban_board.is_deleted = True
        kanban_board.change_user = request.user
        kanban_board.save()
        return Response(
            data='kanban board deleted',
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        description="""
# 📌 Description

Lists all kanban boards within NearBeach.


# ✅ Notes

- Pagination is enabled on this list. Use `?Page=` to navigate to the appropriate page.
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

        kanban_board_results = KanbanBoard.objects.filter(
            is_deleted=False,
            kanban_board_id__in=object_assignment_results.values("kanban_board_id"),
        )

        # Handle pagination
        page = self.paginate_queryset(kanban_board_results)
        if page is not None:
            serializer = KanbanBoardListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = KanbanBoardListSerializer(kanban_board_results, many=True)

        return Response(serializer.data)

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single kanban board.

    """
    )
    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = KanbanBoard.objects.all()
        kanban_board_results = get_object_or_404(
            queryset,
            pk=pk
        )

        # Get Extra Attributes for the data
        kanban_board_results.kanban_column = KanbanColumn.objects.filter(
            is_deleted=False,
            kanban_board_id=kanban_board_results.kanban_board_id,
        )

        kanban_board_results.kanban_level = KanbanLevel.objects.filter(
            is_deleted=False,
            kanban_board_id=kanban_board_results.kanban_board_id,
        )

        kanban_board_results.kanban_card = KanbanCard.objects.filter(
            is_deleted=False,
            kanban_board_id=pk,
        )

        serializer = KanbanBoardSerializer(kanban_board_results)
        return Response(serializer.data)
