from rest_framework import serializers
from NearBeach.serializers.destination_serializer import DestinationSerializer
from NearBeach.models import Tag

class TagSerializer(DestinationSerializer):
    tag_assignment_id = serializers.IntegerField(
        read_only=True,
    )
    tag_id = serializers.IntegerField(
        read_only=True,
    )
    tag_list = serializers.PrimaryKeyRelatedField(
        required=False,
        many=True,
        queryset=Tag.objects.all(),
    )
    tag_name = serializers.CharField(
        read_only=True,
    )
    tag_colour = serializers.CharField(
        read_only=True,
    )
    tag_text_colour = serializers.CharField(
        read_only=True,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            # When there is no context, we don't want these fields to be required
            fields["destination"].required = False
            fields["location_id"].required = False
            return fields

        if self.context["request"].method == "POST":
            fields["tag_list"].required = True

        return fields
