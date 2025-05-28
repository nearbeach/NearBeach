from django.db.models import Max
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from NearBeach.decorators.check_user_permissions.partials.kanban_card_permissions import kanban_card_permissions
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
        serializer = KanbanCardSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Flatpack
        kanban_column_instance = serializer.validated_data['kanban_column_id']
        kanban_level_instance = serializer.validated_data['kanban_level_id']
        kanban_card_priority_instance = serializer.validated_data['kanban_card_priority']

        # Get the column and level data
        kanban_board_instance = get_object_or_404(
            queryset=KanbanBoard.objects.all(),
            kanban_board_id=kwargs['kanban_board_id'],
        )

        column = KanbanColumn.objects.filter(
            is_deleted=False,
            kanban_board=kanban_board_instance,
            kanban_column_id=kanban_column_instance.kanban_column_id,
        )
        if column is None or len(column) == 0:
            return Response(
                data={"Column does not exist for this Kanban Board"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        level = KanbanLevel.objects.filter(
            is_deleted=False,
            kanban_board_id=kanban_board_instance,
            kanban_level_id=kanban_level_instance.kanban_level_id,
        )
        if level is None or len(level) == 0:
            return Response(
                data={"Level does not exist for this Kanban Board"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Submit kanban card data
        sort_number = KanbanCard.objects.filter(
            kanban_column=column[0],
            kanban_level=level[0],
        ).aggregate(
            Max("kanban_card_sort_number"),
        )["kanban_card_sort_number__max"]

        if sort_number is None:
            sort_number = 0
        else:
            sort_number += 1

        kanban_card_submit = KanbanCard(
            kanban_board=kanban_board_instance,
            kanban_card_text=serializer.data.get("kanban_card_text"),
            kanban_card_description=serializer.data.get("kanban_card_description"),
            kanban_card_priority=kanban_card_priority_instance,
            kanban_column=column[0],
            kanban_level=level[0],
            kanban_card_sort_number=sort_number,
            change_user=request.user,
        )
        kanban_card_submit.save()

        # Get the new kanban card and send to user
        kanban_card_results = KanbanCard.objects.get(
            kanban_card_id=kanban_card_submit.kanban_card_id,
        )

        serializer = KanbanCardSerializer(
            kanban_card_results,
            many=False,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
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

        # Update the data - got to check the object etc.
        update_kanban_card = KanbanCard.objects.filter(
            kanban_card_id=pk,
            kanban_board_id=kwargs["kanban_board_id"],
        )
        if update_kanban_card is None or len(update_kanban_card) == 0:
            return Response(
                data={"Kanban Card does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the update kanban card
        update_kanban_card = update_kanban_card[0]
        
        # Flatpack serializer data
        new_column = serializer.validated_data['kanban_column_id']
        new_level = serializer.validated_data['kanban_level_id']

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

        # Get old level and column
        old_level = update_kanban_card.kanban_level
        old_column = update_kanban_card.kanban_column
        
        # Check to see if the card has been moved
        if new_column != old_column or new_level != old_level:
            # Card has been moved
            sort_number = KanbanCard.objects.filter(
                kanban_column=new_column,
                kanban_level=new_level,
            ).aggregate(
                Max("kanban_card_sort_number"),
            )["kanban_card_sort_number__max"]

            if sort_number is None:
                sort_number = 0
            else:
                sort_number += 1

            update_kanban_card.kanban_column = new_column
            update_kanban_card.kanban_level = new_level
            update_kanban_card.kanban_card_sort_number = sort_number

        update_kanban_card.kanban_card_text = serializer.validated_data['kanban_card_text']
        update_kanban_card.kanban_card_description = serializer.validated_data['kanban_card_description']
        update_kanban_card.kanban_card_priority = serializer.validated_data['kanban_card_priority']
        update_kanban_card.save()

        serializer = KanbanCardSerializer(update_kanban_card)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
