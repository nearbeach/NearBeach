from rest_framework import serializers
from NearBeach.models import RequirementItem


class RequirementItemSerializer(serializers.ModelSerializer):
    requirement_item_status_name = serializers.ReadOnlyField(
        source="requirement_item_status.requirement_item_status",
    )
    requirement_item_type_name = serializers.ReadOnlyField(
        source="requirement_item_type.requirement_item_type",
    )

    class Meta:
        model = RequirementItem
        exclude = [
            "date_modified",
            "change_user",
            "is_deleted",
            "ri_story_point_min",
            "ri_story_point_max",
        ]
