"""The list of requirement items of a requirement.

Requirement items have no group rows of their own - they take their access from the requirement they belong to.
In the fixture requirement 1 (item 1) is in the Administration group and requirement 2 (item 2) is in the QA Team.
"""
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.tests.utils.BaseApiClass import BaseApiClass

ITEM_LIST_URL = "/api/v1/requirement/{requirement_id}/requirement_item/"


class RequirementItemListAsAdminTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def _ids(self, requirement_id):
        response = self.client.get(ITEM_LIST_URL.format(requirement_id=requirement_id))
        self.assertEqual(response.status_code, 200)
        return sorted(item["id"] for item in response.data["results"])

    def test_list_has_the_items_of_the_requirement(self):
        self.assertEqual(self._ids(1), [1])
        self.assertEqual(self._ids(2), [2])

    def test_list_leaves_out_deleted_items(self):
        RequirementItem.objects.filter(pk=1).update(is_deleted=True)

        self.assertEqual(self._ids(1), [])
        self.assertEqual(self._ids(2), [2])

    def test_search_finds_an_item_by_title(self):
        response = self.client.get(ITEM_LIST_URL.format(requirement_id=2), {"search": "QA Team"})

        self.assertEqual([item["id"] for item in response.data["results"]], [2])


class RequirementItemListAsTeamLeaderTests(BaseApiClass):
    """The team leader is only in the QA Team"""
    username = "team_leader"
    password = "Test1234$"

    def test_list_has_the_items_of_an_accessible_requirement(self):
        response = self.client.get(ITEM_LIST_URL.format(requirement_id=2))

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data["results"]], [2])

    def test_items_of_an_inaccessible_requirement_are_never_listed(self):
        response = self.client.get(ITEM_LIST_URL.format(requirement_id=1))

        # Refusing the request or sending an empty list are both fine - listing item 1 is not
        if response.status_code == 200:
            self.assertEqual([item["id"] for item in response.data["results"]], [])
        else:
            self.assertEqual(response.status_code, 403)
