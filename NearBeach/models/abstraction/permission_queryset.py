"""QuerySet for the models that decide who may see what (UserGroup, PermissionSet, ObjectAssignment)

NearBeach soft-deletes with `queryset.update(is_deleted=True, ...)`, which never fires `post_save`. Signals alone would
leave a removed user's access sitting in the permission cache, so every bulk write here also throws the cache away.
"""
from typing import Any

from django.db import models


def _bump_permission_cache() -> None:
    # Imported here: permission_cache imports the models that use this queryset
    from NearBeach.utils.permission_cache import bump_permission_version

    bump_permission_version()


class PermissionAwareQuerySet(models.QuerySet[Any]):
    """QuerySet that clears the permission cache after any bulk write"""

    def update(self, **kwargs: Any) -> int:
        updated = super().update(**kwargs)
        _bump_permission_cache()
        return updated

    def delete(self) -> tuple[int, dict[str, int]]:
        deleted = super().delete()
        _bump_permission_cache()
        return deleted

    def bulk_create(self, objs: Any, *args: Any, **kwargs: Any) -> list[Any]:
        created = super().bulk_create(objs, *args, **kwargs)
        _bump_permission_cache()
        return created

    def bulk_update(self, objs: Any, *args: Any, **kwargs: Any) -> int:
        updated = super().bulk_update(objs, *args, **kwargs)
        _bump_permission_cache()
        return updated
