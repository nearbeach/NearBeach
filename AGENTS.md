# NearBeach – agent context

NearBeach is an open-source project management system (Organisations, Customers, Projects, Tasks, Requirements, Kanban, Request for Change, Sprints). Django + DRF backend, Vue 3 + TypeScript + Pinia + Vite frontend.

**Read `Architecture.md` before making structural changes.** It is the source of truth for how the parts connect.

## Status: mid-rewrite (branch `0.32-development`)
Only Organisation, Project, Customer and Public Link are on the new stack (viewset + service + Vue/Pinia). Other objects have models/fixtures only. Do not copy patterns from `__pycache__` leftovers or old docs mentioning Webpack.

## Map
- `NearBeach/` Django app: `models/`, `serializers/`, `services/`, `views/api_v1/`, `urls/`, `decorators/check_user_permissions/`, `tests/`
- `src/` Vue app: `components/<feature>/`, `stores/`, `composables/`, `locales/`
- `local/` dev settings + `ROOT_URLCONF`; `e2e/` Playwright; `docs/` Sphinx

## Commands
```
source venv/bin/activate
python3 manage.py test                 # backend tests
python3 manage.py runserver            # :8000
npm run dev                            # Vite :5173 (needed alongside Django)
npm run test:unit | type-check | lint | format
mypy NearBeach
```

## Rules
1. Filter `is_deleted=False` on every queryset (soft delete via `CommonInfo`).
2. Object-to-object links, assignments and group access all live in `ObjectAssignment` (wide nullable-FK table, not GenericFK).
3. API flow: ViewSet -> `@object_permission`/`@destination_permission` -> Service (`ObjectServiceAbstraction`, returns `(data, status)`) -> Serializer, documented with `@apply_schema`.
4. Enforce permissions server-side. New endpoints need tests for every role folder in `NearBeach/tests/tests_api/test_permissions/`.
5. Type-annotate new models/services (mypy `disallow_untyped_defs`).
6. Every user-facing string goes in both `src/locales/en.json` and `ja.json`.
7. Never use real SMTP/S3 credentials from `.env`; never commit `db.sqlite3` changes. For manual testing use a wrapped settings module (console email backend, nulled S3/Azure keys).
8. Git flow: features from `develop`, hotfixes from `main`. Don't commit unless asked.
