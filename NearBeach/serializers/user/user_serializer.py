from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Class to serialize a user"""
    full_name = serializers.SerializerMethodField()

    # Querysets annotate this with the key of the picture's document (None when there is no picture)
    profile_picture = serializers.UUIDField(
        read_only=True,
        allow_null=True,
    )

    profile_picture_path = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(obj) -> str:
        # Some querysets annotate full_name already (GroupService) - otherwise build it the same way
        annotated = getattr(obj, "full_name", None)
        if annotated is not None:
            return annotated

        return f"{obj.first_name} {obj.last_name}"

    @staticmethod
    def get_profile_picture_path(obj) -> str | None:
        picture_key = getattr(obj, "profile_picture", None)
        if picture_key is None:
            return None

        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return F"{private_media_url}{picture_key}"

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "profile_picture",
            "profile_picture_path",
        ]
