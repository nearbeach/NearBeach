from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.abstraction.date_fields_serializer import DateFieldsSerializer
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.serializers.project_status_serializer import ProjectStatusSerializer

from NearBeach.utils.enums.object_enums import ObjectPriority


class ProjectSerializer(BaseObjectSerializer, DateFieldsSerializer):
    """Class containing serializer base for all objects"""

    organisation = OrganisationSerializer(
        many=False,
        read_only=True,
    )
    project_priority = EnumField(enum=ObjectPriority)
    project_status = ProjectStatusSerializer(
        many=False,
        read_only=False,
        allow_null=False,
    )

    def create(self, validated_data):
        # Pop out the fields we dont need
        group_list = validated_data.pop("group_list", [])

        # Extract data we need
        validated_data["project_status"] = ListOfProjectStatus.objects.filter(
            is_deleted=False
        ).order_by(
            "project_status_sort_order",
        ).first()

        # Create the project
        project = Project.objects.create(**validated_data)

        # Create the group list
        for single_group in group_list:
            # Save the group against the new project
            submit_object_assignment = ObjectAssignment(
                group_id=single_group,
                project=project,
                change_user=validated_data["change_user"],
            )
            submit_object_assignment.save()

        return project

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Creating a new project
        if self.context["request"].method == "POST":
            fields.pop("project_status", None)
            fields.pop("project_priority", None)
            fields["organisation"] = serializers.PrimaryKeyRelatedField(
                queryset=Organisation.objects.filter(is_deleted=False)
            )

        # Updating a new project
        if self.context['request'].method == "PUT":
            fields.pop("group_list", None)
            fields.pop("organisation", None)
            fields["project_status"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfProjectStatus.objects.filter(
                    is_deleted=False,
                )
            )

        return fields

    def update(self, instance, validated_data):
        # Project Status
        project_status_id = validated_data.pop("project_status", 0)
        instance.project_status_id = project_status_id

        # Priority
        project_priority = validated_data.pop("project_priority", 2)
        instance.project_priority = project_priority["value"]

        # Update instance
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Project
        fields = [
            "project_id",
            "project_name",
            "project_description",
            "organisation",
            "project_status",
            "project_higher_order_status",
            "project_priority",
            "project_story_point",
            "project_start_date",
            "project_end_date",
            "group_list",
            "date_created",
            "date_modified",
            "uuid",
        ]


