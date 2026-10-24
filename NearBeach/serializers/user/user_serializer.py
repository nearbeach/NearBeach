from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Class to serialize a user"""
    full_name = serializers.SerializerMethodField()

    profile_picture = serializers.ImageField(
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
        if obj.profile_picture is None:
            return None

        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return F"{private_media_url}{obj.profile_picture_id}"

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
