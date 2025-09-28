from rest_framework import serializers
from NearBeach.decorators.check_destination import OBJECT_ARRAY


class DestinationSerializer(serializers.Serializer):
    destination = serializers.ChoiceField(
        required=True,
        choices=OBJECT_ARRAY,
    )
    location_id = serializers.IntegerField(
        required=True,
    )

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
