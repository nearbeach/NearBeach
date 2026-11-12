# Backend tests

- Run all: `python3 manage.py test`. One module: `python3 manage.py test NearBeach.tests.tests_api.test_permissions.test_admin`.
- Base class: `utils/BaseApiClass.py` (`APITestCase`). Set `username` / `password` on the subclass; `setUp` clears cache, disables auth throttling and logs in. Look at an existing permission test for the seed credentials rather than copying them elsewhere.
- Table-driven permission tests: build a list of `self.URLTest(url, data, expected_status, method)` and loop over it. Pattern: `tests_api/test_permissions/test_admin/test_api_permissions_admin_project.py`.
- Fixtures: `NearBeach_basic_setup.json` (default), `NearBeach_no_setup.json`, `NearBeach_gdpr_setup.json` in `NearBeach/fixtures/`. Fixture conventions: `docs/007-misc/fixtures/`. If you change models, update the fixtures.
- Role folders under `tests_api/test_permissions/`: `test_admin`, `test_no_group`, `test_no_log_in`, `test_no_permission`, `test_read_only`, `test_team_intern`, `test_team_leader`, `test_team_member`. A new endpoint needs a file in **each**, named like `test_api_permissions_<role>_<object>.py` (existing names are not fully consistent, e.g. `test_api_permissions_team_no_permission_project.py`; match the neighbours). `tests_crud/` also holds `test_list_query_counts.py`.
- Other suites: `tests_crud`, `tests_projects`, `tests_authentication` (login, 2FA, throttling, OAuth2, OIDC), `tests_schema`, `tests_services`, `tests_views`, `tests_file_handlers`.
- Admin tests expect 404 for a non-existent object id; check neighbouring role tests before asserting 403 vs 404 for inaccessible objects.
