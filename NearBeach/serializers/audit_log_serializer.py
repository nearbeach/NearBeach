from rest_framework import serializers

from NearBeach.models.audit_log import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    """Read-only view of an audit entry. The IP address is stored but never sent out."""

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "date_created",
            "username",
            "action",
            "summary",
            "changes",
        ]
        read_only_fields = fields
