from django.contrib.auth.models import User
from rest_framework import serializers
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.models import (
    Group,
    RequestForChange, ObjectAssignment,
)
from NearBeach.utils.enums.request_for_change_enums import RequestForChangeStatus, RequestForChangeType, RequestForChangePriority, \
    RequestForChangeRisk, RequestForChangeImpact
from NearBeach.serializers.change_task_serializer import ChangeTaskSerializer
from NearBeach.serializers.user_django_serializer import UserDjangoSerializer


class RequestForChangeSerializer(serializers.ModelSerializer):
    change_task = ChangeTaskSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    date_created = serializers.ReadOnlyField()
    date_modified = serializers.ReadOnlyField()
    group_list = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
        many=True,
        required=True,
        write_only=True,
    )
    rfc_impact = EnumField(
        enum=RequestForChangeImpact,
    )
    rfc_implementation_end_date = serializers.ReadOnlyField()
    rfc_implementation_start_date = serializers.ReadOnlyField()
    rfc_lead = UserDjangoSerializer(
        many=False,
    )
    rfc_priority = EnumField(
        enum=RequestForChangePriority,
    )
    rfc_status = EnumField(RequestForChangeStatus)
    rfc_risk = EnumField(
        enum=RequestForChangeRisk,
    )
    rfc_version_number = serializers.CharField(
        required=True,
    )
    rfc_type = EnumField(enum=RequestForChangeType)
    uuid = serializers.UUIDField(
        required=False,
        write_only=True,
    )
    
    def create(self, validated_data):
        group_list = validated_data.pop("group_list")
        user = validated_data["change_user"]
        
        # Create the request for change
        request_for_change = RequestForChange.objects.create(**validated_data)
        
        # Assign requirement to the groups
        for single_group in group_list:
            # Save the group against the new requirement
            submit_object_assignment = ObjectAssignment(
                group_id=single_group,
                request_for_change=request_for_change,
                change_user=user,
            )
            submit_object_assignment.save()
            
        return request_for_change

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Creating a new Request For Change
        if self.context["request"].method == "POST":
            fields.pop("rfc_implementation_release_date", None)
            fields.pop("rfc_status", None)
            fields["rfc_lead"] = serializers.PrimaryKeyRelatedField(
                queryset=User.objects.filter(
                    is_active=True,
                )
            )

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
        fields = [
            "rfc_id",
            "rfc_title",
            "rfc_summary",
            "rfc_type",
            "rfc_version_number",
            "rfc_lead",
            "rfc_priority",
            "rfc_risk",
            "rfc_impact",
            "rfc_risk_and_impact_analysis",
            "rfc_implementation_plan",
            "rfc_implementation_end_date",
            "rfc_implementation_start_date",
            "rfc_implementation_release_date",
            "rfc_backout_plan",
            "rfc_test_plan",
            "date_created",
            "date_modified",
            "rfc_status",
            "change_task",
            "uuid",
            "group_list",
        ]

