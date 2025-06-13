from rest_framework import serializers
from NearBeach.models import (
    ChangeTask,
    Project,
    Requirement,
    RequirementItem,
    Task,
)


class LinkSerializer(serializers.Serializer):
    link_relationship = serializers.CharField(
        read_only=True,
    )
    object_assignment_id = serializers.IntegerField(
        read_only=True,
    )
    object_id = serializers.IntegerField(
        read_only=True,
    )
    object_title = serializers.CharField(
        read_only=True,
    )
    object_status = serializers.CharField(
        read_only=True,
    )
    object_type = serializers.CharField(
        read_only=True,
    )
    parent_link = serializers.CharField(
        read_only=True,
    )
    reverse_relation = serializers.BooleanField(
        read_only=True,
    )
    object_relation = serializers.CharField( #CHANGTO ENUM
        required=False,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # If creating a new link, we'll need the object relation
        if self.context["request"].method == "POST":
            fields["object_relation"].required = True

        return fields

    class Meta(object):
        fields = (
            "object_assignment_id",
            "object_type",
            "object_id",
            "object_title",
            "object_status",
            "parent_link",
            "link_relationship",
            "reverse_relation",
        )
