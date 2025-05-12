from rest_framework import serializers
from NearBeach.models import ObjectAssignment


class ObjectAssignmentGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(
        source='group_id.group_name',
    )
    object_assignment_id = serializers.ReadOnlyField
    parent_group_id = serializers.ReadOnlyField(
        source='group_id.parent_group_id',
    )

    class Meta:
        model = ObjectAssignment
        fields = [
            "group_id",
            "group_name",
            "object_assignment_id",
            "parent_group_id",
        ]