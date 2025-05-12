from rest_framework import serializers
from NearBeach.models import Group, User
from NearBeach.serializers.group_serializer import GroupSerializer
from NearBeach.serializers.user_serializer import UserSerializer
from NearBeach.serializers.object_data.object_assignment_group_serializer import ObjectAssignmentGroupSerializer
from NearBeach.serializers.object_data.object_assignment_user_serializer import ObjectAssignmentUserSerializer


class GroupAndUserSerializer(serializers.Serializer):
    # Serialise Data
    group_list = serializers.PrimaryKeyRelatedField(
        required=False,
        many=True,
        queryset=Group.objects.filter(
            is_deleted=False,
        ),
    )
    object_assignment = serializers.ReadOnlyField()
    object_group_list = ObjectAssignmentGroupSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    object_user_list = ObjectAssignmentUserSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    potential_group_list = GroupSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    potential_user_list = UserSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    user_group_list = GroupSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    user_list = serializers.PrimaryKeyRelatedField(
        required=False,
        many=True,
        queryset=User.objects.filter(
            is_active=True,
        )
    )
