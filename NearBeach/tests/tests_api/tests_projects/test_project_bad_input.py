"""Regression tests - bad input to the project API must give a 4xx, never a 500.

Every case here was a server error found by Schemathesis (scripts/run_schemathesis.sh).
"""

from django.urls import resolve

from NearBeach.tests.utils.BaseApiClass import BaseApiClass

PROJECT_URL = "/api/v1/project/1/"


class ProjectBadInputTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def _request(self, method, url, data=None):
        return getattr(self.client, method.lower())(url, data or {}, format="json")

    # ---------- ids in the url ----------
    def test_non_numeric_ids_are_not_found(self):
        """Sub-resource ids are numeric - anything else is a 404 from the router, not a ValueError"""
        urls = [
            ("DELETE", "customer/abc/"),
            ("DELETE", "groups/abc/"),
            ("DELETE", "link_list/abc/"),
            ("DELETE", "notes/abc/"),
            ("DELETE", "sprint/abc/"),
            ("DELETE", "users/abc/"),
            ("PATCH", "link_list/abc/"),
            ("PATCH", "notes/abc/"),
        ]
        for method, path in urls:
            with self.subTest(method=method, path=path):
                response = self._request(method, PROJECT_URL + path, {"note": "x"})
                self.assertEqual(response.status_code, 404)

    def test_non_uuid_public_link_ids_are_not_found(self):
        for method in ["PATCH", "DELETE"]:
            for bad_id in ["0", "abc", "123"]:
                with self.subTest(method=method, bad_id=bad_id):
                    response = self._request(method, f"{PROJECT_URL}public_link/{bad_id}/", {"is_active": True})
                    self.assertEqual(response.status_code, 404)

    def test_unknown_uuid_public_link_is_rejected_cleanly(self):
        response = self._request(
            "PATCH",
            f"{PROJECT_URL}public_link/00000000-0000-0000-0000-000000000000/",
            {"is_active": True},
        )
        self.assertEqual(response.status_code, 400)

    # ---------- documents ----------
    def test_document_update_is_routed_to_a_single_document(self):
        """documents_update used to be mapped onto the collection route: TypeError on /documents/, 405 on /documents/<id>/

        Only the routing is checked - DocumentService.update itself is unfinished (see its TODO).
        """
        collection = self._request("PATCH", f"{PROJECT_URL}documents/", {"type": "document", "description": "x"})
        self.assertEqual(collection.status_code, 405)

        actions = resolve(f"{PROJECT_URL}documents/1/").func.actions
        self.assertEqual(actions, {"delete": "documents_delete", "patch": "documents_update"})

    def test_document_create_without_a_file_is_rejected(self):
        response = self._request("POST", f"{PROJECT_URL}documents/", {"type": "document", "description": "x"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("document", response.data)

    def test_link_create_without_a_url_is_rejected(self):
        response = self._request("POST", f"{PROJECT_URL}documents/", {"type": "link", "description": "x"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("url_location", response.data)

    def test_folder_create_still_works_without_file_or_url(self):
        response = self._request("POST", f"{PROJECT_URL}documents/", {"type": "folder", "description": "x"})
        self.assertEqual(response.status_code, 201)

    # ---------- sprint ----------
    def test_sprint_create_needs_both_dates(self):
        cases = {
            "no dates": ({"title": "x"}, {"start_date", "end_date"}),
            "no end date": ({"title": "x", "start_date": "2026-01-01T00:00:00Z"}, {"end_date"}),
            "no start date": ({"title": "x", "end_date": "2026-02-01T00:00:00Z"}, {"start_date"}),
        }
        for name, (body, missing) in cases.items():
            with self.subTest(name):
                response = self._request("POST", f"{PROJECT_URL}sprint/", body)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(set(response.data), missing)

    def test_sprint_create_with_both_dates_works(self):
        response = self._request(
            "POST",
            f"{PROJECT_URL}sprint/",
            {"title": "x", "start_date": "2026-01-01T00:00:00Z", "end_date": "2026-02-01T00:00:00Z"},
        )
        self.assertEqual(response.status_code, 201)
