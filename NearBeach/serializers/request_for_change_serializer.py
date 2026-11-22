from NearBeach.utils.enums.request_for_change_enums import RequestForChangeStatus, RequestForChangePriority, \
    RequestForChangeType, RequestForChangeRisk, RequestForChangeImpact
from rest_framework import serializers
from NearBeach.models.request_for_change.request_for_change import RequestForChange
from NearBeach.serializers.abstraction.meta_data_serializer_mixin import MetaDataSerializerMixin
from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.group_serializer import GroupSerializer
from NearBeach.serializers.user.user_serializer import UserSerializer
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment


class RequestForChangeSerializer(MetaDataSerializerMixin, serializers.ModelSerializer, BaseObjectSerializer):
    """Class containing serializer base for all objects"""

    # TODO - put this in alphabetical order
    priority = EnumField(
        enum=RequestForChangePriority,
        required=False,
    )
    risk = EnumField(
        enum=RequestForChangeRisk,
        required=False,
    )
    status = EnumField(
        enum=RequestForChangeStatus,
        required=False,
    )
    type = EnumField(
        enum=RequestForChangeType,
        required=False,
    )
    impact = EnumField(
        enum=RequestForChangeImpact,
        required=False,
    )
    lead = UserSerializer(
        # TODO - set the write ability
        read_only=True,
    )

    def create(self, validated_data):
        """Method for creating a request_for_change"""
        group_list = validated_data.pop("group_list", [])

        # Extract data we need
        validated_data["priority"] = RequestForChangePriority.MEDIUM
        validated_data["risk"] = RequestForChangeRisk.MODERATE
        validated_data["status"] = RequestForChangeStatus.DRAFT
        validated_data["type"] = RequestForChangeType.MEDIUM

        # Create the request_for_change
        request_for_change = RequestForChange.objects.create(**validated_data)

        # Create the group list
        for single_group in group_list:
            # Save the group against the new request_for_change
            submit_object_assignment = ObjectAssignment(
                group=single_group,
                request_for_change=request_for_change,
                change_user=validated_data["change_user"],
                creation_user=validated_data["creation_user"],
            )
            submit_object_assignment.save()

        return request_for_change

    def get_fields(self):
        fields = super().get_fields()

        # PATCH
        method = self.context.get("method", None)
        if method == "PATCH":
            fields.pop("group_list", None)
            fields.pop("organisation", None)

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
        model = RequestForChange
        fields = [
            "id",
            "title",
            "description",
            "type",
            "implementation_start_date",
            "implementation_end_date",
            "implementation_release_date",
            "version_number",
            "status",
            "lead",
            "priority",
            "risk",
            "impact",
            "risk_and_impact_analysis",
            "implementation_plan",
            "backout_plan",
            "test_plan",
        ]


class RequestForChangeDetailSerializer(RequestForChangeSerializer):
    """The shape of a single request_for_change (GET): groups are readable here and the users are included.

    Exists so the API documentation can describe retrieve accurately; the endpoint itself passes
    `context={"method": "GET"}` to RequestForChangeSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "GET"}

        return super().get_fields()


class RequestForChangePatchSerializer(RequestForChangeSerializer):
    """The PATCH shape of a request_for_change - request and response (no groups, organisation or users; status is an id).

    Exists so the API documentation can describe PATCH accurately; the endpoint itself passes
    `context={"method": "PATCH"}` to RequestForChangeSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "PATCH"}
        fields = super().get_fields()

        # Read-only, and only ever filled in by a GET of a single request_for_change
        fields.pop("user_list", None)

        return fields
