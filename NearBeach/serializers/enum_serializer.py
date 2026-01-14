from rest_framework import serializers


class EnumField(serializers.ChoiceField):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        choices = [(member.value, member.label) for member in enum]
        super().__init__(choices=choices, **kwargs)

    def to_representation(self, value):
        if isinstance(value, self.enum):
            enum_member = value
        else:
            enum_member = self.enum(value)
        return {
            "value": enum_member.value,
            "label": enum_member.label
        }

    def to_internal_value(self, data):
        # If the client sends {"value": 1}, extract the value
        if isinstance(data, dict):
            data = data.get("value")
        return super().to_internal_value(data)
