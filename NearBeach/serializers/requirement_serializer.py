from NearBeach.serializers.object_data.types.requirement_types_serializer import RequirementTypesSerializer
from rest_framework import serializers
from NearBeach.models import ListOfRequirementStatus, Requirement, ListOfRequirementType
from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.abstraction.date_fields_serializer import DateFieldsSerializer
from NearBeach.serializers.group_serializer import GroupSerializer
from NearBeach.serializers.object_data.status.requirement_status_serializer import RequirementStatusSerializer
from NearBeach.serializers.user.user_serializer import UserSerializer
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment


class RequirementSerializer(serializers.ModelSerializer, BaseObjectSerializer, DateFieldsSerializer):
    """Class containing serializer base for all objects"""

    status = RequirementStatusSerializer(
        many=False,
        read_only=False,
        allow_null=False,
        required=False,
    )
    type = RequirementTypesSerializer(
        many=False,
        read_only=False,
        allow_null=False,
        required=False,
    )

    def create(self, validated_data):
        """Method for creating a requirement"""
        group_list = validated_data.pop("group_list", [])

        # Extract data we need
        validated_data["status"] = ListOfRequirementStatus.objects.filter(
            is_deleted=False
        ).order_by(
            "sort_order",
        ).first()

        validated_data["type"] = ListOfRequirementType.objects.filter(
            is_deleted=False
        ).order_by(
            "sort_order",
        ).first()

        # Create the requirement
        requirement = Requirement.objects.create(**validated_data)

        # Create the group list
        for single_group in group_list:
            # Save the group against the new requirement
            submit_object_assignment = ObjectAssignment(
                group=single_group,
                requirement=requirement,
                change_user=validated_data["change_user"],
            )
            submit_object_assignment.save()

        return requirement

    def get_fields(self):
        fields = super().get_fields()

        # PATCH
        method = self.context.get("method", None)
        if method == "PATCH":
            fields.pop("group_list", None)
            fields["status"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfRequirementStatus.objects.filter(
                    is_deleted=False,
                ),
            )

        if method == "GET":
            fields["group_list"] = GroupSerializer(
                many=True,
                read_only=True,
                required=False,
            )

            fields["user_list"] = UserSerializer(
                many=True,
                read_only=True,
                required=False,
            )

        return fields

    class Meta:
        model = Requirement
        fields = [
            "id",
            "title",
            "description",
            "status",
            "type",
            "group_list",
            "user_list",
            "date_created",
            "date_modified",
        ]
