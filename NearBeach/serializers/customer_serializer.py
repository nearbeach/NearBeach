from rest_framework import serializers
from NearBeach.models import (
    Customer,
    ListOfTitle, Organisation,
)
from NearBeach.serializers.customer_title_serializer import CustomerTitleSerializer
from django.conf import settings


class CustomerSerializer(serializers.ModelSerializer):
    customer_id = serializers.ReadOnlyField()
    customer_title = CustomerTitleSerializer(
        many=False,
        read_only=False,
        allow_null=False,
    )
    customer_first_name = serializers.CharField(
        required=True,
    )
    customer_last_name = serializers.CharField(
        required=True,
    )
    customer_email = serializers.EmailField(
        required=True,
    )
    customer_profile_picture_path = serializers.SerializerMethodField()

    @staticmethod
    def get_customer_profile_picture_path(obj):
        if obj.customer_profile_picture_id is None:
            return None

        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return F"{private_media_url}{obj.customer_profile_picture_id}"

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        if self.context["request"].method in ("POST", "PUT"):
            fields.pop("customer_profile_picture_path", None)
            fields["customer_title"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfTitle.objects.filter(
                    is_deleted=False,
                ),
            )

        return fields

    def update(self, instance, validated_data):
        # Update title
        instance.customer_title_id = validated_data.pop("customer_title")

        # Update instance
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "customer_title",
            "customer_first_name",
            "customer_last_name",
            "customer_email",
            "customer_profile_picture_path",
        ]

