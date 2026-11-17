"""Tests for the audit log: what gets recorded, who it is attributed to, and retention / GDPR scrubbing.

Fixture data: projects 1 and 2 (status 1 "New", higher order "Backlog"); status 6 is "Closed".
"""
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone

from NearBeach.models.audit_log import AuditLog
from NearBeach.models.project import Project
from NearBeach.services.AuditService import AuditService
from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.utils.enums.audit_enums import AuditAction

PROJECT_URL = "/api/v1/project/1/"
AUDIT_URL = "/api/v1/project/1/audit/"


class AuditLogRecordingTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def entries(self, object_id=1):
        return AuditLog.objects.filter(object_type="project", object_id=object_id)

    def test_update_records_only_the_changed_fields(self):
        self.client.patch(PROJECT_URL, {"title": "Renamed"}, format="json")

        entry = self.entries().get()
        self.assertEqual(entry.action, AuditAction.UPDATE)
        self.assertEqual(list(entry.changes), ["title"])
        self.assertEqual(entry.changes["title"]["new"], "Renamed")
        self.assertEqual(entry.username, "admin")
        self.assertEqual(entry.user, User.objects.get(username="admin"))

    def test_update_with_no_real_change_records_nothing(self):
        title = Project.objects.get(pk=1).title

        self.client.patch(PROJECT_URL, {"title": title}, format="json")

        self.assertFalse(self.entries().exists())

    def test_closing_a_project_is_recorded_as_a_close_with_readable_status(self):
        response = self.client.patch(PROJECT_URL, {"status": 6}, format="json")
        self.assertEqual(response.status_code, 200)

        entry = self.entries().get()
        self.assertEqual(entry.action, AuditAction.CLOSE)
        self.assertEqual(entry.changes["status"], {"old": "New", "new": "Closed"})

    def test_non_closing_status_change_is_a_status_change(self):
        self.client.patch(PROJECT_URL, {"status": 4}, format="json")

        self.assertEqual(self.entries().get().action, AuditAction.STATUS_CHANGE)

    def test_create_records_every_field(self):
        response = self.client.post(
            "/api/v1/project/", {"title": "Audited", "group_list": [1]}, format="json"
        )
        self.assertEqual(response.status_code, 201)

        entry = self.entries(response.data["id"]).get()
        self.assertEqual(entry.action, AuditAction.CREATE)
        self.assertEqual(entry.changes["title"], {"old": None, "new": "Audited"})
        self.assertIn("status", entry.changes)

    def test_delete_is_recorded(self):
        self.assertEqual(self.client.delete(PROJECT_URL).status_code, 204)

        self.assertEqual(self.entries().get().action, AuditAction.DELETE)

    def test_a_rejected_update_records_nothing(self):
        response = self.client.patch(PROJECT_URL, {"title": ""}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.entries().exists())

    def test_customer_changes_are_recorded_against_the_customer(self):
        self.client.patch(
            "/api/v1/organisation/1/customer/1/", {"first_name": "Patched"}, format="json"
        )

        entry = AuditLog.objects.get(object_type="customer", object_id=1)
        self.assertEqual(entry.changes["first_name"]["new"], "Patched")

    def test_organisation_changes_are_recorded(self):
        self.client.patch("/api/v1/organisation/1/", {"name": "Renamed Org"}, format="json")

        entry = AuditLog.objects.get(object_type="organisation", object_id=1)
        self.assertEqual(entry.changes["name"]["new"], "Renamed Org")


class AuditLogReadTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_endpoint_lists_newest_first_and_paginates(self):
        self.client.patch(PROJECT_URL, {"title": "First"}, format="json")
        self.client.patch(PROJECT_URL, {"title": "Second"}, format="json")

        response = self.client.get(AUDIT_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["changes"]["title"]["new"], "Second")

    def test_endpoint_never_exposes_the_ip_address(self):
        self.client.patch(PROJECT_URL, {"title": "Renamed"}, format="json")

        result = self.client.get(AUDIT_URL).data["results"][0]

        self.assertNotIn("ip_address", result)

    def test_endpoint_only_shows_the_requested_project(self):
        self.client.patch("/api/v1/project/2/", {"title": "Other"}, format="json")

        self.assertEqual(self.client.get(AUDIT_URL).data["count"], 0)


class AuditServiceUnitTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_secret_looking_fields_are_masked(self):
        self.assertEqual(AuditService._mask("api_token", "abc"), "***")
        self.assertEqual(AuditService._mask("user_password", "abc"), "***")
        # Empty values stay empty, so "was blank" is still visible
        self.assertEqual(AuditService._mask("api_token", ""), "")
        self.assertEqual(AuditService._mask("title", "abc"), "abc")

    def test_audit_entries_can_not_be_edited_through_save(self):
        entry = AuditLog.objects.create(
            object_type="project", object_id=1, action=AuditAction.UPDATE
        )
        entry.summary = "tampered"

        with self.assertRaises(ValueError):
            entry.save()


class AuditRetentionTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def make_entry(self, age_days, **kwargs):
        entry = AuditLog.objects.create(
            object_type="project", object_id=1, action=AuditAction.UPDATE, **kwargs
        )
        AuditLog.objects.filter(pk=entry.pk).update(
            date_created=timezone.now() - timedelta(days=age_days)
        )
        return entry

    def test_prune_removes_only_entries_past_the_retention_period(self):
        old = self.make_entry(400)
        recent = self.make_entry(10)

        removed = AuditService.prune(365)

        self.assertEqual(removed, 1)
        self.assertFalse(AuditLog.objects.filter(pk=old.pk).exists())
        self.assertTrue(AuditLog.objects.filter(pk=recent.pk).exists())

    def test_prune_command_uses_the_setting_by_default(self):
        with self.settings(AUDIT_RETENTION_DAYS=30):
            old = self.make_entry(31)
            recent = self.make_entry(29)
            call_command("prune_audit")

        self.assertFalse(AuditLog.objects.filter(pk=old.pk).exists())
        self.assertTrue(AuditLog.objects.filter(pk=recent.pk).exists())

    def test_scrub_object_erases_values_but_keeps_the_entry(self):
        entry = self.make_entry(1, changes={"first_name": {"old": "A", "new": "B"}}, summary="x")

        AuditService.scrub_object("project", 1)

        entry.refresh_from_db()
        self.assertEqual(entry.changes, {})
        self.assertEqual(entry.summary, "Personal data erased")

    def test_anonymise_user_removes_who_and_ip(self):
        user = User.objects.get(username="admin")
        entry = self.make_entry(1, user=user, username="admin", ip_address="10.0.0.1")

        AuditService.anonymise_user(user)

        entry.refresh_from_db()
        self.assertIsNone(entry.user)
        self.assertIsNone(entry.ip_address)
        self.assertNotEqual(entry.username, "admin")


class AuditTransactionTests(BaseApiClass):
    """An audit failure must roll back the associated service mutation."""

    username = "admin"
    password = "Test1234$"

    def test_audit_write_failure_rolls_back_updates_and_soft_deletes(self):
        from unittest.mock import patch

        from NearBeach.models.customer import Customer
        from NearBeach.models.organisation import Organisation

        cases = (
            (Project, PROJECT_URL, "title", "Renamed"),
            (Organisation, "/api/v1/organisation/1/", "name", "Renamed"),
            (Customer, "/api/v1/organisation/1/customer/1/", "first_name", "Renamed"),
        )
        for model, url, field, value in cases:
            for method in ("patch", "delete"):
                with self.subTest(model=model.__name__, method=method):
                    original = model.objects.get(pk=1)
                    with patch.object(AuditService, "record", side_effect=RuntimeError("Audit unavailable")):
                        with self.assertRaisesMessage(RuntimeError, "Audit unavailable"):
                            if method == "patch":
                                self.client.patch(url, {field: value}, format="json")
                            else:
                                self.client.delete(url)
                    current = model.objects.get(pk=1)
                    self.assertEqual(getattr(current, field), getattr(original, field))
                    self.assertFalse(current.is_deleted)
                    self.assertEqual(current.change_user_id, original.change_user_id)
                    self.assertEqual(current.date_modified, original.date_modified)
                    self.assertFalse(AuditLog.objects.exists())

    def test_audit_write_failure_rolls_back_project_creation(self):
        from unittest.mock import patch

        count = Project.objects.count()
        with patch.object(AuditService, "record", side_effect=RuntimeError("Audit unavailable")):
            with self.assertRaisesMessage(RuntimeError, "Audit unavailable"):
                self.client.post("/api/v1/project/", {"title": "Audited", "group_list": [1]}, format="json")
        self.assertEqual(Project.objects.count(), count)
        self.assertFalse(AuditLog.objects.exists())
