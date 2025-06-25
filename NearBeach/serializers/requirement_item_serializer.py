from rest_framework import serializers
from NearBeach.models import (
    ListOfRequirementItemStatus,
    ListOfRequirementItemType,
    RequirementItem,
)
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.requirement_item_status_serializer import RequirementItemStatusSerializer
from NearBeach.serializers.requirement_item_type_serializer import RequirementItemTypeSerializer
from NearBeach.utils.enums.object_enums import ObjectPriority


class RequirementItemSerializer(serializers.ModelSerializer):
    requirement_item_priority = EnumField(
        enum=ObjectPriority,
        required=True,
    )
    requirement_item_scope = serializers.CharField(
        required=True,
    )
    requirement_item_status = RequirementItemStatusSerializer()
    requirement_item_story_point = serializers.IntegerField(
        required=True,
    )
    requirement_item_title = serializers.CharField(
        required=True,
        max_length=255,
    )
    requirement_item_type = RequirementItemTypeSerializer()

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        if self.context["request"].method == "POST":
            fields.pop("requirement_item_story_point")
            fields.pop("requirement_item_priority")

        if self.context["request"].method in ["POST", "PUT"]:
            fields["requirement_item_status"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfRequirementItemStatus.objects.filter(
                    is_deleted=False,
                )
            )
            fields["requirement_item_type"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfRequirementItemType.objects.filter(
                    is_deleted=False,
                )
            )

        return fields

    class Meta:
        model = RequirementItem
        fields = [
            "requirement_item_id",
            "requirement_item_title",
            "requirement_item_scope",
            "requirement_item_story_point",
            "requirement_item_status",
            "requirement_item_type",
            "requirement_item_priority",
            "date_created",
        ]
