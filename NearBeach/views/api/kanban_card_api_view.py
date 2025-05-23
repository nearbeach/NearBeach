from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from NearBeach.models import (
    KanbanBoard,
    KanbanCard,
)
from NearBeach.serializers.kanban_card_serializer import KanbanCardSerializer
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions


class KanbanCardViewSet(viewsets.ModelViewSet):
    queryset = KanbanCard.objects.filter(is_deleted=False)
    serializer_class = KanbanCardSerializer

    def create(self, request, *args, **kwargs):
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    def destroy(self, request, *args, **kwargs):
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    @check_user_api_permissions(min_permission_level=1)
    def list(self, request, *args, **kwargs):
        page_size = int(request.query_params.get("page_size", 100))
        page_size = page_size if page_size <= 1000 else 1000
        page = int(request.query_params.get("page", 1))

        kanban_card_results = KanbanCard.objects.filter(
            is_deleted=False,
            kanban_board_id=kwargs["kanban_board_id"],
        )

        serializer = KanbanCardSerializer(kanban_card_results, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        return status.HTTP_500_INTERNAL_SERVER_ERROR
