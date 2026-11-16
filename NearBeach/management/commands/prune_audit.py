"""Delete audit log entries older than the retention period (GDPR)"""

from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

from NearBeach.services.AuditService import AuditService


class Command(BaseCommand):
    help = (
        "Delete audit log entries older than --days (default: settings.AUDIT_RETENTION_DAYS). "
        "Run on a schedule, e.g. daily from cron."
    )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--days",
            type=int,
            default=None,
            help="Keep this many days of history. Defaults to AUDIT_RETENTION_DAYS.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        days = options["days"] if options["days"] is not None else settings.AUDIT_RETENTION_DAYS
        if days < 1:
            raise CommandError("--days must be 1 or more")

        removed = AuditService.prune(days)
        self.stdout.write(f"Removed {removed} audit entries older than {days} days")
