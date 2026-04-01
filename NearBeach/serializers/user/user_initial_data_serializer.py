from NearBeach.serializers.object_data.status.object_status_serializer import ObjectStatusSerializer
from NearBeach.serializers.object_data.types.object_types_serializer import ObjectTypesSerializer
from NearBeach.serializers.object_data.tags_serializer import TagsSerializer
from NearBeach.serializers.user.permissions_serializer import PermissionSerializer
from NearBeach.serializers.user.user_serializer import UserSerializer


class UserInitialDataSerializer(UserSerializer):
    """Class containing user initial data serialization."""
    permissions = PermissionSerializer(
        many=True,
        read_only=True,
        allow_null=True,
    )

    object_status = ObjectStatusSerializer(
        read_only=True,
        allow_null=True,
    )

    object_types = ObjectTypesSerializer(
        read_only=True,
        allow_null=True,
    )

    tags = TagsSerializer(
        many=True,
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + [
            'permissions',
            'object_status',
            'object_types',
            'tags',
        ]
