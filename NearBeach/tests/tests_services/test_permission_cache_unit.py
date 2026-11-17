"""Database-free checks for permission cache boundaries and invalidation timing."""
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.core.cache import cache
from django.test import SimpleTestCase, override_settings

from NearBeach.utils import permission_cache


@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
    PERMISSION_CACHE_TTL=300,
)
class PermissionCacheUnitTests(SimpleTestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.user = SimpleNamespace(pk=12, is_authenticated=True)

    def test_object_cache_separates_every_permission_dimension(self):
        lookups = [
            (self.user, "project", 2, None),
            (SimpleNamespace(pk=13, is_authenticated=True), "project", 2, None),
            (self.user, "task", 2, None),
            (self.user, "project", 3, None),
            (self.user, "project", 2, "project_note"),
        ]
        answers = [(1, False), (4, False), (2, False), (-1, False), (1, True)]
        expected = [(1, False), (4, False), (2, False), (None, False), (1, True)]
        with patch.object(permission_cache, "_build_object_permission", side_effect=answers) as build:
            for lookup, answer in zip(lookups, expected):
                self.assertEqual(permission_cache.get_object_permission(*lookup), answer)
            for lookup, answer in zip(lookups, expected):
                self.assertEqual(permission_cache.get_object_permission(*lookup), answer)
            self.assertEqual(build.call_count, len(lookups))

    def test_anonymous_and_unsaved_users_bypass_object_cache(self):
        for user in (
            SimpleNamespace(pk=12, is_authenticated=False),
            SimpleNamespace(pk=None, is_authenticated=True),
            SimpleNamespace(),
        ):
            with self.subTest(user=user), patch.object(
                permission_cache, "_build_object_permission", side_effect=[(1, False), (4, True)]
            ) as build:
                self.assertEqual(permission_cache.get_object_permission(user, "project", 2), (1, False))
                self.assertEqual(permission_cache.get_object_permission(user, "project", 2), (4, True))
                self.assertEqual(build.call_count, 2)

    def test_zero_level_and_denial_are_distinct_cached_results(self):
        for level, expected in ((0, 0), (-1, None)):
            cache.clear()
            with self.subTest(level=level), patch.object(
                permission_cache, "_build_object_permission", return_value=(level, False)
            ) as build:
                for _ in range(2):
                    self.assertEqual(permission_cache.get_object_permission(self.user, "project", 2), (expected, False))
                build.assert_called_once()

    def test_nonpositive_timeout_bypasses_even_a_warm_cache(self):
        with patch.object(permission_cache, "_build_object_permission", return_value=(4, False)):
            permission_cache.get_object_permission(self.user, "project", 2)
        for timeout in (0, -1):
            with self.subTest(timeout=timeout), override_settings(PERMISSION_CACHE_TTL=timeout), patch.object(
                permission_cache, "_build_object_permission", return_value=(-1, False)
            ) as build:
                for _ in range(2):
                    self.assertEqual(permission_cache.get_object_permission(self.user, "project", 2), (None, False))
                self.assertEqual(build.call_count, 2)

    def test_entry_expires_at_configured_timeout(self):
        build = Mock(side_effect=[1, 4])
        with override_settings(PERMISSION_CACHE_TTL=10), patch("time.time", return_value=1000):
            self.assertEqual(permission_cache._cached("expiry", build), 1)
        with patch("time.time", return_value=1009):
            self.assertEqual(permission_cache._cached("expiry", build), 1)
        with patch("time.time", return_value=1011):
            self.assertEqual(permission_cache._cached("expiry", build), 4)
        self.assertEqual(build.call_count, 2)

    def test_default_timeout_is_used_when_setting_is_absent(self):
        with self.settings():
            del permission_cache.settings.PERMISSION_CACHE_TTL
            self.assertEqual(permission_cache._timeout(), 300)

    def test_version_eviction_does_not_reuse_old_cached_grant(self):
        with patch.object(permission_cache, "_new_token", side_effect=[101, 102]), patch.object(
            permission_cache, "_build_object_permission", side_effect=[(4, False), (-1, False)]
        ):
            self.assertEqual(permission_cache.get_object_permission(self.user, "project", 2), (4, False))
            cache.delete(permission_cache._VERSION_KEY)
            self.assertEqual(permission_cache.get_object_permission(self.user, "project", 2), (None, False))

    def test_concurrent_version_initialization_uses_winning_token(self):
        with patch.object(permission_cache.cache, "get", side_effect=[None, 42]), patch.object(
            permission_cache.cache, "add", return_value=False
        ):
            self.assertEqual(permission_cache._get_version(), 42)

    def test_backend_that_does_not_store_versions_still_returns_a_token(self):
        with patch.object(permission_cache.cache, "get", return_value=None), patch.object(
            permission_cache.cache, "add", return_value=False
        ), patch.object(permission_cache, "_new_token", side_effect=[41, 42]):
            self.assertEqual(permission_cache._get_version(), 42)

    def test_invalidation_repeats_after_commit_to_discard_racing_reads(self):
        build = Mock(side_effect=[4, 3, 0])
        with patch.object(permission_cache, "_new_token", side_effect=[101, 102, 103]), patch.object(
            permission_cache.transaction, "on_commit"
        ) as on_commit:
            self.assertEqual(permission_cache._cached("race", build), 4)
            permission_cache.bump_permission_version()
            self.assertEqual(permission_cache._cached("race", build), 3)
            on_commit.assert_called_once()
            on_commit.call_args.args[0]()
            self.assertEqual(permission_cache._cached("race", build), 0)
        self.assertEqual(build.call_count, 3)

    def test_only_assignments_with_a_group_trigger_signal_invalidation(self):
        with patch.object(permission_cache, "bump_permission_version") as bump:
            permission_cache._bump_for_group_access(SimpleNamespace(group_id=None))
            bump.assert_not_called()
            permission_cache._bump_for_group_access(SimpleNamespace(group_id=2))
            bump.assert_called_once_with()

    def test_destination_cache_separates_user_destination_and_object_lookup(self):
        with patch.object(permission_cache.UserGroup.objects, "filter") as query:
            query.return_value.aggregate.side_effect = [
                {"permission_set__project__max": 1}, {"permission_set__project__max": 4}, {"permission_set__task__max": 2},
            ]
            lookups = [(self.user, "project"), (SimpleNamespace(pk=13, is_authenticated=True), "project"), (self.user, "task")]
            for _ in range(2):
                for lookup, expected in zip(lookups, (1, 4, 2)):
                    self.assertEqual(permission_cache.get_destination_permission(*lookup), expected)
            self.assertEqual(query.call_count, 3)
        with patch.object(permission_cache, "_build_object_permission", return_value=(-1, False)):
            self.assertEqual(permission_cache.get_object_permission(self.user, "project", 2), (None, False))

    def test_destination_denials_and_zero_levels_are_cached(self):
        for level in (None, 0):
            cache.clear()
            with self.subTest(level=level), patch.object(permission_cache.UserGroup.objects, "filter") as query:
                query.return_value.aggregate.return_value = {"permission_set__project__max": level}
                for _ in range(2):
                    self.assertEqual(permission_cache.get_destination_permission(self.user, "project"), level)
                query.assert_called_once_with(is_deleted=False, username=self.user)

    def test_destination_cache_is_bypassed_for_unsaved_and_anonymous_users(self):
        for user in (SimpleNamespace(pk=None, is_authenticated=True), SimpleNamespace(pk=12, is_authenticated=False)):
            with self.subTest(user=user), patch.object(permission_cache.UserGroup.objects, "filter") as query:
                query.return_value.aggregate.side_effect = [{"permission_set__project__max": 4}, {"permission_set__project__max": None}]
                self.assertEqual(permission_cache.get_destination_permission(user, "project"), 4)
                self.assertIsNone(permission_cache.get_destination_permission(user, "project"))
                self.assertEqual(query.call_count, 2)

    def test_destination_cache_can_be_disabled(self):
        with override_settings(PERMISSION_CACHE_TTL=0), patch.object(permission_cache.UserGroup.objects, "filter") as query:
            query.return_value.aggregate.side_effect = [{"permission_set__project__max": 4}, {"permission_set__project__max": 0}]
            self.assertEqual(permission_cache.get_destination_permission(self.user, "project"), 4)
            self.assertEqual(permission_cache.get_destination_permission(self.user, "project"), 0)
