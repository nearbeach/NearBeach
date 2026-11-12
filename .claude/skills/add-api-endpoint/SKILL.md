---
name: add-api-endpoint
description: Add or extend a NearBeach REST endpoint (viewset action + permission decorator + service + serializer + OpenAPI docs + role tests). Use when asked to add an API route for an existing object.
---

# Add an API endpoint

Reference implementation: `NearBeach/views/api_v1/project_api_view.py`, `services/ProjectService.py`, `serializers/project_serializer.py`, `api_docs/api_v1/project_docs.py`.

1. **Decide the permission.** ID in URL -> `@object_permission(min_permission_level=N)`; creating -> `@destination_permission(min_permission_level=N)`. Levels: 1 read, 2 edit, 3 add, 4 full. Add `additive_permission="<x>_note"` for notes/docs/tags.
2. **Serializer** in `NearBeach/serializers/`. Validate group lists with `check_group_list`.
3. **Service** in `NearBeach/services/` (subclass `ObjectServiceAbstraction`; PascalCase file name). Return `(data, http_status)`. Filter `is_deleted=False`; soft delete only. Fully type-annotate.
4. **ViewSet action** in `views/api_v1/<object>_api_view.py`: decorator stack (permission above `@action`), instantiate `Service(destination="<object>", location_id=pk)`, return `Response(data=data, status=http_status)`.
5. **Routing:** public viewsets register in `NearBeach/urls/api_public.py` (`SimpleRouter`); internal paths in `api_internal.py`.
6. **OpenAPI:** add/update the `XXX_SCHEMA` in `NearBeach/api_docs/api_v1/` and keep `@apply_schema` on the viewset; refresh `schema.yml` if the project does so.
7. **Tests:** one file per role in each folder of `NearBeach/tests/tests_api/test_permissions/` (`test_admin`, `test_no_group`, `test_no_log_in`, `test_no_permission`, `test_read_only`, `test_team_intern`, `test_team_leader`, `test_team_member`) using `BaseApiClass` + `URLTest` tables. Add service tests under `tests_services/`.
8. **Verify:** `python3 manage.py test`, `mypy NearBeach`. If the frontend consumes it, add the Vue call via `safeFetch` and i18n keys in both locale files.
