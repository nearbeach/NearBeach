from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiTeamLeaderPermissionTests(BaseApiClass):
    username = "team_leader"
    password = "Test1234$"

    def test_api_permissions_team_leader_organisation_read(self):
        """Test - API TeamLeader Permissions for reading an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/", {}, 200, "GET"),
            self.URLTest("/api/v1/organisation/2/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_leader_organisation_list(self):
        """Test - API TeamLeader Permissions for listing Organisations"""
        data_list = [
            self.URLTest("/api/v1/organisation/", {}, 200, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_leader_organisation_create(self):
        """Test - API TeamLeader Permissions for creating an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/", {'name': 'API Organisation', 'website': 'https://api.example', 'email': 'api@api.example'}, 201, "POST"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_leader_organisation_update(self):
        """Test - API TeamLeader Permissions for updating an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/", {'name': 'New API Organisation Name'}, 200, "PATCH"),
            self.URLTest("/api/v1/organisation/2/", {'name': 'New API Organisation Name'}, 404, "PATCH"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_leader_organisation_delete(self):
        """Test - API TeamLeader Permissions for deleting an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/organisation/1/", {}, 204, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_leader_organisation_customers_read(self):
        """Test - API TeamLeader Permissions for reading the customers of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/", {}, 200, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 200, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 404, "GET"),
            self.URLTest("/api/v1/organisation/2/customer/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_leader_organisation_customers_create(self):
        """Test - API TeamLeader Permissions for creating a customer on an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/", {'first_name': 'Api', 'last_name': 'Customer', 'email': 'api.customer@api.example', 'title': 1}, 201, "POST"),
            self.URLTest("/api/v1/organisation/2/customer/", {'first_name': 'Api', 'last_name': 'Customer', 'email': 'api.customer@api.example', 'title': 1}, 404, "POST"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_leader_organisation_customers_update(self):
        """Test - API TeamLeader Permissions for updating a customer of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/1/", {'first_name': 'Changed'}, 200, "PATCH"),
            self.URLTest("/api/v1/organisation/2/customer/1/", {'first_name': 'Changed'}, 404, "PATCH"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_team_leader_organisation_customers_delete(self):
        """Test - API TeamLeader Permissions for deleting a customer of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 400, "DELETE"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 204, "DELETE"),
            self.URLTest("/api/v1/organisation/2/customer/1/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)
