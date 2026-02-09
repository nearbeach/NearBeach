from NearBeach.models import ListOfProjectStatus
from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.abstraction.date_fields_serializer import DateFieldsSerializer
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.serializers.project_status_serializer import ProjectStatusSerializer
from NearBeach.utils.enums.object_enums import ObjectPriority
from NearBeach.models.project import Project
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.utils.enums.status_enums import ObjectHigherOrderStatus


class ProjectSerializer(BaseObjectSerializer, DateFieldsSerializer):
    """Class containing serializer base for all objects"""

    higher_order_status = EnumField(enum=ObjectHigherOrderStatus)
    organisation = OrganisationSerializer(
        many=False,
        read_only=True,
    )
    priority = EnumField(enum=ObjectPriority)
    status = ProjectStatusSerializer(
        many=False,
        read_only=False,
        allow_null=False,
    )

    def create(self, validated_data):
        """Method for creating a project"""
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

        # PATCH
        if self.context['request'].method == "PATCH":
            fields.pop("group_list", None)
            fields.pop("organisation", None)

        return fields

    # def update(self, instance, validated_data):
    #     # Project Status
    #     project_status_id = validated_data.pop("project_status", 0)
    #     instance.project_status_id = project_status_id
    #
    #     # Priority
    #     project_priority = validated_data.pop("project_priority", 2)
    #     instance.project_priority = project_priority["value"]
    #
    #     # Update instance
    #     instance = super().update(instance, validated_data)
    #     return instance

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "organisation",
            "status",
            "higher_order_status",
            "priority",
            "story_point",
            "start_date",
            "end_date",
            "group_list",
            "date_created",
            "date_modified",
        ]


