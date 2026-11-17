"""Focused audit service tests, without API authentication or application fixtures."""
from datetime import datetime, timedelta, timezone
from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, TestCase

from NearBeach.models.audit_log import AuditLog
from NearBeach.models.project import Project, ListOfProjectStatus
from NearBeach.serializers.audit_log_serializer import AuditLogSerializer
from NearBeach.services.AuditService import AuditService
from NearBeach.utils.enums.audit_enums import AuditAction


class AuditSnapshotTests(SimpleTestCase):
    def test_snapshot_uses_raw_foreign_keys_and_excludes_bookkeeping(self):
        project = Project(id=7, title="Example", status_id=42, change_user_id=9,
                          creation_user_id=9, is_deleted=True)
        snapshot = AuditService.snapshot(project)
        self.assertEqual(snapshot["status"], 42)
        self.assertEqual(snapshot["title"], "Example")
        self.assertTrue({"id", "date_created", "date_modified", "change_user",
                         "creation_user", "is_deleted"}.isdisjoint(snapshot))
        self.assertNotIn("status", project._state.fields_cache)

    def test_scalar_diff_keeps_falsy_values_and_ignores_unchanged_fields(self):
        before = {"title": "Same", "story_point": 1, "description": "Text"}
        after = {"title": "Same", "story_point": 0, "description": ""}
        self.assertEqual(AuditService.diff(before, after, Project()), {
            "story_point": {"old": 1, "new": 0},
            "description": {"old": "Text", "new": ""},
        })

    def test_unchanged_foreign_key_needs_no_database_lookup(self):
        self.assertEqual(AuditService.diff({"status": 42}, {"status": 42}, Project()), {})

    def test_all_secret_markers_are_case_insensitive_and_preserve_empty_values(self):
        for name in ("PASSWORD", "Access_Token", "client_SECRET", "API_KEY", "PRIVATE_KEY"):
            for value, expected in (("sensitive", "***"), (0, "***"), (None, None), ("", "")):
                with self.subTest(name=name, value=value):
                    self.assertEqual(AuditService._mask(name, value), expected)
        self.assertEqual(AuditService._mask("description", "public"), "public")

    def test_ip_uses_remote_address_without_trusting_forwarded_headers(self):
        for meta, expected in (({}, None), (None, None), ({"REMOTE_ADDR": ""}, None),
                               ({"HTTP_X_FORWARDED_FOR": "203.0.113.5"}, None),
                               ({"REMOTE_ADDR": "::1", "HTTP_X_FORWARDED_FOR": "203.0.113.5"}, "::1")):
            with self.subTest(meta=meta):
                self.assertEqual(AuditService._ip_address(SimpleNamespace(META=meta)), expected)
        self.assertIsNone(AuditService._ip_address(SimpleNamespace()))


