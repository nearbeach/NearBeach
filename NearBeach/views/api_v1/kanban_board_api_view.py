from NearBeach.decorators.check_user_permissions.destination_permission import destination_permission
from NearBeach.decorators.check_user_permissions.object_permission import object_permission
from NearBeach.serializers.kanban_board.kanban_board_serializer import KanbanBoardSerializer
from NearBeach.services.kanban_board.KanbanBoardServices import KanbanBoardService
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response


@extend_schema(
    exclude=True,
)
class KanbanBoardViewSet(viewsets.ViewSet):
    serializer_class = None

    @staticmethod
    @destination_permission(min_permission_level=3)
    def create(request, *args, **kwargs) -> Response:
        kanban_board_service = KanbanBoardService(destination="kanban_board", location_id=0)
        data, http_status = kanban_board_service.create(request)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=4)
    def destroy(request, pk, *args, **kwargs):
        kanban_board_service = KanbanBoardService(destination="kanban_board", location_id=pk)
        data, http_status = kanban_board_service.delete(request, None)

        return Response(
            data=data,
            status=http_status,
        )

    @destination_permission(min_permission_level=1)
    def list(self, request, *args, **kwargs) -> Response:
        """Method for getting a list of all projects through search"""
        kanban_board_service = KanbanBoardService(destination="kanban_board", location_id=0)
        kanban_board_results = kanban_board_service.get_list(request)

        page = self.paginate_queryset(kanban_board_results)
        if page is not None:
            serializer = KanbanBoardSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(
            data={"Issue with pagination of object"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    @object_permission(min_permission_level=2)
    def partial_update(request, pk, *args, **kwargs) -> Response:
        kanban_board_service = KanbanBoardService(destination="project", location_id=pk)
        data, http_status = kanban_board_service.update(request, None)

        return Response(
            data=data,
            status=http_status,
        )

    @staticmethod
    @object_permission(min_permission_level=1)
    def retrieve(request, pk, *args, **kwargs) -> Response:
        kanban_board_service = KanbanBoardService(destination="project", location_id=pk)
        data, http_status = kanban_board_service.retrieve(request)

        return Response(
            data=data,
            status=http_status,
        )
