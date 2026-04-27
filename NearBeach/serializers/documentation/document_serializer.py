from rest_framework import serializers
from NearBeach.models import Document
from NearBeach.serializers.documentation.folder_serializer import FolderSerializer


class DocumentSerializer(serializers.Serializer):
    """Class for document serialization"""
    key = serializers.UUIDField(
        read_only=True,
    )
    description = serializers.CharField(
        required=True,
    )
    url_location = serializers.CharField(
        read_only=True,
    )
    folder = FolderSerializer()
