from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
        read_only=True,
    )
    profile_picture_path = serializers.SerializerMethodField()

    @staticmethod
    def get_profile_picture_path(obj):
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
            "email",
            "profile_picture",
            "profile_picture_path",
        ]
