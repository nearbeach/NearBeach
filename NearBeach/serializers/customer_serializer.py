from rest_framework import serializers
from NearBeach.models import (
    Customer,
    ListOfTitle,
    Organisation,
)


class CustomerSerializer(serializers.ModelSerializer):
    customer_id = serializers.ReadOnlyField()
    customer_title = serializers.PrimaryKeyRelatedField(
        queryset=ListOfTitle.objects.filter(
            is_deleted=False,
        ),
        required=True,
    )
    customer_title_name = serializers.ReadOnlyField(
        source="title_name.title_name",
    )
    customer_first_name = serializers.CharField(
        required=True,
    )
    customer_last_name = serializers.CharField(
        required=True,
    )
    customer_email = serializers.CharField(
        required=True,
    )
    customer_profile_picture = serializers.ReadOnlyField(
        source='userprofilepicture__document_id__document_key'
    )
    organisation = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.filter(
            is_deleted=False,
        ),
        required=True,
    )
    organisation_name = serializers.ReadOnlyField(
        source="organisation.organisation_name",
    )

    class Meta:
        model = Customer
        exclude = [
            "customer_profile_picture",
            "date_created",
            "date_modified",
            "change_user",
            "is_deleted",
        ]

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating an organisation
        if self.context["request"].method == "PUT":
            fields.pop("organisation", None)
