"""drf-spectacular extensions for NearBeach's custom serializer fields."""
from drf_spectacular.contrib.django_oauth_toolkit import DjangoOAuthToolkitScheme
from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import build_basic_type
from drf_spectacular.types import OpenApiTypes


class EnumFieldExtension(OpenApiSerializerFieldExtension):
    """EnumField is represented as {"value": ..., "label": ...} (and accepts that, or the bare value, on input)"""

    target_class = "NearBeach.serializers.enum_serializer.EnumField"

    def map_serializer_field(self, auto_schema, direction):
        first = next(iter(self.target.enum))
        value_type = OpenApiTypes.INT if isinstance(first.value, int) else OpenApiTypes.STR

        return {
            "type": "object",
            "properties": {
                "value": {**(build_basic_type(value_type) or {}), "enum": [member.value for member in self.target.enum]},
                "label": build_basic_type(OpenApiTypes.STR),
            },
            "required": ["value", "label"],
        }


class NearBeachOAuth2Scheme(DjangoOAuthToolkitScheme):
    """Documents NearBeach's bearer token authentication as the same `oauth2` scheme django-oauth-toolkit uses"""

    target_class = "NearBeach.utils.oauth2.authentication.NearBeachOAuth2Authentication"
    priority = 1

    def get_security_requirement(self, auto_schema):
        # Scopes are enforced globally (read/write by HTTP method) rather than per view
        return {self.name: []}
