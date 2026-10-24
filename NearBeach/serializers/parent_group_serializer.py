from rest_framework import serializers
from NearBeach.models.user import Group


class ParentGroupSerializer(serializers.ModelSerializer):
    """Class containing serializer for Parent Groups"""
    # Name
    # Parent Group
    id = serializers.IntegerField(source='pk', read_only=True)
    name = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
        ]
