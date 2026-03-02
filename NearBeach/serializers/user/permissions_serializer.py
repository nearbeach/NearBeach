from rest_framework import serializers

from NearBeach.serializers.group_serializer import GroupSerializer


class PermissionSerializer(serializers.Serializer):
    """Class for permission serializer"""
    administration_assign_user_to_group = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    administration_create_group = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    administration_create_permission_set = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    administration_create_user = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    customer = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    document = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    group_id = serializers.IntegerField()
    group_name = serializers.CharField()
    kanban_board = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    organisation = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    organisation_note = serializers.IntegerField(
        min_value=0,
        max_value=1,
    )
    project = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    project_note = serializers.IntegerField(
        min_value=0,
        max_value=1,
    )
    request_for_change = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    requirement = serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    requirement_item_note = serializers.IntegerField(
        min_value=0,
        max_value=1,
    )
    requirement_note =  serializers.IntegerField(
        min_value=0,
        max_value=1,
    )
    schedule_object =  serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    sprint =  serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    task =  serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    tag =  serializers.IntegerField(
        min_value=0,
        max_value=4,
    )
    kanban_note = serializers.IntegerField(
        min_value=0,
        max_value=1,
    )
    task_note = serializers.IntegerField(
        min_value=0,
        max_value=1,
    )
