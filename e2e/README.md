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
## Accessibility tests

`test_accessibility.py` runs axe-core (via `axe-playwright-python`) against the
dashboard, project search/new and the project details tabs. Known issues from
`A11Y_REPORT.md` are listed in `KNOWN_ISSUES` / marked `xfail(strict=True)`, so
the suite fails when a new violation appears and also when a known one is fixed
(remove it from the list then).

```bash
DJANGO_ALLOW_ASYNC_UNSAFE=true python -m pytest -c e2e/pytest.ini e2e/test_accessibility.py -v
```
