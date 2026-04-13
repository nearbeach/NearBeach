from rest_framework import serializers
from NearBeach.models import ListOfProjectStatus
from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.abstraction.date_fields_serializer import DateFieldsSerializer
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.serializers.object_data.status.project_status_serializer import ProjectStatusSerializer
from NearBeach.utils.enums.object_enums import ObjectPriority
from NearBeach.models.project import Project
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment


class ProjectSerializer(serializers.ModelSerializer, BaseObjectSerializer, DateFieldsSerializer):
    """Class containing serializer base for all objects"""

    organisation = OrganisationSerializer(
        many=False,
        read_only=True,
    )
    priority = EnumField(
        enum=ObjectPriority,
        required=False,
    )
    status = ProjectStatusSerializer(
        many=False,
        read_only=False,
        allow_null=False,
        required=False,
    )

    def create(self, validated_data):
        """Method for creating a project"""
        group_list = validated_data.pop("group_list", [])

        # Extract data we need
        validated_data["status"] = ListOfProjectStatus.objects.filter(
            is_deleted=False
        ).order_by(
            "sort_order",
        ).first()

        # Create the project
        project = Project.objects.create(**validated_data)

        # Create the group list
        for single_group in group_list:
            # Save the group against the new project
            submit_object_assignment = ObjectAssignment(
                group=single_group,
                project=project,
                change_user=validated_data["change_user"],
            )
            submit_object_assignment.save()

        return project

    def get_fields(self):
        fields = super().get_fields()

        # PATCH
        method = self.context.get("method", None)
        if method == "PATCH":
            fields.pop("group_list", None)
            fields.pop("organisation", None)
            fields["status"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfProjectStatus.objects.filter(
                    is_deleted=False,
                ),
            )

        return fields

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "organisation",
            "status",
            "priority",
            "story_point",
            "start_date",
            "end_date",
            "group_list",
            "user_list",
            "date_created",
            "date_modified",
        ]
