from rest_framework import serializers
from NearBeach.models import ExtendsAuthToken, User
# from django.contrib.auth.models import User
import datetime


class UserApiSerializer(serializers.ModelSerializer):
    api_key = serializers.SerializerMethodField(
        read_only=True,
    )
    pk = serializers.ReadOnlyField()

    class Meta:
        model = ExtendsAuthToken
        fields = [
            "pk",
            "api_key",
            "description",
            "expiry",
        ]

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Add expires_in field when  creating
        if self.context["request"].method == "POST":
            fields["expires_in"] = serializers.IntegerField(
                required=False,
            )

        return fields

    def get_api_key(self, field):
        # Check to make sure the request context exists
        if "request" not in self.context:
            return field.api_key

        # If the user creates a new token, we want to return the token in full
        if self.context["request"].method == "POST":
            return field.api_key

        # Replace the characters after the 4th character with '*'
        return field.api_key[0:4] + "*" * (len(field.api_key) - 4)

    def create(self, validated_data):
        user_id = validated_data.pop("user")
        expires_in = validated_data.pop("expires_in", None)

        # Modify the validated data
        validated_data["user"] = User.objects.get(pk=user_id)
        if expires_in is not None:
            validated_data["expiry"] = datetime.timedelta(days=expires_in)


        # Create the token
        created_token = ExtendsAuthToken.objects.create(**validated_data)

        # Fetch the object
        extend_auth_token = ExtendsAuthToken.objects.get(pk=created_token[0])
        extend_auth_token.api_key = created_token[1]
        extend_auth_token.expires_in = expires_in

        return extend_auth_token
