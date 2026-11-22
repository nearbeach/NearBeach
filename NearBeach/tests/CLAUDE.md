# Backend tests

- Run all: `python3 manage.py test`. One module: `python3 manage.py test NearBeach.tests.tests_api.test_permissions.test_admin`.
- Base class: `utils/BaseApiClass.py` (`APITestCase`). Set `username` / `password` on the subclass; `setUp` clears cache, disables auth throttling and logs in. Look at an existing permission test for the seed credentials rather than copying them elsewhere.
- Table-driven permission tests: build a list of `self.URLTest(url, data, expected_status, method)` and loop over it. Pattern: `tests_api/test_permissions/test_admin/test_api_permissions_admin_project.py`.
- Fixtures: `NearBeach_basic_setup.json` (default), `NearBeach_no_setup.json`, `NearBeach_gdpr_setup.json` in `NearBeach/fixtures/`. Fixture conventions: `docs/007-misc/fixtures/`. If you change models, update the fixtures.
- Role folders under `tests_api/test_permissions/`: `test_admin`, `test_no_group`, `test_no_log_in`, `test_no_permission`, `test_read_only`, `test_team_intern`, `test_team_leader`, `test_team_member`. A new endpoint needs a file in **each**, named like `test_api_permissions_<role>_<object>.py` (existing names are not fully consistent, e.g. `test_api_permissions_team_no_permission_project.py`; match the neighbours). `tests_crud/` also holds `test_list_query_counts.py`.
- Other suites: `tests_crud`, `tests_projects`, `tests_authentication` (login, 2FA, throttling, OAuth2, OIDC), `tests_schema`, `tests_services`, `tests_views`, `tests_file_handlers`.
- Admin tests expect 404 for a non-existent object id; check neighbouring role tests before asserting 403 vs 404 for inaccessible objects.

## Choosing a test type
| Testing | Base class | Example |
|---|---|---|
| Endpoint + permissions per role | `BaseApiClass` | `tests_api/test_permissions/test_admin/` |
| Endpoint behaviour (data effects, audit, meta_data, query counts) | `BaseApiClass` | `tests_api/tests_crud/test_audit_log.py`, `test_list_query_counts.py` |
| Service called directly, no route yet or logic-focused | `django.test.TestCase` | `tests_services/test_unrouted_services.py` |
| Pure helper, no database | `SimpleTestCase` | `tests_services/test_audit_service.py` (`AuditSnapshotTests`) |

## Test data and credentials
- `BaseApiClass` loads `NearBeach_basic_setup.json`; tests run in a transaction that is rolled back, so create what you need and don't clean up. Rolled-back data fires no cache-invalidating signals, which is why `setUp` clears the cache.
- Seed users (`admin`, `team_leader`, ...) and their test passwords are in the fixture and in the existing role tests (see `tests_api/test_permissions/test_admin/`); they are fixture-only values. Don't invent users or put real credentials in tests. Don't repeat them in docs, commits or chat.
- Put the fixture ids a test relies on in the module docstring (see `test_audit_log.py`: "projects 1 and 2, status 6 is Closed"). If a new object needs fixture rows, extend `NearBeach_basic_setup.json` and follow `docs/007-misc/fixtures/`; check that existing tests (counts, list lengths) still pass.
- To create extra rows, copy an existing fixture row (`project.pk = None; project.save()`) or use `Model.objects.create(...)` in `setUp`.

## Service tests
Services return `(data, status)`, so call them directly with a stand-in request: `SimpleNamespace(data=..., user=User.objects.get(username="admin"), method="POST")` and `Service(destination="organisation", location_id=1)` (see `ServiceTestBase` in `tests_services/test_unrouted_services.py`). Assert on both values.

Each service needs tests for: create, update (and that no second row appears), delete (soft: `is_deleted=True`, row still exists), invalid input (400 and nothing saved; use `subTest` per bad input), unknown or already-deleted id (404), list filters/ordering/search, and **an audit row** (Rule 8): `AuditLog.objects.filter(object_type="<destination>", object_id=...)` has the right `action`, only the changed fields in `changes`, and a no-op update writes none. Querysets must exclude `is_deleted=True` rows; add a case with a soft-deleted object.

## Writing endpoint tests
- Permission tables assert status only; put behaviour assertions in `tests_crud`.
- Use `self.client.patch(url, data, format="json")` for JSON bodies.
- List endpoints: add a query-count test (count must not grow with rows) like `test_list_query_counts.py`.
- Name test methods for the behaviour (`test_closing_a_project_is_recorded_as_a_close`), not the function.
- Before finishing: `python3 manage.py test <your module>`, then the full `python3 manage.py test`, then `mypy NearBeach` (tests themselves are not type-checked).
