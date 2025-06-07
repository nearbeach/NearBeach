from rest_framework import serializers
from NearBeach.models import KanbanCard, Project, KanbanColumn, KanbanLevel
from NearBeach.utils.enums import ObjectPriority
from NearBeach.serializers.tag_serializer import TagSerializer
from NearBeach.models import Tag, TagAssignment


class KanbanCardSerializer(serializers.ModelSerializer):
    kanban_card_text = serializers.CharField(
        required=True,
    )
    kanban_card_priority = serializers.ChoiceField(
        choices=ObjectPriority,
        required=True,
    )
    kanban_card_description = serializers.CharField(
        required=True,
    )
    kanban_column_id = serializers.PrimaryKeyRelatedField(
        queryset=KanbanColumn.objects.filter(
            is_deleted=False,
        ),
        required=True,
    )
    kanban_column_name = serializers.ReadOnlyField(
        source='kanban_column.kanban_column_name',
    )
    kanban_level_id = serializers.PrimaryKeyRelatedField(
        queryset=KanbanLevel.objects.filter(
            is_deleted=False,
        ),
        required=True,
    )
    kanban_level_name = serializers.ReadOnlyField(
        source='kanban_level.kanban_level_name',
    )
    kanban_card_sort_number = serializers.IntegerField(
        required=False,
    )
    project = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        many=False,
        read_only=True,
    )
    requirement = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        many=False,
        read_only=True,
    )
    task = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        many=False,
        read_only=True,
    )
    tags = serializers.SerializerMethodField()

    class Meta:
        model = KanbanCard
        exclude = [
            "kanban_board",
            "kanban_column",
            "kanban_level",
            "is_archived",
            "date_modified",
            "change_user",
            "is_deleted",
        ]

    @staticmethod
    def get_tags(obj):
        # We don't always have this field
        if not hasattr(obj, "kanban_card_id"):
            return []

        # Get the tag data for the current card
        tag_results = Tag.objects.filter(
            is_deleted=False,
            tag_id__in=TagAssignment.objects.filter(
                is_deleted=False,
                object_enum="kanban_card",
                object_id=obj.kanban_card_id,
            ).values("tag_id"),
        )

        return TagSerializer(tag_results, many=True).data
