from django.db import connection
from django.test.utils import CaptureQueriesContext

from NearBeach.models.misc.tag import Tag
from NearBeach.tests.utils.BaseApiClass import BaseApiClass

URL = "/api/v1/user/initial_data/"


class InitialDataCacheTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def _get(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        return response, len(queries)

    def test_second_call_runs_fewer_queries(self):
        _, first = self._get()
        _, second = self._get()

        self.assertLess(second, first)

    def test_saving_a_tag_clears_the_cache(self):
        before, _ = self._get()
        self._get()
        tag_count = len(before.data["tags"])

        Tag.objects.create(name="cache_invalidation_tag")

        after, _ = self._get()
        self.assertEqual(len(after.data["tags"]), tag_count + 1)
