from rest_framework import serializers


class PotentialObjectLinkSerializer(serializers.Serializer):
    """An object that can be linked to - just enough to identify it"""
    object_id = serializers.IntegerField(read_only=True)
    object_title = serializers.CharField(read_only=True)
    object_type = serializers.CharField(read_only=True)
