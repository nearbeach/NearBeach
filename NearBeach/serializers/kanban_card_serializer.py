from django.db.models import Max
from rest_framework import serializers
from NearBeach.models import KanbanCard, Project, KanbanColumn, KanbanLevel
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.kanban_column_serializer import KanbanColumnSerializer
from NearBeach.serializers.kanban_level_serializer import KanbanLevelSerializer
from NearBeach.utils.enums.object_enums import ObjectPriority
from NearBeach.serializers.tag_serializer import TagSerializer
from NearBeach.models import Tag, TagAssignment


class KanbanCardSerializer(serializers.ModelSerializer):
    kanban_card_text = serializers.CharField(
        required=True,
    )
    kanban_card_priority = EnumField(enum=ObjectPriority)
    kanban_card_description = serializers.CharField(
        required=True,
    )
    kanban_column = KanbanColumnSerializer(
        many=False,
        read_only=False,
        allow_null=False,
    )
    kanban_level = KanbanLevelSerializer(
        many=False,
        read_only=False,
        allow_null=False,
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
        fields = [
            "kanban_card_id",
            "kanban_card_text",
            "kanban_card_description",
            "kanban_card_priority",
            "kanban_column",
            "kanban_level",
            "kanban_card_sort_number",
            "tags",
            "date_created",
            "project",
            "requirement",
            "task",
        ]

    def create(self, validated_data):
        # Sort Number
        sort_number = KanbanCard.objects.filter(
            kanban_column_id=validated_data["kanban_column"],
            kanban_level_id=validated_data["kanban_level"],
        ).aggregate(
            Max("kanban_card_sort_number"),
        )["kanban_card_sort_number__max"]

        if sort_number is None:
            sort_number = 0
        else:
            sort_number += 1
        
        validated_data["kanban_card_sort_number"] = sort_number

        # Create the kanban card
        kanban_card = KanbanCard.objects.create(**validated_data)

        return kanban_card

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating the kanban card
        if self.context['request'].method in ["POST", "PUT"]:
            fields["kanban_column"] = serializers.PrimaryKeyRelatedField(
                queryset=KanbanColumn.objects.filter(
                    is_deleted=False,
                )
            )
            fields["kanban_level"] = serializers.PrimaryKeyRelatedField(
                queryset=KanbanLevel.objects.filter(
                    is_deleted=False,
                )
            )

        return fields

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

    def update(self, instance, validated_data):
        # Get new/old level and column
        new_column = validated_data['kanban_column']
        new_level = validated_data['kanban_level']
        old_level = instance.kanban_level
        old_column = instance.kanban_column

        # Check to see if the card has been moved
        if new_column != old_column.pk or new_level != old_level.pk:
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

            instance.kanban_card_sort_number = sort_number

        # Priority
        kanban_card_priority = validated_data.pop("kanban_card_priority", 2)
        instance.kanban_card_priority = kanban_card_priority["value"]

        # Kanban Column
        instance.kanban_column_id = validated_data.pop("kanban_column")

        # Kanban Level
        instance.kanban_level_id = validated_data.pop("kanban_level")

        # Update instance
        instance = super().update(instance, validated_data)
        return instance
