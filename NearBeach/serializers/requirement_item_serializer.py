from rest_framework import serializers
from NearBeach.models import (
    ListOfRequirementItemStatus,
    ListOfRequirementItemType,
    OBJECT_CARD_PRIORITY,
    RequirementItem,
)

class RequirementItemSerializer(serializers.ModelSerializer):
    # requirement_item_status_id = serializers.PrimaryKeyRelatedField(
    #     queryset=ListOfRequirementItemStatus.objects.filter(
    #         is_deleted=False,
    #     )
    # )
    requirement_item_status_name = serializers.ReadOnlyField(
        source="requirement_item_status.requirement_item_status",
    )
    # requirement_item_type_id = serializers.PrimaryKeyRelatedField(
    #     queryset=ListOfRequirementItemType.objects.filter(
    #         is_deleted=False,
    #     )
    # )
    requirement_item_type_name = serializers.ReadOnlyField(
        source="requirement_item_type.requirement_item_type",
    )
    requirement_item_priority = serializers.ChoiceField(
        choices=OBJECT_CARD_PRIORITY,
        required=False,
    )
    requirement_item_priority_text = serializers.ReadOnlyField(
        source="get_requirement_item_priority_display",
    )
    requirement_item_scope = serializers.CharField(
        required=True,
    )

    class Meta:
        model = RequirementItem
        exclude = [
            "date_modified",
            "change_user",
            "is_deleted",
            "ri_story_point_min",
            "ri_story_point_max",
            # "requirement_item_status",
            # "requirement_item_type",
            "requirement",
        ]
        
    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating a new task
        if self.context['request'].method == "PUT":
            fields["requirement_item_priority"].required = True

        return fields
