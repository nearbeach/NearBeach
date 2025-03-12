from rest_framework import serializers
from NearBeach.models import (
    Group,
    ListOfProjectStatus,
    Project,
    OBJECT_CARD_PRIORITY,
    Organisation,
)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    group_list = serializers.MultipleChoiceField(
        write_only=True,
        required=True,
        choices=Group.objects.filter(
            is_deleted=False,
        ).values_list(
            "group_id",
            "group_name",
        ),
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
    project_end_date = serializers.DateTimeField(
        required=True,
    )
    project_higher_order_status = serializers.ReadOnlyField(
        source='project_status.project_higher_order_status',
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

    class Meta:
        model = Project
        fields = [
            "project_id",
            "project_name",
            "project_description",
            "organisation_id",
            "organisation_name",
            "project_start_date",
            "project_end_date",
            "project_status",
            "project_status_name",
            "project_higher_order_status",
            "project_priority",
            "project_priority_name",
            "uuid",
            "group_list",
        ]

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
            # fields.pop("group_list", None)
            fields.pop("organisation_id", None)

        return fields
