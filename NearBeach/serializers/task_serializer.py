from rest_framework import serializers
from NearBeach.models.task import ListOfTaskStatus, Task
from NearBeach.serializers.abstraction.meta_data_serializer_mixin import MetaDataSerializerMixin
from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.abstraction.date_fields_serializer import DateFieldsSerializer
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.group_serializer import GroupSerializer
from NearBeach.serializers.organisation_serializer import OrganisationSerializer
from NearBeach.serializers.object_data.status.task_status_serializer import TaskStatusSerializer
from NearBeach.serializers.user.user_serializer import UserSerializer
from NearBeach.utils.enums.object_enums import ObjectPriority
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment


class TaskSerializer(MetaDataSerializerMixin, serializers.ModelSerializer, BaseObjectSerializer, DateFieldsSerializer):
    """Class containing serializer base for all objects"""

    organisation = OrganisationSerializer(
        many=False,
        read_only=True,
        allow_null=True,
    )
    priority = EnumField(
        enum=ObjectPriority,
        required=False,
    )
    status = TaskStatusSerializer(
        many=False,
        read_only=False,
        allow_null=False,
        required=False,
    )

    def create(self, validated_data):
        """Method for creating a task"""
        group_list = validated_data.pop("group_list", [])

        # Extract data we need
        validated_data["status"] = ListOfTaskStatus.objects.filter(
            is_deleted=False
        ).order_by(
            "sort_order",
        ).first()

        # Create the task
        task = Task.objects.create(**validated_data)

        # Create the group list
        for single_group in group_list:
            # Save the group against the new task
            submit_object_assignment = ObjectAssignment(
                group=single_group,
                task=task,
                change_user=validated_data["change_user"],
                creation_user=validated_data["creation_user"],
            )
            submit_object_assignment.save()

        return task

    def get_fields(self):
        fields = super().get_fields()

        # PATCH
        method = self.context.get("method", None)
        if method == "PATCH":
            fields.pop("group_list", None)
            fields.pop("organisation", None)
            fields["status"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfTaskStatus.objects.filter(
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
        model = Task
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
            "meta_data",
        ]


class TaskDetailSerializer(TaskSerializer):
    """The shape of a single task (GET): groups are readable here and the users are included.

    Exists so the API documentation can describe retrieve accurately; the endpoint itself passes
    `context={"method": "GET"}` to TaskSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "GET"}

        return super().get_fields()


class TaskPatchSerializer(TaskSerializer):
    """The PATCH shape of a task - request and response (no groups, organisation or users; status is an id).

    Exists so the API documentation can describe PATCH accurately; the endpoint itself passes
    `context={"method": "PATCH"}` to TaskSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "PATCH"}
        fields = super().get_fields()

        # Read-only, and only ever filled in by a GET of a single task
        fields.pop("user_list", None)

        return fields
