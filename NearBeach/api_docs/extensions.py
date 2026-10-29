"""drf-spectacular extensions for NearBeach's custom serializer fields."""
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
