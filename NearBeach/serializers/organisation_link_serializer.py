from rest_framework import serializers
from NearBeach.models import (
    Organisation,
)
from NearBeach.serializers.customer_serializer import CustomerSerializer
from NearBeach.serializers.organisation_serializer import OrganisationSerializer


class OrganisationLinkSerializer(serializers.ModelSerializer):
    """Class containing serializer for Organisation links"""
    customers = CustomerSerializer(
        allow_null=True,
        many=True,
        read_only=True,
    )

    id = serializers.IntegerField(
        write_only=True,
        required=True,
    )

    organisation = OrganisationSerializer(
        read_only=True,
        allow_null=True,
    )

    potential_customers = CustomerSerializer(
        allow_null=True,
        many=True,
        read_only=True,
    )

    potential_organisations = OrganisationSerializer(
        read_only=True,
        many=True,
        allow_null=True,
    )

    class Meta:
        model = Organisation
        fields = [
            "id",
            "customers",
            "organisation",
            "potential_customers",
            "potential_organisations",
        ]
