from rest_framework import serializers
from NearBeach.models import (
    ChangeTask,
    Group,
    ListOfRFCStatus,
    RequestForChange,
    RFC_TYPE,
    RFC_PRIORITY,
    RFC_RISK,
    RFC_IMPACT,
    RFC_STATUS,
)
from NearBeach.serializers.change_task_serializer import ChangeTaskSerializer


class RequestForChangeSerializer(serializers.ModelSerializer):
    change_task = ChangeTaskSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    group_list = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
        required=True,
        write_only=True,
    )
    rfc_implementation_start_date = serializers.ReadOnlyField()
    rfc_implementation_end_date = serializers.ReadOnlyField()
    rfc_status = serializers.PrimaryKeyRelatedField(
        queryset=ListOfRFCStatus.objects.filter(
            is_deleted=False,
        ),
    )
    rfc_status_name = serializers.ReadOnlyField(
        source="rfc_status.rfc_status",
    )
    rfc_type_name = serializers.CharField(
        source="get_rfc_type_display",
        read_only=True,
    )
    rfc_priority_name = serializers.CharField(
        source="get_rfc_priority_display",
        read_only=True,
    )
    rfc_risk = serializers.ChoiceField(
        choices=RFC_RISK,
        required=True,
    )
    rfc_risk_name = serializers.CharField(
        source="get_rfc_risk_display",
        read_only=True,
    )
    rfc_impact = serializers.ChoiceField(
        choices=RFC_IMPACT,
        required=True,
    )
    rfc_impact_name = serializers.CharField(
        source="get_rfc_impact_display",
        read_only=True,
    )
    rfc_version_number = serializers.CharField(
        required=True,
    )
    rfc_priority = serializers.ChoiceField(
        choices=RFC_PRIORITY,
        required=True,
    )
    rfc_type = serializers.ChoiceField(
        choices=RFC_TYPE,
        required=True,
    )
    date_created = serializers.ReadOnlyField()
    date_modified = serializers.ReadOnlyField()
    uuid = serializers.UUIDField(
        required=False,
        write_only=True,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Creating a new Request For Change
        if self.context["request"].method == "POST":
            fields.pop("rfc_implementation_release_date", None)
            fields.pop("rfc_status", None)

        # Updating a new Request For Change
        if self.context['request'].method == "PUT":
            fields.pop("group_list", None)
            fields.pop("rfc_lead", None)
            fields.pop("rfc_priority", None)
            fields.pop("rfc_risk", None)
            fields.pop("rfc_impact", None)
            fields.pop("rfc_risk_and_impact_analysis", None)
            fields.pop("rfc_implementation_plan", None)
            fields.pop("rfc_backout_plan", None)
            fields.pop("rfc_test_plan", None)
            fields.pop("rfc_status", None)

        return fields

    class Meta:
        model = RequestForChange
        exclude = [
            "change_user",
            "creation_user",
            "is_deleted",
        ]

