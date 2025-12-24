from rest_framework import serializers
from NearBeach.models.models import ListOfProjectStatus


class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfProjectStatus
        fields = [
            "project_status_id",
            "project_status",
        ]