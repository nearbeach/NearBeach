# NearBeach Architecture

This document explains how NearBeach is structured so that new contributors can quickly understand how the parts of the system fit together and where to find things in the codebase.

If you are completely new to the project, start with the README for context, then come back here for a deeper architectural overview.

- Project homepage: https://nearbeach.org
- Documentation: https://nearbeach.readthedocs.io
- Community/Support: https://discord.gg/64uhRztS6n


## High-level overview

NearBeach is an open source project management system.

- Backend: Django (Python)
  - Provides server‑rendered pages and a JSON API used by the frontend.
  - Uses Django ORM for database access
  - Uses Django for authentication handling
- Frontend: Vue.js (Single File Components, SFCs)
  - Compiled via Webpack; served as static assets by Django.
  - Talks to the backend using REST‑style JSON APIs.
- Database: Configured via Django ORM (SQLite for development by default, others in production).
- Tests and tooling: Python tests with pytest/Django test runner under tests/, end‑to‑end tooling available (Playwright), frontend tests with Vitest. Load testing with locust.


## Repository layout (top level)

- NearBeach/ — Django project and application code (models, serializers, views, URLs, templates, static, migrations, etc.).
- src/ — Frontend source (Vue components, JS entry points, styles). Bundled with Webpack.
- NearBeach/tests - Tests for backend
- tests/ Tests for frontend.
- docs/ — Documentation sources (Sphinx/readthedocs).
- swagger/ — API specification and assets related to API description.
- node_modules/, package.json, webpack.*.js, vitest.config.js — Frontend build and test tooling.
- pyproject.toml, requirements*.txt — Python packaging and dependencies.
- manage.py — Django management entry point.
- db.sqlite3 — Default local development database (do not commit changes from production use).
- browserstack/, playwright.config.ts, locust_tests/ — Testing and QA tooling.


## Django backend structure (NearBeach/)

Key paths inside NearBeach/ (only representative highlights listed):

- NearBeach/apps.py — Django app configuration.
- NearBeach/urls_two_factor.py — URL routes for optional two‑factor authentication flows.
- NearBeach/migrations/ — Database schema migrations (managed by Django).
- NearBeach/serializers/ — DRF‑style serializers used by API viewsets and endpoints.
  - Example: NearBeach/serializers/destination_serializer.py
