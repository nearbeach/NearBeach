"""Bulk writes must invalidate permissions even though they bypass save signals."""
from unittest.mock import patch

from django.db import DatabaseError, models
from django.test import SimpleTestCase

from NearBeach.models.abstraction.permission_queryset import PermissionAwareQuerySet
from NearBeach.models.permission.permission_set import PermissionSet


class PermissionAwareQuerySetTests(SimpleTestCase):
    def test_bulk_writes_forward_arguments_and_preserve_results(self):
        rows = [PermissionSet(name="Test")]
        cases = [
            ("update", (), {"is_deleted": True}, 2),
            ("delete", (), {}, (2, {"NearBeach.PermissionSet": 2})),
            ("bulk_create", (rows,), {"batch_size": 10, "ignore_conflicts": True}, rows),
            ("bulk_update", (rows, ["project"]), {"batch_size": 10}, 1),
        ]
        for method, args, kwargs, expected in cases:
            with self.subTest(method=method), patch.object(models.QuerySet, method, return_value=expected) as write, patch(
                "NearBeach.models.abstraction.permission_queryset._bump_permission_cache"
            ) as bump:
                result = getattr(PermissionAwareQuerySet(model=PermissionSet), method)(*args, **kwargs)
                self.assertEqual(result, expected)
                write.assert_called_once_with(*args, **kwargs)
                bump.assert_called_once_with()

    def test_failed_writes_do_not_invalidate_or_hide_database_errors(self):
        for method, args in (("update", ()), ("delete", ()), ("bulk_create", ([],)), ("bulk_update", ([], ["project"]))):
            with self.subTest(method=method), patch.object(models.QuerySet, method, side_effect=DatabaseError("write failed")), patch(
                "NearBeach.models.abstraction.permission_queryset._bump_permission_cache"
            ) as bump:
                with self.assertRaisesMessage(DatabaseError, "write failed"):
                    getattr(PermissionAwareQuerySet(model=PermissionSet), method)(*args)
                bump.assert_not_called()
