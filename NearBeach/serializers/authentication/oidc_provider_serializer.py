from rest_framework import serializers


class OidcProviderSerializer(serializers.Serializer):
    """The public details of a provider - just enough to draw a login button"""

    name = serializers.CharField()
    slug = serializers.SlugField()
    login_url = serializers.CharField()
