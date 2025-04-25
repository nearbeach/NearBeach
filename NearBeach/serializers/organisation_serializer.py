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
    organisation_website = serializers.CharField(
        required=True,
    )
    organisation_email = serializers.CharField(
        required=True,
    )
    organisation_profile_picture_path = serializers.SerializerMethodField()

    class Meta:
        model = Organisation
        exclude = [
            "organiation_profile_picture",
            "date_created",
            "date_modified",
            "change_user",
            "is_deleted",
        ]

    def get_organisation_profile_picture_path(self, obj):
        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return private_media_url + str(obj.organisation_profile_picture_id)
