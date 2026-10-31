"""CRUD tests for updating a customer through its organisation, run as the admin.

Fixture data: organisation 1 ("NearBeach Incorporate") has customers 1 and 2.
"""
from NearBeach.models.customer import Customer
from NearBeach.tests.utils.BaseApiClass import BaseApiClass

CUSTOMER_URL = "/api/v1/organisation/1/customer/1/"


class CustomerUpdateTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_patch_updates_and_returns_the_customer(self):
        response = self.client.patch(CUSTOMER_URL, {"first_name": "Patched"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Patched")
        self.assertEqual(Customer.objects.get(pk=1).first_name, "Patched")

    def test_patch_leaves_other_customers_alone(self):
        before = Customer.objects.get(pk=2).first_name

        self.client.patch(CUSTOMER_URL, {"first_name": "Patched"}, format="json")

        self.assertEqual(Customer.objects.get(pk=2).first_name, before)

    def test_patch_with_invalid_email_is_rejected(self):
        response = self.client.patch(CUSTOMER_URL, {"email": "not-an-email"}, format="json")

        self.assertEqual(response.status_code, 400)

    def test_patch_of_a_customer_from_another_organisation_is_rejected(self):
        response = self.client.patch(
            "/api/v1/organisation/1/customer/9999/", {"first_name": "Patched"}, format="json"
        )

        self.assertIn(response.status_code, (400, 404))

    def test_get_and_delete_share_the_customer_url(self):
        self.assertEqual(self.client.get(CUSTOMER_URL).status_code, 200)
        self.assertEqual(self.client.delete(CUSTOMER_URL).status_code, 204)
        self.assertTrue(Customer.objects.get(pk=1).is_deleted)
