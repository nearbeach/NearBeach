# Python E2E tests

Uses pytest, pytest-django, and Playwright to verify project creation
and persistence of the title and selected group after a page reload.

## Setup

From the repository root, with your virtual environment activated:

```bash
python -m pip install -r requirements-e2e.txt
python -m playwright install chromium
npm install
```

## Run

Start Vite in a separate terminal:

```bash
npm run dev -- --host localhost --port 5173 --strictPort
```

Run the test:

```bash
DJANGO_ALLOW_ASYNC_UNSAFE=true python -m pytest -c e2e/pytest.ini e2e/test_project_creation.py --headed -v
```

Django starts automatically. Fixtures prepare the user, group, permissions,
session, and CSRF cookie in an isolated SQLite test database.
No real credentials or separate `runserver` process are needed.

`DJANGO_ALLOW_ASYNC_UNSAFE` disables Django's async-safety guard to allow
synchronous ORM calls while Playwright's event loop is running.
Keep it scoped to this sequential test command, not production.

## Debugging

Add these options to the test command to retain a trace on failure:

```bash
--tracing retain-on-failure --output test-results
```

Find the resulting archive:

```bash
find test-results -name trace.zip
```

Open it using the returned path:

```bash
python -m playwright show-trace "test-results/<test-folder>/trace.zip"
```

## Status

Five consecutive local runs passed on macOS with Chromium and Vite.
Earlier intermittent authentication failures were observed; their cause
was not confirmed.
CI and production-build execution have not been verified.