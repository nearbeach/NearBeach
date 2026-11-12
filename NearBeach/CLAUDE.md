# Backend (NearBeach/) conventions

See `/Architecture.md` sections 3 and 7 for the full picture. Working rules for this directory:

- **Reference implementation:** copy `views/api_v1/project_api_view.py`, `services/ProjectService.py`, `serializers/project_serializer.py` and `api_docs/api_v1/project_docs.py`. Ignore anything that only exists as `.pyc`.
- **Layering:** ViewSet methods stay thin. Permission decorator on top, then `Service(destination="<name>", location_id=pk)`, then `Response(data=data, status=http_status)`. Business logic and queries go in the service; shape/validation in the serializer.
- **Decorators:** `@object_permission(min_permission_level=N)` for anything with an id in the URL (place it above `@action`); `@destination_permission(min_permission_level=N)` for create. Levels: 1 read, 2 edit, 3 add, 4 full.
- **Queries:** always `is_deleted=False`. Prefer `Exists`/`OuterRef` over `id__in` for permission-filtered lists (see `ProjectService.get_list`; MySQL performance). Watch N+1s: `tests/tests_api/tests_crud/test_list_query_counts.py` guards this.
- **Deletes are soft:** update `is_deleted=True`, `change_user`, `date_modified`.
- **Typing:** new code in `models/` and `services/` must pass `mypy NearBeach` with `disallow_untyped_defs`.
- **Migrations:** `python3 manage.py makemigrations`, commit the generated file in `migrations/` (latest is numbered sequentially, e.g. `0055_...`). Never edit an applied migration.
- **Strings:** `from django.utils.translation import gettext_lazy as _`.
- **API docs:** every viewset gets `@apply_schema(X_SCHEMA)`; regenerate/verify `schema.yml` when endpoints change.
- **Known quirk:** `ProjectService.delete` returns a bare status code (marked TODO); don't propagate that pattern.
