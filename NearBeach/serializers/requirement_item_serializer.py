from NearBeach.serializers.object_data.types.requirement_item_types_serializer import RequirementItemTypesSerializer
from rest_framework import serializers
from NearBeach.models.requirement.requirement_item import ListOfRequirementItemStatus, RequirementItem, ListOfRequirementItemType
from NearBeach.serializers.abstraction.base_object_serializer import BaseObjectSerializer
from NearBeach.serializers.abstraction.date_fields_serializer import DateFieldsSerializer
from NearBeach.serializers.group_serializer import GroupSerializer
from NearBeach.serializers.object_data.status.requirement_item_status_serializer import RequirementItemStatusSerializer
from NearBeach.serializers.user.user_serializer import UserSerializer
from NearBeach.models.object_assignment.object_assignment import ObjectAssignment


class RequirementItemSerializer(serializers.ModelSerializer, BaseObjectSerializer, DateFieldsSerializer):
    """Class containing serializer base for all objects"""

    status = RequirementItemStatusSerializer(
        many=False,
        read_only=False,
        allow_null=False,
        required=False,
    )
    type = RequirementItemTypesSerializer(
        many=False,
        read_only=False,
        allow_null=False,
        required=False,
    )

    def create(self, validated_data):
        """Method for creating a requirement_item"""
        group_list = validated_data.pop("group_list", [])

        # Extract data we need
        validated_data["status"] = ListOfRequirementItemStatus.objects.filter(
            is_deleted=False
        ).order_by(
            "sort_order",
        ).first()

        validated_data["type"] = ListOfRequirementItemType.objects.filter(
            is_deleted=False
        ).order_by(
            "id",
        ).first()

        # Create the requirement_item
        requirement_item = RequirementItem.objects.create(**validated_data)

        # Create the group list
        for single_group in group_list:
            # Save the group against the new requirement_item
            submit_object_assignment = ObjectAssignment(
                group=single_group,
                requirement_item=requirement_item,
                change_user=validated_data["change_user"],
            )
            submit_object_assignment.save()

        return requirement_item

    def get_fields(self):
        fields = super().get_fields()

        # PATCH
        method = self.context.get("method", None)
        if method == "PATCH":
            fields.pop("group_list", None)
            fields["status"] = serializers.PrimaryKeyRelatedField(
                queryset=ListOfRequirementItemStatus.objects.filter(
                    is_deleted=False,
                ),
            )

        if method == "GET":
            fields["group_list"] = GroupSerializer(
                many=True,
                read_only=True,
                required=False,
            )

            fields["user_list"] = UserSerializer(
                many=True,
                read_only=True,
                required=False,
            )

        return fields

    class Meta:
        model = RequirementItem
        fields = [
            "id",
            "title",
            "description",
            "status",
            "type",
            "group_list",
            "user_list",
            "date_created",
            "date_modified",
        ]


class RequirementItemDetailSerializer(RequirementItemSerializer):
    """The shape of a single requirement_item (GET): groups are readable here and the users are included.

    Exists so the API documentation can describe retrieve accurately; the endpoint itself passes
    `context={"method": "GET"}` to RequirementItemSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "GET"}

        return super().get_fields()


class RequirementItemPatchSerializer(RequirementItemSerializer):
    """The PATCH shape of a requirement_item - request and response (no groups, organisation or users; status is an id).

    Exists so the API documentation can describe PATCH accurately; the endpoint itself passes
    `context={"method": "PATCH"}` to RequirementItemSerializer.
    """

    def get_fields(self):
        self._context = {**self._context, "method": "PATCH"}
        fields = super().get_fields()

        # Read-only, and only ever filled in by a GET of a single requirement_item
        fields.pop("user_list", None)

        return fields
