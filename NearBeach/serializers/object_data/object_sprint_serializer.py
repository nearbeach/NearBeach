from rest_framework import serializers
from NearBeach.serializers.destination_serializer import DestinationSerializer


class ObjectSprintSerializer(DestinationSerializer):
     sprint_id = serializers.IntegerField(
         read_only=True,
     )
     sprint_name = serializers.CharField(
         # read_only=True,
     )
     total_story_points = serializers.IntegerField(
         read_only=True,
         required=False,
     )
     completed_story_points = serializers.IntegerField(
         read_only=True,
         required=False,
     )
     sprint_status = serializers.CharField(
         read_only=True,
     )
     sprint_start_date = serializers.DateTimeField(
         # read_only=True,
     )
     sprint_end_date = serializers.DateTimeField(
         # read_only=True,
     )

     def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            # When there is no context, we don't want these fields to be required
            fields["destination"].required = False
            fields["location_id"].required = False
            return fields

        if self.context["request"].method == "GET":
            fields["sprint_name"].required = False
            fields["sprint_start_date"].required = False
            fields["sprint_end_date"].required = False

        return fields
