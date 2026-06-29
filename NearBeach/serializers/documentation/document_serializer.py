from rest_framework import serializers
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
        required=False,
    )
    folder = FolderSerializer(
        required=False,
    )
    document = serializers.FileField(
        required=False,
    )
    parent_folder_id = serializers.IntegerField(
        required=False,
    )
    type = serializers.ChoiceField(
        write_only=True,
        choices=[
            'document',
            'folder',
            'link'
        ]
    )