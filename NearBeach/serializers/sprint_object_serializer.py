from rest_framework import serializers


class SprintObjectSerializer(serializers.Serializer):
    description = serializers.CharField(
        read_only=True,
        allow_null=True,
    )
    end_date = serializers.DateTimeField(
        read_only=True,
        allow_null=True,
    )
    higher_order_status = serializers.CharField(
        read_only=True,
        max_length=10,
        allow_null=True,
    )
    object_id = serializers.IntegerField(
        required=True,
        allow_null=True,
    )
    object_type = serializers.ChoiceField(
        required=True,
        allow_null=True,
        choices=["requirement_item", "project", "task"]
    )
    parent_object_type = serializers.CharField(
        read_only=True,
        allow_null=True,
    )
    parent_object_id = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    sprint_object_assignment_id = serializers.IntegerField(
        read_only=True,
    )
    start_date = serializers.DateTimeField(
        read_only=True,
        allow_null=True,
    )
    status_id = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    title = serializers.CharField(
        max_length=255,
        read_only=True,
        allow_null=True,
    )
    
    def create(self, validated_data):
        raise NotImplementedError()

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Creating a new link
        if self.context["request"].method == "POST":
            fields["object_id"] = serializers.ListField(
                child=serializers.IntegerField(min_value=1),
                required=True,
            )

        return fields

    def update(self, instance, validated_data):
        raise NotImplementedError()
