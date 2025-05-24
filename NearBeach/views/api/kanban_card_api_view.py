from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.models import (
    KanbanBoard,
    KanbanCard,
    KanbanColumn,
    KanbanLevel,
)
from NearBeach.serializers.kanban_card_serializer import KanbanCardSerializer
from NearBeach.serializers.tag_serializer import TagSerializer
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions


class KanbanCardViewSet(viewsets.ModelViewSet):
    queryset = KanbanCard.objects.filter(is_deleted=False)
    serializer_class = KanbanCardSerializer

    @check_user_api_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_user_api_permissions(min_permission_level=2)
    def destroy(self, request, *args, **kwargs):
        kanban_card = self.get_object()
        kanban_card.is_deleted = True
        kanban_card.change_user = request.user
        kanban_card.save()

        return Response(
            data="kanban card deleted",
            status=status.HTTP_204_NO_CONTENT,
        )

    @check_user_api_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        kanban_card_results = KanbanCard.objects.filter(
            is_archived=False,
            is_deleted=False,
            kanban_board_id=kwargs["kanban_board_id"],
            # Don't send cards that are in deleted Columns
            kanban_column_id__in=KanbanColumn.objects.filter(
                is_deleted=False,
                kanban_board_id=kwargs["kanban_board_id"],
            ),
            # Don't send cards that are in deleted Levels
            kanban_level_id__in=KanbanLevel.objects.filter(
                is_deleted=False,
                kanban_board_id=kwargs["kanban_board_id"],
            ),
        )

        serializer = KanbanCardSerializer(kanban_card_results, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @check_user_api_permissions(min_permission_level=1)
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = KanbanCard.objects.filter(
            is_deleted=False,
        )
        kanban_card_results = get_object_or_404(
            queryset,
            pk=pk,
        )

        serializer = KanbanCardSerializer(kanban_card_results)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
