from rest_framework import serializers
from serializers.organisation_serializer import OrganisationSerializer


class PublicLinkDataSerializer(serializers.Serializer):
    """Class containing serializer for public link data"""
    object_type = serializers.CharField(
        required=True,
    )
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    organisation = OrganisationSerializer(
        many=False,
        read_only=True,
        allow_null=True,
    )
    status = serializers.CharField()
    priority = serializers.SerializerMethodField()
    story_point = serializers.IntegerField()

    @staticmethod
    def get_priority(obj):
        return obj.get_priority_display()
