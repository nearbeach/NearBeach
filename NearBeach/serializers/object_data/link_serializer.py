from rest_framework import serializers



RELATION_DICT = {
    "relates": "Relate",
    "blocked_by": "Block",
    "blocking": "Block",
    "sub_object_of": "Subobject",
    "parent_object_of": "Subobject",
    "has_duplicate": "Duplicate",
    "duplicate_object": "Duplicate",
}


class LinkSerializer(serializers.Serializer):
    link_relationship = serializers.CharField(
        read_only=True,
    )
    object_assignment_id = serializers.IntegerField(
        read_only=True,
    )
    object_id = serializers.IntegerField(
        required=True,
    )
    object_title = serializers.CharField(
        read_only=True,
    )
    object_status = serializers.CharField(
        read_only=True,
    )
    object_type = serializers.CharField(
        required=True,
    )
    parent_link = serializers.CharField(
        read_only=True,
    )
    reverse_relation = serializers.BooleanField(
        read_only=True,
    )

    def create(self, validated_data):
        raise NotImplementedError()

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # If creating a new link, we'll need the object relation
        if self.context["request"].method == "POST":
            fields["object_relation"] = serializers.ChoiceField(
                required=True,
                choices=RELATION_DICT,
            )


        return fields

    def update(self, instance, validated_data):
        raise NotImplementedError()

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
