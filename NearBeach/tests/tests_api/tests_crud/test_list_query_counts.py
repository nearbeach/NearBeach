"""List endpoints must not run a query per row - the count stays flat however many rows come back"""
from django.db import connection
from django.test.utils import CaptureQueriesContext

from NearBeach.models.customer import Customer
from NearBeach.models.project import Project
from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ListQueryCountTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def _count(self, url):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return len(queries), response

    def test_project_list_query_count_does_not_grow_with_rows(self):
        _, response = self._count("/api/v1/project/")
        rows = len(response.data["results"])
        self.assertGreater(rows, 1)

        small, _ = self._count("/api/v1/project/")
        for project in Project.objects.filter(is_deleted=False)[:rows]:
            project.pk = None
            project.title = f"{project.title} copy"
            project.save()
        large, _ = self._count("/api/v1/project/")

        self.assertEqual(small, large)

    def test_customer_list_query_count_does_not_grow_with_rows(self):
        small, response = self._count("/api/v1/organisation/1/customer/")
        rows = len(response.data["results"])
        self.assertGreater(rows, 1)

        for customer in Customer.objects.filter(organisation_id=1, is_deleted=False):
            customer.pk = None
            customer.save()
        large, _ = self._count("/api/v1/organisation/1/customer/")

        self.assertEqual(small, large)
