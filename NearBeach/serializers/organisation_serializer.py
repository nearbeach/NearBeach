from rest_framework import serializers
from NearBeach.models import (
    Organisation,
)
from NearBeach.serializers.customer_serializer import CustomerSerializer
from django.conf import settings


class OrganisationSerializer(serializers.ModelSerializer):
    """Class containing serializer for Organisation"""
    customers = CustomerSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    email = serializers.EmailField(
        required=True,
    )
    id = serializers.ReadOnlyField()
    name = serializers.CharField(
        required=True,
    )
    website = serializers.URLField(
        required=True,
    )
    profile_picture_path = serializers.SerializerMethodField()

    @staticmethod
    def get_profile_picture_path(obj):
        if obj.profile_picture is None:
            return None

        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return private_media_url + str(obj.profile_picture_id)

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating an organisation
        if self.context["request"].method == "PUT":
            fields.pop("profile_picture_path", None)

        if self.context["request"].method == "POST":
            fields.pop("profile_picture_path", None)

        return fields

    class Meta:
        model = Organisation
        fields = [
            "id",
            "name",
            "website",
            "email",
            "profile_picture_path",
            "customers",
        ]
