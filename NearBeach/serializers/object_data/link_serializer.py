from rest_framework import serializers

from NearBeach.utils.dicts.relation_dict import RELATION_DICT


class LinkSerializer(serializers.Serializer):
    """Close for serializing Link objects."""
    object_assignment_id = serializers.IntegerField(
        read_only=True,
    )
    object_id = serializers.IntegerField(
        required=True,
    )
    object_relation = serializers.ChoiceField(
        required=True,
        choices=RELATION_DICT,
        write_only=True,
    )
    object_title = serializers.CharField(
        read_only=True,
    )
    object_status = serializers.CharField(
        read_only=True,
    )
    object_type = serializers.CharField(
        required=True,
    )
    parent_link = serializers.CharField(
        read_only=True,
    )
    link_relationship = serializers.CharField(
        read_only=True,
    )
    reverse_relation = serializers.BooleanField(
        read_only=True,
    )
