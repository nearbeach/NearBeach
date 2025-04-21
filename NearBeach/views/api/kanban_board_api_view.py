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
            kanban_board_name=serializer.data.get("kanban_board_name"),
        ))
        if count_kanban_board_name > 0:
            return Response(
                "Kanban Board Name is not unique. Please supply a unique name",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Submit kanban board data
        kanban_board_submit = KanbanBoard(
            kanban_board_name=serializer.data.get("kanban_board_name"),
            creation_user=request.user,
            change_user=request.user
        )
        kanban_board_submit.save()

        # Assign task to the groups
        for single_group in group_list:
            group_instance = Group.objects.get(
                group_id=single_group,
            )

            # Save the group against the new task
            submit_object_assignment = ObjectAssignment(
                group_id=group_instance,
                change_user=request.user,
                kanban_board=kanban_board_submit,
            )
            submit_object_assignment.save()

        # Create the required columns
        for index, column_title in enumerate(column_title_list, start=0):
            submit_kanban_column = KanbanColumn(
                kanban_column_name=column_title,
                kanban_column_property=column_property_list[index],
                kanban_column_sort_number=index,
                kanban_board=kanban_board_submit,
                change_user=request.user
            )
            submit_kanban_column.save()

        # Create the required levels
        for index, level_title in enumerate(level_title_list, start=0):
            submit_kanban_level = KanbanLevel(
                kanban_level_name=level_title,
                kanban_level_sort_number=index,
                kanban_board=kanban_board_submit,
                change_user=request.user
            )
            submit_kanban_level.save()

        return Response(
            data={ "kanban_board_id": kanban_board_submit.kanban_board_id },
            status=status.HTTP_201_CREATED,
        )

    @check_user_api_permissions(min_permission_level=4)
    def destroy(self, request, *args, **kwargs):
        kanban_board = self.get_object()
        kanban_board.is_deleted = True
        kanban_board.change_user = request.user
        kanban_board.save()
        return Response(data='kanban board deleted')

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

        kanban_board_results = KanbanBoard.objects.filter(
            is_deleted=False,
            kanban_board_id__in=object_assignment_results.values("kanban_board_id"),
        )[(page - 1) * page_size : page * page_size]

        serializer = KanbanBoardSerializer(kanban_board_results, many=True)

        return Response(serializer.data)

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
