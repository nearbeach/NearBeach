from rest_framework import serializers
from NearBeach.models import (
    Organisation,
)
from NearBeach.serializers.customer_serializer import CustomerSerializer


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
    organisation_profile_picture = serializers.ReadOnlyField(
        source="organisationprofilepicture__document_id__document_key"
    )

    class Meta:
        model = Organisation
        exclude = [
            "organiation_profile_picture",
            "date_created",
            "date_modified",
            "change_user",
            "is_deleted",
        ]