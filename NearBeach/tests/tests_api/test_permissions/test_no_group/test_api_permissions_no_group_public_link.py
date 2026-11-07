from django.contrib.auth.models import User

from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoGroupPublicLinkPermissionTests(BaseApiClass):
    """A public link is readable by any logged-in user - their group and permission set do not matter"""
    username = "no_group"
    password = "Test1234$"

    # OVERRIDE - a user in no group can not log in through the api, but can still hold a session
    def _login_user(self):
        self.client.force_login(User.objects.get(username=self.username))

    def test_api_permissions_no_group_public_link(self):
        """Test - API NoGroup Permissions for the Public Link module"""
        data_list = [
            self.URLTest("/api/v1/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/", {}, 200, "GET"),
            self.URLTest("/api/v1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/", {}, 200, "GET"),
            self.URLTest("/api/v1/public_link/00000000-0000-0000-0000-000000000000/", {}, 404, "GET"),
            self.URLTest("/api/v1/public_link/not-a-uuid/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_public_link_returns_the_linked_project(self):
        """Test - API NoGroup gets the project a public link points at, and the page is never cached"""
        response = self.client.get("/api/v1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["object_type"], "project")
        self.assertEqual(response.data["id"], 2)
        self.assertIn("no-store", response["Cache-Control"])
