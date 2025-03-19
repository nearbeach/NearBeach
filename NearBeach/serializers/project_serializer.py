from rest_framework import serializers
from NearBeach.models import (
    Group,
    ListOfProjectStatus,
    OBJECT_CARD_PRIORITY,
    Organisation,
)


# We are using serializers.Serializer because "group_list" is not in the project table
class ProjectSerializer(serializers.Serializer):
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
    project_description = serializers.CharField(
        required=True,
    )
    project_end_date = serializers.DateTimeField(
        required=True,
    )
    project_higher_order_status = serializers.ReadOnlyField(
        source='project_status.project_higher_order_status',
    )
    project_id = serializers.IntegerField(
        read_only=True,
    )
    project_name = serializers.CharField(
        max_length=255,
        required=True,
    )
    project_priority = serializers.ChoiceField(
        choices=OBJECT_CARD_PRIORITY,
    )
    project_priority_name = serializers.ReadOnlyField(
        source='get_project_priority_display',
    )
    project_start_date = serializers.DateTimeField(
        required=True,
    )
    project_status = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=ListOfProjectStatus.objects.filter(
            is_deleted=False,
        ),
    )
    project_status_name = serializers.ReadOnlyField(
        source='project_status.project_status',
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

        # Creating a new project
        if self.context["request"].method == "POST":
            fields.pop("project_status", None)
            fields.pop("project_priority", None)

        # Updating a new project
        if self.context['request'].method == "PUT":
            fields.pop("group_list", None)
            fields.pop("organisation_id", None)

        return fields
