from rest_framework import serializers
from django.conf import settings
from NearBeach.models import ObjectAssignment


class ObjectAssignmentUserSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(
        source='assigned_user.email',
    )
    first_name = serializers.ReadOnlyField(
        source='assigned_user.first_name',
    )
    last_name = serializers.ReadOnlyField(
        source='assigned_user.last_name',
    )
    profile_picture = serializers.ImageField(
        read_only=True,
    )
    profile_picture_path = serializers.SerializerMethodField()
    user_id = serializers.ReadOnlyField(
        source='assigned_user_id',
    )
    username = serializers.ReadOnlyField(
        source='assigned_user.username',
    )

    class Meta:
        model = ObjectAssignment
        fields = [
            "assigned_user",
            "email",
            "first_name",
            "last_name",
            "object_assignment_id",
            "profile_picture",
            "profile_picture_path",
            "user_id",
            "username",
        ]

    def get_profile_picture_path(self, obj):
        if obj.profile_picture is None:
            return None

        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return private_media_url + str(obj.profile_picture_id)
