from rest_framework import serializers


class NoteSerializer(serializers.Serializer):
    can_edit = serializers.BooleanField(
        read_only=True,
    )
    date_modified = serializers.DateTimeField(
        read_only=True,
    )
    first_name = serializers.CharField(
        read_only=True,
    )
    last_name = serializers.CharField(
        read_only=True,
    )
    object_note_id = serializers.IntegerField(
        read_only=True,
    )
    object_note = serializers.CharField()
    profile_picture = serializers.CharField(
        read_only=True,
        required=False,
    )
    username = serializers.IntegerField(
        read_only=True,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        if self.context["request"].method == "GET":
            fields["object_note"].required = False

        if self.context["request"].method == "DELETE":
            fields["object_note"].required = False

        return fields
