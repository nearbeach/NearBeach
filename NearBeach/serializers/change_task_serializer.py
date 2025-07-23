from rest_framework import serializers
from NearBeach.models import ChangeTask
from django.contrib.auth.models import User
from NearBeach.serializers.enum_serializer import EnumField
from NearBeach.serializers.user_django_serializer import UserDjangoSerializer
from NearBeach.utils.enums.request_for_change_enums import RequestForChangeStatus


class ChangeTaskSerializer(serializers.ModelSerializer):
    change_task_assigned_user = UserDjangoSerializer(
        many=False,
        allow_null=False,
    )
    change_task_qa_user = UserDjangoSerializer(
        many=False,
        allow_null=False,
    )
    change_task_required_by = serializers.CharField(
        required=False,
    )
    change_task_seconds = serializers.ReadOnlyField()
    change_task_start_date = serializers.DateTimeField(
        required=True,
    )
    change_task_status = EnumField(
        enum=RequestForChangeStatus,
        read_only=True,
    )
    is_downtime = serializers.BooleanField(
        required=False,
    )
    request_for_change = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    def create(self, validated_data):
        start_date = validated_data["change_task_start_date"]
        end_date = validated_data["change_task_end_date"]

        # Create the change task seconds
        validated_data["change_task_seconds"] = int((end_date - start_date).total_seconds())

        # Check for stakeholder
        if "change_task_required_by" not in validated_data:
            validated_data["change_task_required_by"] = "Stakeholder(s)"

        # Change task status
        validated_data["change_task_status"] = RequestForChangeStatus.DRAFT

        # Create the change task
        change_task = ChangeTask.objects.create(**validated_data)

        return change_task

    def get_fields(self):
        fields = super().get_fields()

        # Check to see if request exists in context
        if "request" not in self.context:
            return fields

        # Updating the change task
        if self.context["request"].method in ["POST", "PUT"]:
            fields["change_task_assigned_user"] = serializers.PrimaryKeyRelatedField(
                queryset=User.objects.filter(
                    is_active=True,
                )
            )
            fields["change_task_qa_user"] = serializers.PrimaryKeyRelatedField(
                queryset=User.objects.filter(
                    is_active=True,
                )
            )

        return fields
    
    def update(self, instance, validated_data):
        start_date = validated_data["change_task_start_date"]
        end_date = validated_data["change_task_end_date"]
        validated_data["change_task_seconds"] = int((end_date - start_date).total_seconds())

        # Update
        instance = super().update(instance, validated_data)
        return instance
        
    class Meta:
        model = ChangeTask
        fields = [
            "change_task_id",
            "change_task_title",
            "change_task_description",
            "change_task_assigned_user",
            "change_task_qa_user",
            "change_task_status",
            "is_downtime",
            "change_task_seconds",
            "change_task_start_date",
            "change_task_end_date",
            "change_task_required_by",
            "request_for_change",
        ]
