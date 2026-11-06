from django.contrib.auth.models import User

from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ApiNoGroupPermissionTests(BaseApiClass):
    username = "no_group"
    password = "Test1234$"

    # OVERRIDE - a user in no group can not log in through the api, but can still hold a session
    def _login_user(self):
        self.client.force_login(User.objects.get(username=self.username))

    def test_api_permissions_no_group_organisation_read(self):
        """Test - API NoGroup Permissions for reading an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/2/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_organisation_list(self):
        """Test - API NoGroup Permissions for listing Organisations"""
        data_list = [
            self.URLTest("/api/v1/organisation/", {}, 403, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_organisation_create(self):
        """Test - API NoGroup Permissions for creating an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/", {'name': 'API Organisation', 'website': 'https://api.example', 'email': 'api@api.example'}, 403, "POST"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_organisation_update(self):
        """Test - API NoGroup Permissions for updating an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/", {'name': 'New API Organisation Name'}, 403, "PATCH"),
            self.URLTest("/api/v1/organisation/2/", {'name': 'New API Organisation Name'}, 404, "PATCH"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_organisation_delete(self):
        """Test - API NoGroup Permissions for deleting an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/2/", {}, 404, "DELETE"),
            self.URLTest("/api/v1/organisation/1/", {}, 403, "DELETE"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_organisation_customers_read(self):
        """Test - API NoGroup Permissions for reading the customers of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 403, "GET"),
            self.URLTest("/api/v1/organisation/2/customer/", {}, 404, "GET"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_organisation_customers_create(self):
        """Test - API NoGroup Permissions for creating a customer on an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/", {'first_name': 'Api', 'last_name': 'Customer', 'email': 'api.customer@api.example', 'title': 1}, 403, "POST"),
            self.URLTest("/api/v1/organisation/2/customer/", {'first_name': 'Api', 'last_name': 'Customer', 'email': 'api.customer@api.example', 'title': 1}, 404, "POST"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_organisation_customers_update(self):
        """Test - API NoGroup Permissions for updating a customer of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/1/", {'first_name': 'Changed'}, 403, "PATCH"),
            self.URLTest("/api/v1/organisation/2/customer/1/", {'first_name': 'Changed'}, 404, "PATCH"),
        ]

        self._run_test_array(data_list)

    def test_api_permissions_no_group_organisation_customers_delete(self):
        """Test - API NoGroup Permissions for deleting a customer of an Organisation"""
        data_list = [
            self.URLTest("/api/v1/organisation/1/customer/99/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/organisation/1/customer/1/", {}, 403, "DELETE"),
            self.URLTest("/api/v1/organisation/2/customer/1/", {}, 404, "DELETE"),
        ]

        self._run_test_array(data_list)
