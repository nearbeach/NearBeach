# NearBeach Architecture

How NearBeach is put together, for human contributors and AI coding agents. This is the single source of truth for the system map; `AGENTS.md` and `CLAUDE.md` summarise it and link here.

- Homepage: https://nearbeach.org
- Docs: https://nearbeach.readthedocs.io
- Community: https://discord.gg/64uhRztS6n

> **Rewrite in progress (branch `0.32-development`).** The frontend moved from Webpack/Vue to Vite + Vue 3 + TypeScript + Pinia, and the backend is moving from function views to DRF viewsets + a service layer. Only **Organisation, Project, Customer and Public Link** are fully on the new stack. Do not assume other objects (Task, Requirement, Kanban, RFC, Sprint) have API endpoints, services or Vue components yet; their models and fixtures exist.

## 1. Stack at a glance

| Layer | Technology |
|---|---|
| Backend | Django 6, Django REST Framework, drf-spectacular (OpenAPI) |
| Auth | Django sessions, django-rest-knox tokens, django-oauth-toolkit (OAuth2), django_otp (2FA), authlib (OIDC SSO) |
| Frontend | Vue 3, vue-router, Pinia, TypeScript, petite-vue-i18n, Vite + django-vite |
| DB | SQLite in dev; MariaDB/MySQL/PostgreSQL/Oracle in production |
| Files | Local, AWS S3 or Azure Blob (`NearBeach/utils/private_media.py`) |
| Tests | Django `APITestCase`, Vitest, Playwright (Python e2e), schemathesis |

## 2. Repository layout

- `NearBeach/` – the single Django app (`NearBeach.apps.NearBeachConfig`)
- `local/` – dev project config: `settings.py`, `urls.py` (`ROOT_URLCONF`), `settings_schemathesis.py`
- `src/` – Vue 3 + TS frontend (entry points `src/main.ts`, `src/login.ts`)
- `e2e/` – Python Playwright tests (need Vite running); see `e2e/README.md`
- `docs/` – Sphinx / Read the Docs manual (RST, numbered folders)
- `swagger/`, `schema.yml` – OpenAPI artefacts
- `scripts/` – benchmarks, locale extraction, schemathesis runner
- `vite.config.ts` – builds to `NearBeach/static/NearBeach/` (`js/[name]-bundle.js`, `css/[name].css`, `manifest.json`)

## 3. Backend (`NearBeach/`)

```
models/      domain tables, split per area
serializers/ DRF serializers (+ available_data, object_data, user, ...)
services/    business logic; one Service class per object
views/       api_v1/ (viewsets), application/, authentication/, private_document/, public_link/, search/
urls/        base.py, api_public.py, api_internal.py, oauth2.py
decorators/  check_user_permissions/ (object_permission, destination_permission)
utils/       enums/, api/ helpers, dicts/, throttle/, oauth2/
api_docs/    drf-spectacular schema constants (XXX_SCHEMA) + @apply_schema
tests/       tests_api, tests_services, tests_views, ...
```

### Models
Every model extends `CommonInfo` (`models/abstraction/common_abstractions.py`): `date_created`, `date_modified`, `creation_user`, `change_user` and a soft-delete flag **`is_deleted`**. Querysets must filter `is_deleted=False`. Primary keys are explicit `BigAutoField`. Enums are `IntegerChoices`/`TextChoices` in `utils/enums/` with `gettext_lazy` labels.

Domain areas: Organisation, Customer, Project, Task, Requirement + RequirementItem, RequestForChange + ChangeTask, KanbanBoard + KanbanCard, Sprint, Document/Folder, Note, Tag, Group/PermissionSet/UserGroup, OIDC provider.

### How objects are tied together: `ObjectAssignment`
`models/object_assignment/object_assignment.py` is **one wide table with nullable FKs** to every object type plus `assigned_user` and `group`. It is *not* a Django GenericForeignKey. A row means one of:

1. **Group access**: `group` + one object FK. The group may access the object.
2. **User assignment**: `assigned_user` + one object FK.
3. **Object link**: object FK + `meta_object`, `meta_object_title`, `meta_object_status`, `link_relationship` (block / duplicate / relate / subobject) + `parent_link`.

Fixture conventions: `docs/007-misc/fixtures/fixture-object-assignment.rst`.

### Permissions
- A user belongs to groups via `UserGroup`; each row carries a `PermissionSet`.
- `PermissionSet` holds one integer per area (project, task, requirement, kanban_board, request_for_change, customer, organisation, sprint, document, tag, `administration_*`) using `PermissionLevel`: 0 none, 1 read, 2 edit, 3 add+edit, 4 full.
- Additive permissions (`project_note`, `task_note`, `kanban_note`, ...) extend the base level.
- **Effective access = ObjectAssignment group access ∩ PermissionSet level.** Organisation is exempt from the group filter.
- Child objects (card, change task, ...) resolve to their parent via `utils/api/get_parent_object.py`; `utils/api/object_to_permission_set_mapping.py` maps a destination name to a `PermissionSet` field.
- Enforced with decorators in `decorators/check_user_permissions/`:
  - `@object_permission(min_permission_level=N, additive_permission="...")` – object id is in the URL (404 if missing, `PermissionDenied` if not allowed).
  - `@destination_permission(min_permission_level=N)` – create flows, no id yet.
  - Used together with `@action`. Validate group lists with `check_group_list`.

