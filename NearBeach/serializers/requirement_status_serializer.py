from rest_framework import serializers
from NearBeach.models import ListOfRequirementStatus


class RequirementStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfRequirementStatus
        fields = [
            "requirement_status_id",
            "requirement_status",
        ]
        