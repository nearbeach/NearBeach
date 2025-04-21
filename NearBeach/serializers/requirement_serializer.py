from rest_framework import serializers
from NearBeach.models import (
    Group,
    Organisation,
    ListOfRequirementStatus,
    ListOfRequirementType,
)
from NearBeach.serializers.requirement_item_serializer import RequirementItemSerializer


class RequirementSerializer(serializers.Serializer):
    group_list = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
        required=True,
        write_only=True,
    )
    organisation_id = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Organisation.objects.filter(
            is_deleted=False,
        ),
        required=True,
    )
    organisation_name = serializers.ReadOnlyField(
        source='organisation.organisation_name',
    )
    requirement_id = serializers.IntegerField(
        read_only=True,
    )
    requirement_item = RequirementItemSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    requirement_scope = serializers.CharField(
        required=True,
    )
    requirement_status = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=ListOfRequirementStatus.objects.filter(
            is_deleted=False,
        ),
    )
    requirement_status_name = serializers.ReadOnlyField(
        source='requirement_status.requirement_status',
    )
    requirement_title = serializers.CharField(
        max_length=255,
        required=True,
    )
    requirement_type = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=ListOfRequirementType.objects.filter(
            is_deleted=False,
        ),
    )
    requirement_type_name = serializers.ReadOnlyField(
        source='requirement_type.requirement_type'
    )
    uuid = serializers.UUIDField(
        required=False,
        write_only=True,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating a new requirement
        if self.context['request'].method == "PUT":
            fields.pop("organisation_id", None)
            fields.pop("group_list", None)

        return fields