### Request path
```
browser -> local/urls.py
  -> NearBeach/urls/base.py
       api/v1/  -> api_public.py (SimpleRouter viewsets, schema/, docs/)
                -> api_internal.py (auth, OIDC, user/initial_data/; catch-all JSON 404)
       login / logout / reset-password views
       private/<uuid>/   private documents
       public_link/<uuid>/
       <path:_>  -> ApplicationView -> templates/NearBeach/application.html -> Vue SPA
```

### Layering for an API call
```
ViewSet (views/api_v1/*_api_view.py)
  @apply_schema(X_SCHEMA)            # docs
  @object_permission / @destination_permission
  -> Service (services/XxxService.py, subclass ObjectServiceAbstraction)
        ProjectService(destination="project", location_id=pk)
  -> Serializer (serializers/...)
  <- returns (data, http_status); the view wraps it in Response
```
Rate limits for auth endpoints: `utils/throttle/` (`THROTTLE_AUTH_*` env vars). Tests disable them.

## 4. Frontend (`src/`)

- `main.ts` (app) and `login.ts` (login app); `pages/app/App.vue`, `pages/login_app`.
- `router/router.ts`, `loginRouter.ts`.
- `stores/` (Pinia): documentation, error, nav, object, object_meta_data, permissions, search, user.
- `composables/`: `safeFetch`, `getCsrfToken`, `failedValidation`, `getSafeNextUrl`, `useSsoProviders`.
- `components/<feature>/`: each component folder has `Name.vue`, `Name.spec.ts`, `index.ts`. Shared: `object_components/*`, `prefab/*`.
- i18n: `petite-vue-i18n`; `locales/en.json` is bundled, others (`ja.json`) lazy-load; page language from `<html lang>`. `scripts/extract-locales.mjs` and `locales.spec.ts` keep files in sync.
- Accessibility is first-class (`skip_links`, `styles/_accessibility.css`, axe in `e2e/test_accessibility.py`).
- Dev: Vite on :5173 alongside Django :8000 (`vite_hmr_client` / `vite_asset` template tags). Prod: `npm run build` into `NearBeach/static/NearBeach/`.

## 5. Common tasks

| Task | Command |
|---|---|
| Python env | `python3 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt` |
| DB | `python3 manage.py migrate && python3 manage.py createsuperuser` |
| Backend server | `python3 manage.py runserver` |
| Frontend dev | `npm install && npm run dev` (Node ^22.12 or ^24) |
| Backend tests | `python3 manage.py test` |
| Frontend tests | `npm run test:unit` |
| Types / lint | `npm run type-check`, `npm run lint`, `npm run format`, `mypy NearBeach` |
| E2E | `DJANGO_ALLOW_ASYNC_UNSAFE=true python -m pytest -c e2e/pytest.ini e2e/test_project_creation.py --headed -v` |
| API fuzz | `scripts/run_schemathesis.sh` |
| Docs | `cd docs && make html` |

CI: CircleCI (backend on Python 3.12, frontend on Node 23 + Vitest + Playwright) and GitHub Actions (`type-check.yml`, `schemathesis.yml`, `deploy-*.yml`).

## 6. Testing

- Base class `NearBeach/tests/utils/BaseApiClass.py`: loads `NearBeach_basic_setup.json`, clears cache, disables auth throttling.
- Other fixtures: `NearBeach_no_setup.json`, `NearBeach_gdpr_setup.json`.
- `tests_api/test_permissions/` has one folder per role: admin, no_group, no_log_in, no_permission, read_only, team_intern, team_leader, team_member. New endpoints need coverage across these roles.
- Seed users in the dev DB: `admin`, `team_leader`, `team_member`, `team_intern`, `read_only`, `read_only_extra`, `team_no_permissions`, `no_group`, `dark_admin`.
- Permission/frontend test matrices: `docs/backend_permission_test_plan.xlsx`, `docs/frontend_unit_test_plan.xlsx`.

## 7. Conventions

- Python: PEP 8, black. New models and services must be fully type-annotated (mypy `disallow_untyped_defs` there). Service files are PascalCase (`ProjectService.py`); API views `*_api_view.py`; viewsets `XxxViewSet`; schema constants `XXX_SCHEMA`; destination strings are lowercase singular (`"project"`).
- Vue: small SFCs, `<script setup lang="ts">` (nearly all components), Pinia for shared state, spec beside component.
- Every user-visible string goes through i18n in **both** `en.json` and `ja.json` (backend: `gettext_lazy as _`).
- Permissions are always enforced server-side; hiding UI is not security.
- Git flow: features branch from `develop`, hotfixes from `main` (`docs/006-procedures/git-flow`).

## 8. Known gaps and stale items

- `pyproject.toml` still says Django>=3.1 (used mainly for mypy config).
- `views/__pycache__` holds `.pyc` for deleted function views; ignore them.
- No Celery; `services/AsyncEmailService.py` is the only async piece.
- User theme/colour setting has no frontend rebuild yet.
- Root `tests/` is empty; backend tests live in `NearBeach/tests/`.