- NearBeach/views/ — View modules for pages and APIs. Notable sub-areas:
  - NearBeach/views/api/ — JSON API endpoints grouped by domains (e.g., sprint_api_view.py, coffee_api_view.py, object_data/link_api_view.py, available_data/*_list_api_view.py, etc.).
  - NearBeach/views/authentication/ — Login/2FA and related UI views.
  - Other domain views: admin_views.py, sprint_views.py, card_views.py, change_task_views.py, customer_views.py, document_views.py, gdpr_wizard_views.py, etc.
- NearBeach/static/ — Static assets collected and served by Django (vendored libraries, icons, TinyMCE, etc.).
- NearBeach/templates/ — Django templates for server-rendered pages (if present).

Typical backend layering
- URL routing: Configured in project urls (and urls_two_factor.py for 2FA). Each domain area has URL patterns pointing to function-based views, class-based views, or DRF ViewSets.
- Views and APIs:
  - Server-rendered views return HTML templates and embed frontend entrypoints for Vue where appropriate.
  - API endpoints (in views/api) return JSON responses and accept JSON bodies. Patterns commonly use Django REST Framework style ViewSets or function-based views with @require_http_methods.
- Serializers:
  - Define how model instances are converted to/from JSON payloads for the API.
  - Live under NearBeach/serializers/ and are imported by API views.
- Models:
  - Django ORM models define persistent data. Migrations in NearBeach/migrations/ track schema changes.
- Permissions and authentication:
  - Authentication uses Django’s auth. 2FA support is routed via urls_two_factor.py and views under views/authentication/.
  - Many views implement permission checks with helper utilities (e.g., get_user_group_permission) and per‑object gating.


## Vue frontend structure (src/)

- src/js/app.js — Main frontend entry that registers and bootstraps Vue components for pages.
- src/js/components.js — Central index of components for lazy/explicit imports.
- src/js/components/** — Vue Single File Components (SFCs) grouped by feature domain.
  - Administration: src/js/components/administration/*.vue
  - Change/Task: src/js/components/change_task/*.vue
  - Cards/Kanban: src/js/components/card_information/*.vue, src/js/components/kanban/*.vue
  - Users: src/js/components/users/*.vue
  - Icons and shared UI: src/js/components/icons/*.vue
- State management: The project primarily composes state within components and passes props/events between them. If a global store is in use, it will be initialized from app.js; otherwise look for composables or shared modules by domain.
- Validation/UI libraries: Vuelidate is used for form validation; Bootstrap is used for CSS layout. TinyMCE is used for rich text editing.

Build output
- Webpack bundles the Vue SFCs into static assets that Django serves from its static files pipeline.
- The webpack.*.js files define common, dev, prod, and watch configurations.


## API and data flow

- Most user interactions in the UI trigger API calls to endpoints under NearBeach/views/api/.
- Serialization: Requests/Responses are validated and shaped by serializers (NearBeach/serializers/*).
- Permissions are checked server-side; the frontend should not rely solely on UI hiding.
- Common patterns:
  - ViewSets for list/detail actions (e.g., CustomerListViewSet, SprintListViewSet).
  - Domain-specific API modules (e.g., sprint_api_view.py) expose endpoints for the corresponding Vue components (e.g., Sprint boards, modules).

Example paths (non-exhaustive):
- NearBeach/views/api/sprint_api_view.py — Sprint-related JSON endpoints.
- NearBeach/views/api/object_data/link_api_view.py — Linking objects (relations) endpoints.
- NearBeach/views/api/coffee_api_view.py — Example/testing endpoints.


## Authentication, authorization, and security

- Authentication via Django’s session auth; the login/2FA views reside under NearBeach/views/authentication/ and urls_two_factor.py wires routes to the two_factor app.
- CSRF protection is enabled for session-authenticated POST/PUT/PATCH/DELETE by default in Django. Frontend must send CSRF tokens (usually embedded in templates or fetched via a CSRF endpoint).
- Authorization per feature/object is enforced in view functions using helper permission checks (see views/* importing get_user_group_permission and similar helpers). Always validate server-side.


## Testing

- Backend tests: Python tests under tests/ and NearBeach/tests/ where applicable.
  - Example: NearBeach/tests/tests_specific_user_functionality/test_admin_user_settings.py
- Frontend unit tests: Vitest with configuration in vitest.config.js.
- E2E/Browser: Playwright config in playwright.config.ts. BrowserStack config available in browserstack/.
- Load testing: locust tests under locust_tests/.

To run backend tests locally:
- python manage.py test
- Or with pytest if configured via pyproject.toml

To run frontend unit tests:
- npm run test


## Development workflow

- Python environment
  - Install dependencies from requirements.txt or requirements-dev.txt.
  - Use manage.py for running the server, migrations, creating superusers, etc.
- Frontend environment
  - Install Node dependencies via npm ci or npm install.
  - Run Webpack in watch/dev mode with npm scripts (see package.json) and webpack.dev.js.
  - Production bundles use webpack.prod.js.

Static files and assets
- Run Django collectstatic as part of deployment to gather bundled assets into the static root.


## Adding features (typical steps)

1) Backend
- Add/modify models in NearBeach/models.py or domain-specific modules and create migrations.
- Add/extend serializers in NearBeach/serializers/.
- Implement API views in NearBeach/views/api/ and add URL routes.
- Add permission checks as required.

2) Frontend
- Build or extend Vue components under src/js/components/<domain>/.
- Wire components in src/js/app.js or feature entry points.
- Call the new API endpoints and handle responses with appropriate validation and error states.

3) Tests
- Add/extend backend unit tests in tests/ or NearBeach/tests/.
- Add/extend frontend tests with Vitest.
- Update any E2E scenarios if user flows change.


## Conventions and guidelines

- Python: Follow PEP 8; keep views small and delegate serialization/validation to serializers.
- Vue: Prefer small, focused SFCs; lift shared logic into reusable components. Use Vuelidate for forms, Bootstrap for layout.
- API: Keep endpoints REST‑like; provide clear 4xx/5xx error responses with helpful detail; document in swagger/ when applicable.
- Security: Validate every server-side input; enforce object-level permissions in views; keep CSRF headers/tokens in place for state‑changing requests.
- Performance: Use pagination for list endpoints; minimize N+1 queries via select_related/prefetch_related; prefer incremental rendering on the frontend.


## Where to look for specific topics

- URL routing: NearBeach/urls_two_factor.py and the project’s main urls module.
- Authentication and 2FA: NearBeach/views/authentication/* and urls_two_factor.py (routes into two_factor.views and project-specific wrappers).
- Serializers: NearBeach/serializers/*
- API endpoints: NearBeach/views/api/*
- Feature views (HTML + Vue mount points): NearBeach/views/*_views.py
- Vue components: src/js/components/**
- Webpack configuration: webpack.common.js, webpack.dev.js, webpack.prod.js, webpack.watch.js
- Frontend entry: src/js/app.js and src/js/components.js
- Tests: tests/, NearBeach/tests/, locust_tests/


## Deployment notes (summary)

- Build frontend assets with npm run build (production) to generate minified bundles.
- Run Django migrations and collectstatic.
- Configure environment variables for database, secret key, allowed hosts, email, and any integrations.
- Serve with a production WSGI server (e.g., gunicorn/uwsgi) behind a reverse proxy; serve static files from a CDN or web server.


## Appendix: Example files referenced in recent work

- Backend views (examples):
  - NearBeach/views/object_data_views.py
  - NearBeach/views/api/object_data/link_api_view.py
  - NearBeach/views/api/coffee_api_view.py
  - NearBeach/views/sprint_views.py
  - NearBeach/views/api/sprint_api_view.py
  - NearBeach/views/gdpr_wizard_views.py
- Serializers:
  - NearBeach/serializers/destination_serializer.py
- Frontend components:
  - src/js/components/users/UserApiList.vue
  - src/js/components/change_task/ChangeTaskModules.vue
  - src/js/components/administration/UserList.vue

This document is intentionally high level. If you discover discrepancies or have suggestions, please open a PR to update Architecture.md or the docs in docs/.