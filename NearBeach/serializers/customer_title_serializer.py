from rest_framework import serializers
from NearBeach.models import ListOfTitle


class CustomerTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfTitle
        fields = [
            "title_id",
            "title",
        ]