from rest_framework import serializers
from NearBeach.models import Sprint


class ObjectSprintSerializer(serializers.ModelSerializer):
    completed_story_points = serializers.IntegerField(
        read_only=True,
        required=False,
    )
    sprint_end_date = serializers.DateTimeField()
    sprint_id = serializers.IntegerField(
         read_only=True,
    )
    sprint_name = serializers.CharField(
         # read_only=True,
    )
    sprint_start_date = serializers.DateTimeField()
    sprint_status = serializers.CharField(
        read_only=True,
    )
    total_story_points = serializers.IntegerField(
         read_only=True,
         required=False,
    )

    def create(self, validated_data):
        destination = validated_data.pop("destination")
        location_id = validated_data.pop("location_id")

        validated_data[F"{destination}_id"] = location_id

        sprint = Sprint.objects.create(**validated_data)

        return sprint


    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        if self.context["request"].method == "GET":
            fields["sprint_name"].required = False
            fields["sprint_start_date"].required = False
            fields["sprint_end_date"].required = False

        return fields

    class Meta:
         model = Sprint
         fields = [
             "sprint_id",
             "sprint_name",
             "total_story_points",
             "completed_story_points",
             "sprint_status",
             "sprint_start_date",
             "sprint_end_date",
         ]
