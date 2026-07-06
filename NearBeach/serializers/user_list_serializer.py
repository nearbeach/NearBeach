from rest_framework import serializers
from django.contrib.auth.models import User


class UserListSerializer(serializers.Serializer):
    """Class containing serializer for adding/removing users to objects"""
    user_list = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        queryset=User.objects.filter(
            is_active=True,
        ),
    )
