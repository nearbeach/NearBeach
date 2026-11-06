from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoPermissionPermissionTests(BaseApiClass):
    username = "team_no_permissions"
    password = "Test1234$"

    def test_api_permissions_no_permission_organisation_read(self):
        """Test - API NoPermission Permissions for reading an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/2/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_permission_organisation_list(self):
        """Test - API NoPermission Permissions for listing Organisations"""
        data_list = [
            self.URLTest("/api/v1/organisation/", {}, 403, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_permission_organisation_create(self):
        """Test - API NoPermission Permissions for creating an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/", {'name': 'API Organisation', 'website': 'https://api.example', 'email': 'api@api.example'}, 403, "POST"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_permission_organisation_update(self):
        """Test - API NoPermission Permissions for updating an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/", {'name': 'New API Organisation Name'}, 403, "PATCH"),
            self.URLTest("/api/v1/organisation/2/", {'name': 'New API Organisation Name'}, 404, "PATCH"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_permission_organisation_delete(self):
        """Test - API NoPermission Permissions for deleting an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/organisation/1/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_permission_organisation_customers_read(self):
        """Test - API NoPermission Permissions for reading the customers of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/2/customer/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_permission_organisation_customers_create(self):
        """Test - API NoPermission Permissions for creating a customer on an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/", {'first_name': 'Api', 'last_name': 'Customer', 'email': 'api.customer@api.example', 'title': 1}, 403, "POST"),
            self.URLTest("/api/v1/organisation/2/customer/", {'first_name': 'Api', 'last_name': 'Customer', 'email': 'api.customer@api.example', 'title': 1}, 404, "POST"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_permission_organisation_customers_update(self):
        """Test - API NoPermission Permissions for updating a customer of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/1/", {'first_name': 'Changed'}, 403, "PATCH"),
            self.URLTest("/api/v1/organisation/2/customer/1/", {'first_name': 'Changed'}, 404, "PATCH"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_permission_organisation_customers_delete(self):
        """Test - API NoPermission Permissions for deleting a customer of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/organisation/2/customer/1/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)
