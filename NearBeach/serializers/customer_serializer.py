from rest_framework import serializers
from NearBeach.models import (
    Customer,
    ListOfTitle,
    Organisation,
)
from django.conf import settings


class CustomerSerializer(serializers.ModelSerializer):
    customer_id = serializers.ReadOnlyField()
    customer_title = serializers.PrimaryKeyRelatedField(
        queryset=ListOfTitle.objects.filter(
            is_deleted=False,
        ),
        required=True,
    )
    customer_title_name = serializers.ReadOnlyField(
        source="customer_title.title",
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
    customer_profile_picture = serializers.ImageField(
        read_only=True,
    )
    customer_profile_picture_path = serializers.SerializerMethodField()
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
            "date_created",
            "date_modified",
            "change_user",
            "is_deleted",
        ]
    
    def get_customer_profile_picture_path(self, obj):
        if obj.customer_profile_picture_id is None:
            return None

        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return private_media_url + str(obj.customer_profile_picture_id)

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating an organisation
        if self.context["request"].method == "PUT":
            fields.pop("organisation", None)
            fields.pop("customer_profile_picture_path", None)

        if self.context["request"].method == "POST":
            fields.pop("customer_profile_picture_path", None)

        return fields
