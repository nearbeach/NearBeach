from rest_framework import serializers
from NearBeach.models import (
    Organisation,
)
from NearBeach.serializers.customer_serializer import CustomerSerializer
from django.conf import settings


class OrganisationSerializer(serializers.ModelSerializer):
    customers = CustomerSerializer(
        many=True,
        allow_null=True,
        read_only=True,
    )
    organisation_id = serializers.ReadOnlyField()
    organisation_name = serializers.CharField(
        required=True,
    )
    organisation_website = serializers.URLField(
        required=True,
    )
    organisation_email = serializers.EmailField(
        required=True,
    )
    organisation_profile_picture_path = serializers.SerializerMethodField()

    def get_organisation_profile_picture_path(self, obj):
        if obj.organisation_profile_picture is None:
            return None

        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return private_media_url + str(obj.organisation_profile_picture_id)

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating an organisation
        if self.context["request"].method == "PUT":
            fields.pop("organisation_profile_picture_path", None)

        if self.context["request"].method == "POST":
            fields.pop("organisation_profile_picture_path", None)

        return fields

    class Meta:
        model = Organisation
        fields = [
            "organisation_id",
            "organisation_name",
            "organisation_website",
            "organisation_email",
            "organisation_profile_picture_path",
            "customers",
        ]

