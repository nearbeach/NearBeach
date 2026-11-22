from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.serializers.kanban_board.kanban_card_serializer import KanbanCardSerializer
from NearBeach.services.abstraction.object_services_abstraction import AuthenticatedRequest
from NearBeach.services.kanban_board.KanbanCardServices import KanbanCardService
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response


@extend_schema(
    exclude=True,
)
class KanbanCardViewSet(viewsets.ViewSet):
    serializer_class = None

    @staticmethod
    @destination_permission(min_permission_level=3)
    def create(request, *args, **kwargs) -> Response:
        kanban_card_service = KanbanCardService(destination="kanban_card", location_id=0)
        data, http_status = kanban_card_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=4)
    def destroy(request: AuthenticatedRequest, kanban_board_id: int, pk: int, *args, **kwargs):
        kanban_card_service = KanbanCardService(destination="kanban_board", location_id=kanban_board_id)
        data, http_status = kanban_card_service.delete(request, pk)

        return Response(
            data=data,
            status=http_status,
        )

    @destination_permission(min_permission_level=1)
    def list(self, request, *args, **kwargs) -> Response:
        """Method for getting a list of all projects through search"""
        kanban_card_service = KanbanCardService(destination="kanban_card", location_id=0)
        kanban_card_results = kanban_card_service.get_list(request)

        page = self.paginate_queryset(kanban_card_results)
        if page is not None:
            serializer = KanbanCardSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(
            data={"Issue with pagination of object"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def partial_update(request, kanban_board_id: int, pk: int, *args, **kwargs) -> Response:
        kanban_card_service = KanbanCardService(destination="kanban_board", location_id=kanban_board_id)
        data, http_status = kanban_card_service.update(request, pk)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(request, kanban_board_id: int, pk: int, *args, **kwargs) -> Response:
        kanban_card_service = KanbanCardService(destination="kanban_board", location_id=kanban_board_id)
        data, http_status = kanban_card_service.retrieve(request, pk)

        return Response(
            data=data,
            status=http_status,
        )