class AuditPersistenceTests(TestCase):
    def entry(self, **kwargs):
        values = {"object_type": "project", "object_id": 1, "action": AuditAction.UPDATE}
        return AuditLog.objects.create(**(values | kwargs))

    def test_record_converts_id_truncates_summary_and_captures_actor(self):
        user = User.objects.create_user(username="actor")
        request = SimpleNamespace(user=user, META={"REMOTE_ADDR": "203.0.113.1"})
        entry = AuditService.record(request, "project", "12", AuditAction.UPDATE,
                                    summary="x" * 256)
        entry.refresh_from_db()
        self.assertEqual((entry.object_id, entry.username, entry.user), (12, "actor", user))
        self.assertEqual(entry.ip_address, "203.0.113.1")
        self.assertEqual(entry.summary, "x" * 255)
        self.assertEqual(entry.changes, {})

    def test_foreign_key_diff_labels_existing_values_and_preserves_missing_ids(self):
        status = ListOfProjectStatus.objects.create(status="Ready")
        missing_id = status.pk + 100
        self.assertEqual(AuditService.diff(
            {"status": status.pk}, {"status": missing_id}, Project()),
            {"status": {"old": "Ready", "new": missing_id}})
        self.assertEqual(AuditService.diff(
            {"status": status.pk}, {"status": None}, Project()),
            {"status": {"old": "Ready", "new": None}})

    def test_noop_update_does_not_write_even_when_bookkeeping_changes(self):
        project = Project(title="Unchanged", status_id=1)
        before = AuditService.snapshot(project)
        project.is_deleted = True
        project.change_user_id = 22
        with self.assertNumQueries(0):
            self.assertIsNone(AuditService.record_update(SimpleNamespace(), "project", before, project))
        self.assertFalse(AuditLog.objects.exists())

    def test_list_isolates_type_and_id_and_breaks_timestamp_ties_by_id(self):
        first = self.entry()
        second = self.entry()
        self.entry(object_type="customer")
        self.entry(object_id=2)
        AuditLog.objects.update(date_created=datetime(2026, 1, 1, tzinfo=timezone.utc))
        self.assertEqual(list(AuditService.get_list("project", "1")), [second, first])

    def test_prune_keeps_exact_cutoff_and_newer_entries(self):
        now = datetime(2026, 1, 31, tzinfo=timezone.utc)
        cutoff = now - timedelta(days=30)
        entries = [self.entry() for _ in range(3)]
        for entry, delta in zip(entries, (-1, 0, 1)):
            AuditLog.objects.filter(pk=entry.pk).update(
                date_created=cutoff + timedelta(microseconds=delta))
        with patch("NearBeach.services.AuditService.timezone.now", return_value=now):
            self.assertEqual(AuditService.prune(30), 1)
        self.assertEqual(set(AuditLog.objects.values_list("pk", flat=True)),
                         {entries[1].pk, entries[2].pk})

    def test_scrub_only_changes_matching_object_and_is_repeatable(self):
        target = self.entry(changes={"name": {"old": "A", "new": "B"}}, summary="Updated")
        other_type = self.entry(object_type="customer", summary="Keep")
        other_id = self.entry(object_id=2, summary="Keep")
        for _ in range(2):
            self.assertEqual(AuditService.scrub_object("project", "1"), 1)
        target.refresh_from_db()
        self.assertEqual((target.changes, target.summary, target.action),
                         ({}, "Personal data erased", AuditAction.UPDATE))
        for entry in (other_type, other_id):
            entry.refresh_from_db()
            self.assertEqual(entry.summary, "Keep")
        self.assertEqual(AuditService.scrub_object("project", 999), 0)

    def test_anonymise_only_erases_target_actor_and_keeps_change_history(self):
        user = User.objects.create_user(username="erase")
        other = User.objects.create_user(username="keep")
        target = self.entry(user=user, username="erase", ip_address="::1",
                            changes={"title": {"old": "A", "new": "B"}})
        untouched = self.entry(user=other, username="keep", ip_address="::1")
        self.assertEqual(AuditService.anonymise_user(user), 1)
        self.assertEqual(AuditService.anonymise_user(user), 0)
        target.refresh_from_db()
        untouched.refresh_from_db()
        self.assertEqual((target.user_id, target.username, target.ip_address), (None, "erased user", None))
        self.assertEqual(target.changes, {"title": {"old": "A", "new": "B"}})
        self.assertEqual((untouched.user_id, untouched.username, untouched.ip_address), (other.pk, "keep", "::1"))

    def test_deleting_actor_preserves_history_and_username(self):
        user = User.objects.create_user(username="former")
        entry = self.entry(user=user, username="former")
        user.delete()
        entry.refresh_from_db()
        self.assertIsNone(entry.user_id)
        self.assertEqual(entry.username, "former")

    def test_serializer_exposes_only_public_read_only_fields(self):
        entry = self.entry(username="actor", ip_address="::1")
        serializer = AuditLogSerializer(entry)
        self.assertEqual(set(serializer.data),
                         {"id", "date_created", "username", "action", "summary", "changes"})
        self.assertTrue(all(field.read_only for field in serializer.fields.values()))


class PruneAuditCommandTests(SimpleTestCase):
    def test_explicit_days_overrides_setting_and_reports_deleted_count(self):
        output = StringIO()
        with self.settings(AUDIT_RETENTION_DAYS=730), patch.object(AuditService, "prune", return_value=4) as prune:
            call_command("prune_audit", days=1, stdout=output)
        prune.assert_called_once_with(1)
        self.assertEqual(output.getvalue().strip(), "Removed 4 audit entries older than 1 days")

    def test_invalid_explicit_or_configured_retention_never_prunes(self):
        for days in (0, -1):
            for options in ({"days": days}, {}):
                with self.subTest(days=days, options=options), self.settings(AUDIT_RETENTION_DAYS=days):
                    with patch.object(AuditService, "prune") as prune:
                        with self.assertRaisesMessage(CommandError, "--days must be 1 or more"):
                            call_command("prune_audit", **options)
                        prune.assert_not_called()
