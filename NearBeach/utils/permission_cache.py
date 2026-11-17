"""Cache for the permission lookups done by the permission decorators

`@object_permission` and `@destination_permission` ask the database "what is this user's level on this object" on
every request. Permissions change rarely, so the answer is cached.

Invalidation uses a version token. Every cache key contains the current token; changing anything that could change
an answer (a UserGroup, PermissionSet, Group or the group rows of ObjectAssignment) replaces the token, which orphans
every cached answer at once. The token is a unique value rather than a counter so that, if the cache evicts it, the
next token can never collide with one that older entries were written under.

The default Django cache is per process: with several workers another worker keeps serving the old answer until
`PERMISSION_CACHE_TTL` runs out. Point `CACHES` at a shared backend (Redis - see `REDIS_URL` in the settings) for
instant invalidation. Set `PERMISSION_CACHE_TTL = 0` to switch caching off.
"""
import time
from typing import Any, Optional, Tuple

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import Max
from django.db.models.signals import post_delete, post_save

from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.permission.permission_set import PermissionSet
from NearBeach.models.user import UserGroup

DEFAULT_TIMEOUT_SECONDS = 300
_VERSION_KEY = "nearbeach_permission_version"
_KEY_PREFIX = "nearbeach_permission"
# Stored in place of None, as the cache cannot tell "cached None" from "not cached"
_DENIED = -1


def _timeout() -> int:
    return int(getattr(settings, "PERMISSION_CACHE_TTL", DEFAULT_TIMEOUT_SECONDS))


def _new_token() -> int:
    return time.time_ns()


def _get_version() -> int:
    version: Optional[int] = cache.get(_VERSION_KEY)
    if version is None:
        # add() so two workers starting together agree on one token
        cache.add(_VERSION_KEY, _new_token(), None)
        version = cache.get(_VERSION_KEY)
    return version if version is not None else _new_token()


def bump_permission_version(*_: Any, **__: Any) -> None:
    """Throw away every cached permission answer - also usable as a signal handler"""
    cache.set(_VERSION_KEY, _new_token(), None)

    # A request that starts after this bump but before the change commits would cache the old answer under the new
    # token, so bump again once the surrounding transaction has committed (runs at once in autocommit)
    transaction.on_commit(lambda: cache.set(_VERSION_KEY, _new_token(), None))


def _cached(key_parts: str, build: Any) -> Any:
    timeout = _timeout()
    if timeout <= 0:
        return build()

    key = f"{_KEY_PREFIX}:{_get_version()}:{key_parts}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    value = build()
    cache.set(key, value, timeout)
    return value


def _user_key(user: Any) -> Optional[int]:
    """The user's id, or None when the user should not be cached (anonymous / unsaved)"""
    if not getattr(user, "is_authenticated", False):
        return None
    return getattr(user, "pk", None)


def _build_object_permission(
    user: Any,
    destination: str,
    location_id: int,
    additive_permission: Optional[str],
) -> Tuple[int, bool]:
    user_group_results = UserGroup.objects.filter(
        is_deleted=False,
        permission_set__is_deleted=False,
        username=user,
    )

    # Organisation is exempt from the group filter
    if destination != "organisation":
        user_group_results = user_group_results.filter(
            group_id__in=ObjectAssignment.objects.filter(
                is_deleted=False,
                group_id__isnull=False,
                **{destination: location_id},
            ).values("group_id")
        )

    # The aggregate is None when the user has no matching group
    user_level = user_group_results.aggregate(
        Max(f"permission_set__{destination}")
    )[f"permission_set__{destination}__max"]
    if user_level is None:
        return _DENIED, False

    # The additive permission has to come from the same permission set that lets the user read the object
    has_additive_permission = additive_permission is not None and user_group_results.filter(
        permission_set__is_deleted=False,
        **{
            f"permission_set__{destination}__gte": 1,
            f"permission_set__{additive_permission}__gte": 1,
        },
    ).exists()

    return int(user_level), bool(has_additive_permission)


def get_object_permission(
    user: Any,
    destination: str,
    location_id: int,
    additive_permission: Optional[str] = None,
) -> Tuple[Optional[int], bool]:
    """Return (user level, has additive permission) for an object. The level is None when the user has no access"""
    user_pk = _user_key(user)

    def build() -> Tuple[int, bool]:
        return _build_object_permission(user, destination, location_id, additive_permission)

    if user_pk is None:
        level, additive = build()
    else:
        level, additive = _cached(
            f"object:{user_pk}:{destination}:{location_id}:{additive_permission}",
            build,
        )
    return (None if level == _DENIED else level), additive


def get_destination_permission(user: Any, destination: str) -> Optional[int]:
    """Return the user's highest level for a permission set field, or None when they have no group"""
    user_pk = _user_key(user)

    def build() -> int:
        level = UserGroup.objects.filter(
            is_deleted=False,
            username=user,
        ).aggregate(
            Max(f"permission_set__{destination}")
        )[f"permission_set__{destination}__max"]
        return _DENIED if level is None else int(level)

    level = build() if user_pk is None else _cached(f"destination:{user_pk}:{destination}", build)
    return None if level == _DENIED else level


def _bump_for_group_access(instance: ObjectAssignment, **_: Any) -> None:
    """Only rows that grant a group access to an object can change a permission answer"""
    if instance.group_id is not None:
        bump_permission_version()


for _model in (UserGroup, PermissionSet):
    post_save.connect(bump_permission_version, sender=_model, weak=False, dispatch_uid=f"perm_cache_save_{_model.__name__}")
    post_delete.connect(bump_permission_version, sender=_model, weak=False, dispatch_uid=f"perm_cache_delete_{_model.__name__}")

post_save.connect(_bump_for_group_access, sender=ObjectAssignment, weak=False, dispatch_uid="perm_cache_save_ObjectAssignment")
post_delete.connect(_bump_for_group_access, sender=ObjectAssignment, weak=False, dispatch_uid="perm_cache_delete_ObjectAssignment")
