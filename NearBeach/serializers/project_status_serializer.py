from rest_framework import serializers
from NearBeach.models import ListOfProjectStatus


class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfProjectStatus
        fields = [
            "id",
            "status",
        ]
