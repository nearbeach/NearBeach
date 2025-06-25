from rest_framework import serializers
from NearBeach.models import (
    Group,
    Requirement, ListOfRequirementType, Organisation, ObjectAssignment, ListOfRequirementStatus,
)
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.serializers.requirement_item_serializer import RequirementItemSerializer
from NearBeach.serializers.requirement_status_serializer import RequirementStatusSerializer
from NearBeach.serializers.requirement_type_serializer import RequirementTypeSerializer


class RequirementSerializer(serializers.ModelSerializer):
    group_list = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
        many=True,
        required=True,
        write_only=True,
    )
    organisation = OrganisationSerializer()
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
    requirement_status = RequirementStatusSerializer()
    requirement_title = serializers.CharField(
        max_length=255,
        required=True,
    )
    requirement_type = RequirementTypeSerializer()
    uuid = serializers.UUIDField(
        required=False,
        write_only=True,
    )

    def create(self, validated_data):
        group_list = validated_data.pop("group_list")
        user = validated_data["change_user"]

        requirement = Requirement.objects.create(**validated_data)

        # Assign requirement to the groups
        for single_group in group_list:
            # Save the group against the new requirement
            submit_object_assignment = ObjectAssignment(
                group_id=single_group,
                requirement=requirement,
                change_user=user,
            )
            submit_object_assignment.save()

        return requirement

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        if self.context["request"].method in ["PUT", "POST"]:
            fields["requirement_type"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfRequirementType.objects.filter(
                    is_deleted=False,
                ),
                required=True,
            )
            fields["requirement_status"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfRequirementStatus.objects.filter(
                    is_deleted=False,
                ),
                required=True,
            )
            fields["organisation"] = serializers.PrimaryKeyRelatedField(
                queryset=Organisation.objects.filter(
                    is_deleted=False,
                ),
                required=True,
            )

        # Updating a new requirement
        if self.context['request'].method == "PUT":
            fields.pop("organisation", None)
            fields.pop("group_list", None)

        return fields

    class Meta:
        model = Requirement
        fields = [
            "requirement_id",
            "requirement_title",
            "requirement_scope",
            "requirement_status",
            "requirement_type",
            "organisation",
            "requirement_item",
            "uuid",
            "group_list",
        ]
        