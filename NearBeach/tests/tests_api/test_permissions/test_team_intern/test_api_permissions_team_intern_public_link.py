from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiTeamInternPublicLinkPermissionTests(BaseApiClass):
    """A public link is readable by any logged-in user - their group and permission set do not matter"""
    username = "team_intern"
    password = "Test1234$"

    def test_api_permissions_team_intern_public_link(self):
        """Test - API TeamIntern Permissions for the Public Link module"""
        data_list = [
            self.URLTest("/api/v1/public_link/3d7346c4-05b6-41df-816a-eff814d9bbd0/", {}, 200, "GET"),
            self.URLTest("/api/v1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/", {}, 200, "GET"),
            self.URLTest("/api/v1/public_link/00000000-0000-0000-0000-000000000000/", {}, 404, "GET"),
            self.URLTest("/api/v1/public_link/not-a-uuid/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_intern_public_link_returns_the_linked_project(self):
        """Test - API TeamIntern gets the project a public link points at, and the page is never cached"""
        response = self.client.get("/api/v1/public_link/5f369dc9-a0bb-416d-9779-92576d0500bb/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["object_type"], "project")
        self.assertEqual(response.data["id"], 2)
        self.assertIn("no-store", response["Cache-Control"])
