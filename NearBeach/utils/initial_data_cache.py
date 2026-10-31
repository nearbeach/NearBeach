"""Cache for the lookup data every user receives in the initial data call

Statuses, types, tags and groups are the same for every user and change rarely, so they are cached for a short time.
Saving or deleting any of them clears the cache. The default cache is per process, so with several workers another
worker can show stale data until the timeout runs out - keep the timeout short, or use a shared cache backend.
"""
from typing import Any, Callable, Iterable, List, Set

from django.core.cache import cache
from django.db.models import Model
from django.db.models.signals import post_delete, post_save

from NearBeach.models.misc.tag import Tag
from NearBeach.models.permission.group import Group
from NearBeach.models.project import ListOfProjectStatus
from NearBeach.models.requirement.requirement import ListOfRequirementStatus, ListOfRequirementType
from NearBeach.models.requirement.requirement_item import ListOfRequirementItemStatus, ListOfRequirementItemType
from NearBeach.models.task import ListOfTaskStatus

CACHE_TIMEOUT_SECONDS = 60
_KEY_PREFIX = "nearbeach_initial_data_"
_cache_keys: Set[str] = set()


def get_cached(key: str, build: Callable[[], Iterable[Any]]) -> List[Any]:
    """Return the cached list for the key, building it from the queryset on a miss"""
    _cache_keys.add(key)
    cached = cache.get_or_set(_KEY_PREFIX + key, lambda: list(build()), CACHE_TIMEOUT_SECONDS)
    return cached if cached is not None else []


def clear_initial_data_cache(*_, **__) -> None:
    """Clear every cached list - also used as the signal handler"""
    cache.delete_many([_KEY_PREFIX + key for key in _cache_keys])


_cached_models: List[type[Model]] = [
    Group,
    ListOfProjectStatus,
    ListOfRequirementItemStatus,
    ListOfRequirementItemType,
    ListOfRequirementStatus,
    ListOfRequirementType,
    ListOfTaskStatus,
    Tag,
]
for _model in _cached_models:
    post_save.connect(clear_initial_data_cache, sender=_model, weak=False)
    post_delete.connect(clear_initial_data_cache, sender=_model, weak=False)
