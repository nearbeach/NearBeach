from django.db.models import Max
from drf_spectacular.utils import extend_schema, OpenApiExample
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
from NearBeach.decorators.check_user_permissions.api_permissions_v0 import check_user_api_permissions
from NearBeach import event_hooks


event_hooks.register_event_type("kanban_card.create", KanbanCard)


@extend_schema(
    tags=["Kanban Cards"],
)
class KanbanCardViewSet(viewsets.ModelViewSet):
    queryset = KanbanCard.objects.filter(is_deleted=False)
    serializer_class = KanbanCardSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    @extend_schema(
        description="""
# 📌 Description

Create Kanban Card against the kanban board.

# 🧾 Parameters

- Kanban Card Text: The kanban board name
- Kanban Card Description: The description for the kanban card
- Kanban Card Priority: The priority of the kanban card
    - 0 = Highest
    - 1 = High
    - 2 = Normal
    - 3 = Low
    - 4 = Lowest
- Kanban Column: The id of the kanban column you would like the card to be moved to
- Kanban Level: The id of the kanban level you would like the card to be moved to


# ✅ Notes

Both the Column/Level id's will need to exist under the current kanban board. Or an error will occur.
        """,
        examples=[
            OpenApiExample(
                "Example 1",
                description="Create a new kanban board",
                value={
                    "kanban_board_name": "My Kanban Board",
                    "group_list": [1, 2],
                    "kanban_column": [
                        {
                            "kanban_column_name": "Backlog",
                            "kanban_column_property": "Backlog",
                        },
                        {
                            "kanban_column_name": "Blocked",
                            "kanban_column_property": "Blocked",
                        },
                        {
                            "kanban_column_name": "In Progress",
                            "kanban_column_property": "Normal",
                        },
                        {
                            "kanban_column_name": "User Acceptance Testing",
                            "kanban_column_property": "Normal",
                        },
                        {
                            "kanban_column_name": "Closed",
                            "kanban_column_property": "Closed",
                        },
                    ],
                    "kanban_level": [
                        {
                            "kanban_level_name": "Swimlane 1",
                        },
                        {
                            "kanban_level_name": "Swimlane 2",
                        },
                    ],
                }
            )
        ],
    )
    @check_user_api_permissions(min_permission_level=2)
    def create(self, request, *args, **kwargs):
        serializer = KanbanCardSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the column and level data
        get_object_or_404(
            queryset=KanbanBoard.objects.filter(
                is_deleted=False,
            ),
            kanban_board_id=kwargs['kanban_board_id'],
        )

        # Do some data checking first
        new_column = serializer.validated_data['kanban_column']
        new_level = serializer.validated_data['kanban_level']

        if int(new_column.kanban_board_id) != int(kwargs["kanban_board_id"]):
            return Response(
                data={"Column does not exist for this Kanban Board"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if int(new_level.kanban_board_id) != int(kwargs["kanban_board_id"]):
            return Response(
                data={"Level does not exist for this Kanban Board"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        kanban_card = serializer.save(
            change_user=request.user,
            kanban_board_id=kwargs["kanban_board_id"],
        )

        # Apply the event hooks
        event_hooks.emit("kanban_card.create", kanban_card)

        # Re-serialize the results
        serializer = KanbanCardSerializer(
            kanban_card,
            many=False,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        description="""
# 📌 Description

Delete kanban card.


# ✅ Notes

Users will need to have the permission to delete. This entails having the ability to edit a kanban board.
        """
    )
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

    @extend_schema(
        description="""
# 📌 Description

Lists all kanban cards within the kanban board.
    """
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

    @extend_schema(
        description="""
# 📌 Description

Retrieves a single kanban card.

    """
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

    @extend_schema(
        description="""
# 📌 Description

Updates a single kanban card under the kanban board

# 🧾 Parameters

- Kanban Card Text: The kanban card's title
- Kanban Card Description: The description of the kanban card
- Kanban Card Priority: The priority of the kanban card
    - 0 = Highest
    - 1 = High
    - 2 = Normal
    - 3 = Low
    - 4 = Lowest
- Kanban Column: The id of the kanban column you would like the card to be moved to
- Kanban Level: The id of the kanban level you would like the card to be moved to


# ✅ Notes

Both the Column/Level id's will need to exist under the current kanban board. Or an error will occur.
    """
    )
    @check_user_api_permissions(min_permission_level=2)
    def update(self, request, pk=None, *args, **kwargs):
        serializer = KanbanCardSerializer(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the kanban card
        update_kanban_card = get_object_or_404(
            queryset=KanbanCard.objects.filter(
                is_deleted=False,
                kanban_board_id=kwargs["kanban_board_id"],
            ),
            pk=pk,
        )
        
        # Do some data checking first
        new_column = serializer.validated_data['kanban_column']
        new_level = serializer.validated_data['kanban_level']

        if int(new_column.kanban_board_id) != int(kwargs["kanban_board_id"]):
            return Response(
                data={"Column does not exist for this Kanban Board"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if int(new_level.kanban_board_id) != int(kwargs["kanban_board_id"]):
            return Response(
                data={"Level does not exist for this Kanban Board"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the kanban card
        update_kanban_card = serializer.update(
            update_kanban_card,
            serializer.data,
        )

        # Re-serializer everything
        serializer = KanbanCardSerializer(update_kanban_card, many=False)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
