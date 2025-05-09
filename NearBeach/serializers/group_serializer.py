from rest_framework import serializers
from NearBeach.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = [
            "change_user",
            "date_created",
            "date_modified",
            "is_deleted",
        ]
