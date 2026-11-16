"""Tests for the `meta_data` JSON field (card #518).

Fixture data: organisation 1 has customer 1; project 1 is visible to the admin; public link
3d7346c4-... points at project 1.
"""
import json

from django.apps import apps
from django.test import SimpleTestCase

from NearBeach.models.abstraction.meta_data_abstraction import MetaDataAbstraction
from NearBeach.models.audit_log import AuditLog
from NearBeach.models.customer import Customer
from NearBeach.models.organisation import Organisation
from NearBeach.models.project import Project
from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.utils.meta_data import META_DATA_MAX_BYTES, merge_meta_data

ORGANISATION_URL = "/api/v1/organisation/1/"
CUSTOMER_URL = "/api/v1/organisation/1/customer/1/"
PROJECT_URL = "/api/v1/project/1/"
# Project 2 is readable (but not editable) by the read_only user; project 1 is not visible to them
READ_ONLY_PROJECT_URL = "/api/v1/project/2/"
PUBLIC_LINK_URL = "/api/v1/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/"

OBJECTS_WITH_META_DATA = {
    "Organisation", "Customer", "Project", "Task", "Requirement", "RequirementItem",
    "RequestForChange", "ChangeTask", "KanbanBoard", "KanbanCard", "Sprint",
}


class MergeMetaDataTests(SimpleTestCase):
    def test_adds_a_key(self):
        self.assertEqual(merge_meta_data({"a": 1}, {"b": 2}), {"a": 1, "b": 2})

    def test_updates_a_key(self):
        self.assertEqual(merge_meta_data({"a": 1}, {"a": 2}), {"a": 2})

    def test_keeps_keys_that_are_not_sent(self):
        self.assertEqual(merge_meta_data({"a": 1, "b": 2}, {"a": 3}), {"a": 3, "b": 2})

    def test_null_deletes_a_key(self):
        self.assertEqual(merge_meta_data({"a": 1, "b": 2}, {"a": None}), {"b": 2})

    def test_deleting_a_missing_key_is_a_no_op(self):
        self.assertEqual(merge_meta_data({"a": 1}, {"zzz": None}), {"a": 1})

    def test_nested_objects_merge(self):
        existing = {"plugin": {"x": 1, "y": 2}}
        self.assertEqual(
            merge_meta_data(existing, {"plugin": {"y": 3, "z": 4}}),
            {"plugin": {"x": 1, "y": 3, "z": 4}},
        )

    def test_nested_null_deletes(self):
        self.assertEqual(
            merge_meta_data({"plugin": {"x": 1, "y": 2}}, {"plugin": {"x": None}}),
            {"plugin": {"y": 2}},
        )

    def test_nested_object_replaces_a_scalar(self):
        self.assertEqual(merge_meta_data({"a": 1}, {"a": {"b": 2}}), {"a": {"b": 2}})

    def test_nested_null_in_a_new_object_is_dropped(self):
        self.assertEqual(merge_meta_data({}, {"a": {"b": None, "c": 1}}), {"a": {"c": 1}})

    def test_arrays_are_replaced_whole(self):
        self.assertEqual(merge_meta_data({"a": [1, 2, 3]}, {"a": [9]}), {"a": [9]})

    def test_empty_patch_changes_nothing(self):
        self.assertEqual(merge_meta_data({"a": {"b": 1}}, {}), {"a": {"b": 1}})

    def test_arguments_are_not_modified(self):
        existing = {"a": {"b": 1}}
        patch = {"a": {"c": 2}}

        merge_meta_data(existing, patch)

        self.assertEqual(existing, {"a": {"b": 1}})
        self.assertEqual(patch, {"a": {"c": 2}})


class MetaDataModelTests(SimpleTestCase):
    def test_every_listed_object_has_the_field(self):
        for name in OBJECTS_WITH_META_DATA:
            with self.subTest(model=name):
                model = apps.get_model("NearBeach", name)
                self.assertTrue(issubclass(model, MetaDataAbstraction))
                self.assertIn("meta_data", [f.name for f in model._meta.get_fields()])

    def test_other_models_do_not_have_it(self):
        for name in ("Group","PermissionSet", "ObjectAssignment", "ObjectNote", "Document"):
            with self.subTest(model=name):
                model = apps.get_model("NearBeach", name)
                self.assertFalse(issubclass(model, MetaDataAbstraction))


class MetaDataApiTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def _patch(self, url, meta_data):
        return self.client.patch(url, {"meta_data": meta_data}, format="json")

    def test_defaults_to_an_empty_object(self):
        for url in (ORGANISATION_URL, CUSTOMER_URL, PROJECT_URL):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).data["meta_data"], {})

    def test_patch_sets_and_returns_meta_data(self):
        for url, model in ((ORGANISATION_URL, Organisation), (CUSTOMER_URL, Customer), (PROJECT_URL, Project)):
            with self.subTest(url=url):
                response = self._patch(url, {"a": 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["meta_data"], {"a": 1})
                self.assertEqual(model.objects.get(pk=1).meta_data, {"a": 1})

    def test_patch_merges_and_keeps_other_keys(self):
        self._patch(PROJECT_URL, {"a": 1, "b": 2})

        response = self._patch(PROJECT_URL, {"b": 3, "c": 4})

        self.assertEqual(response.data["meta_data"], {"a": 1, "b": 3, "c": 4})
        self.assertEqual(Project.objects.get(pk=1).meta_data, {"a": 1, "b": 3, "c": 4})

    def test_patch_null_deletes_a_key(self):
        self._patch(PROJECT_URL, {"a": 1, "b": 2})

        response = self._patch(PROJECT_URL, {"b": None, "c": 3})

        self.assertEqual(response.data["meta_data"], {"a": 1, "c": 3})

    def test_patch_without_meta_data_leaves_it_alone(self):
        self._patch(PROJECT_URL, {"a": 1})

        response = self.client.patch(PROJECT_URL, {"title": "Renamed"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.get(pk=1).meta_data, {"a": 1})

    def test_whole_value_must_be_an_object(self):
        for value in ([1, 2], "text", 5, None):
            with self.subTest(value=value):
                response = self._patch(PROJECT_URL, value)

                self.assertEqual(response.status_code, 400)
                self.assertIn("meta_data", response.data)

        self.assertEqual(Project.objects.get(pk=1).meta_data, {})

    def test_result_over_the_size_cap_is_rejected(self):
        big = "x" * (META_DATA_MAX_BYTES + 1)

        response = self._patch(PROJECT_URL, {"big": big})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Project.objects.get(pk=1).meta_data, {})

    def test_small_patches_cannot_add_up_past_the_cap(self):
        chunk = "x" * (META_DATA_MAX_BYTES // 2)
        self.assertEqual(self._patch(PROJECT_URL, {"one": chunk}).status_code, 200)

        response = self._patch(PROJECT_URL, {"two": chunk})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(list(Project.objects.get(pk=1).meta_data), ["one"])

    def test_delete_frees_up_room_under_the_cap(self):
        chunk = "x" * (META_DATA_MAX_BYTES // 2)
        self._patch(PROJECT_URL, {"one": chunk})

        # Swap the large key for another one in a single patch
        response = self._patch(PROJECT_URL, {"one": None, "two": chunk})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(Project.objects.get(pk=1).meta_data), ["two"])

    def test_create_stores_meta_data_without_null_keys(self):
        response = self.client.post(
            "/api/v1/project/",
            {"title": "With meta", "group_list": [1], "meta_data": {"a": 1, "gone": None}},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.get(pk=response.data["id"]).meta_data, {"a": 1})

    def test_changes_are_written_to_the_audit_log(self):
        before = AuditLog.objects.filter(object_type="project", object_id=1).count()

        self._patch(PROJECT_URL, {"a": 1})

        entries = AuditLog.objects.filter(object_type="project", object_id=1)
        self.assertEqual(entries.count(), before + 1)
        self.assertIn("meta_data", entries.latest("id").changes)

    def test_public_link_does_not_expose_meta_data(self):
        self._patch(PROJECT_URL, {"secret": "internal"})

        response = self.client.get(PUBLIC_LINK_URL)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("meta_data", response.data)
        self.assertNotIn("internal", json.dumps(response.data))


class MetaDataReadOnlyTests(BaseApiClass):
    username = "read_only"
    password = "Test1234$"

    def test_read_only_user_cannot_change_meta_data(self):
        response = self.client.patch(READ_ONLY_PROJECT_URL, {"meta_data": {"a": 1}}, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Project.objects.get(pk=2).meta_data, {})

    def test_read_only_user_can_read_meta_data(self):
        Project.objects.filter(pk=2).update(meta_data={"a": 1})

        response = self.client.get(READ_ONLY_PROJECT_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["meta_data"], {"a": 1})
