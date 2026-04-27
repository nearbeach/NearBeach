from rest_framework import serializers

from NearBeach.serializers.documentation.document_serializer import DocumentSerializer
from NearBeach.serializers.documentation.folder_serializer import FolderSerializer


class FileSystemSerializer(serializers.Serializer):
    """Class containing serializer details for a file system"""
    documents = DocumentSerializer(
        many=True,
        read_only=True,
    )
    folders = FolderSerializer(
        many=True,
        read_only=True,
    )
    max_upload_size = serializers.IntegerField(
        read_only=True,
    )
