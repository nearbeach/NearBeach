from rest_framework import serializers
from NearBeach.models import Organisation
from django.conf import settings


class OrganisationListSerializer(serializers.ModelSerializer):
    organisation_profile_picture_path = serializers.SerializerMethodField()

    @staticmethod
    def get_organisation_profile_picture_path(obj):
        if obj.organisation_profile_picture is None:
            return None

        private_media_url = getattr(settings, "PRIVATE_MEDIA_URL", False)

        return private_media_url + str(obj.organisation_profile_picture_id)

    class Meta:
        model = Organisation
        fields = [
            "organisation_id",
            "organisation_name",
            "organisation_website",
            "organisation_email",
            "organisation_profile_picture_path",
        ]