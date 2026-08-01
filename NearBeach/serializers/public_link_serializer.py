from rest_framework import serializers
from NearBeach.models import PublicLink


class PublicLinkSerializer(serializers.ModelSerializer):
    """Class for serializing the model PublicLink"""

    class Meta:
        model = PublicLink
        fields = [
            "id",
            "is_active",
        ]