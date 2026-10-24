from rest_framework import serializers
from django.contrib.auth.models import User


class UserListSerializer(serializers.Serializer):
    """Class containing serializer for adding/removing users to objects"""
    user_list = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        allow_empty=False,  # a form post with no user_list at all arrives as an empty list
        queryset=User.objects.filter(
            is_active=True,
        ),
    )
