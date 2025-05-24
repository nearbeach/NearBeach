from rest_framework import serializers
from NearBeach.models import KanbanCard
from NearBeach.serializers.tag_serializer import TagSerializer
from NearBeach.models import Tag, TagAssignment


class KanbanCardSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = KanbanCard
        exclude = [
            "is_archived",
            "date_modified",
            "change_user",
            "is_deleted",
        ]

    @staticmethod
    def get_tags(obj):
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