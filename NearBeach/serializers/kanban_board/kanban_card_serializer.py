from NearBeach.serializers.project_serializer import ProjectSerializer
from NearBeach.serializers.requirement_item_serializer import RequirementItemSerializer
from NearBeach.serializers.requirement_serializer import RequirementSerializer
from NearBeach.serializers.task_serializer import TaskSerializer
from rest_framework import serializers
from NearBeach.serializers.kanban_board.kanban_column_serializer import KanbanColumnSerializer
from NearBeach.serializers.kanban_board.kanban_level_serializer import KanbanLevelSerializer
from NearBeach.models.kanban_board.kanban_card import KanbanCard
from NearBeach.serializers.abstraction.meta_data_serializer_mixin import MetaDataSerializerMixin
from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.utils.enums.object_enums import ObjectPriority


class KanbanCardSerializer(MetaDataSerializerMixin, serializers.ModelSerializer, BaseObjectSerializer):
    """Class containing serializer base for all objects"""

    kanban_column = KanbanColumnSerializer()
    kanban_level = KanbanLevelSerializer()
    priority = EnumField(
        enum=ObjectPriority,
        required=False,
    )
    project = ProjectSerializer(
        allow_null=True,
        required=False,
    )
    requirement = RequirementSerializer(
        allow_null=True,
        required=False,
    )
    requirement_item = RequirementItemSerializer(
        allow_null=True,
        required=False,
    )
    task = TaskSerializer(
        allow_null=True,
        required=False,
    )

    def create(self, validated_data):
        """Method for creating a kanban_card"""
        kanban_card = KanbanCard.objects.create(**validated_data)

        return kanban_card

    def get_fields(self):
        fields = super().get_fields()

        return fields

    class Meta:
        model = KanbanCard
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "sort_number",
            "kanban_level",
            "kanban_column",
            "task",
            "requirement",
            "requirement_item",
            "meta_data",
        ]


class KanbanCardDetailSerializer(KanbanCardSerializer):
    """The shape of a single kanban_card (GET): groups are readable here and the users are included.

    Exists so the API documentation can describe retrieve accurately; the endpoint itself passes
    `context={"method": "GET"}` to KanbanCardSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "GET"}

        return super().get_fields()


class KanbanCardPatchSerializer(KanbanCardSerializer):
    """The PATCH shape of a kanban_card - request and response (no groups, organisation or users; status is an id).

    Exists so the API documentation can describe PATCH accurately; the endpoint itself passes
    `context={"method": "PATCH"}` to KanbanCardSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "PATCH"}
        fields = super().get_fields()

        # Read-only, and only ever filled in by a GET of a single kanban_card
        fields.pop("user_list", None)

        return fields
