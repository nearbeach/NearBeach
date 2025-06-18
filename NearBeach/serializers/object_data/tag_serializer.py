from rest_framework import serializers
from NearBeach.models import Tag


class TagSerializer(serializers.ModelSerializer):
    tag_id = serializers.IntegerField(
        read_only=True,
    )
    tag_assignment_id = serializers.IntegerField(
        read_only=True,
    )
    tag_colour = serializers.CharField(
        read_only=True,
    )
    tag_list = serializers.PrimaryKeyRelatedField(
        required=False,
        many=True,
        queryset=Tag.objects.all(),
    )
    tag_name = serializers.CharField(
        read_only=True,
    )
    tag_text_colour = serializers.CharField(
        read_only=True,
    )

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        if self.context["request"].method == "POST":
            fields["tag_list"].required = True

        return fields

    class Meta:
        model = Tag
        fields = [
            "tag_assignment_id",
            "tag_id",
            "tag_name",
            "tag_list",
            "tag_colour",
            "tag_text_colour",
        ]