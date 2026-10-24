from rest_framework import serializers
from NearBeach.models.misc.note import ObjectNote


class NoteSerializer(serializers.ModelSerializer):
    """Serializer class for notes"""
    can_edit = serializers.BooleanField(
        read_only=True,
    )
    date_modified = serializers.DateTimeField(
        read_only=True,
    )
    first_name = serializers.CharField(
        read_only=True,
    )
    id = serializers.IntegerField(
        read_only=True,
    )
    last_name = serializers.CharField(
        read_only=True,
    )
    note = serializers.CharField()
    profile_picture = serializers.CharField(
        read_only=True,
        required=False,
        allow_null=True,
    )
    username = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = ObjectNote
        fields = [
            "id",
            "note",
            "first_name",
            "last_name",
            "username",
            "profile_picture",
            "date_modified",
            "can_edit",
        ]
