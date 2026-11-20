"""CRUD tests for requirement items, run as the team leader.

Items 1 and 2 of the fixture sit in requirements 1 and 2 with the same ids, which hides any place the code mixes up
an item id and a requirement id. These tests create a new item (id 3) in requirement 2, so the two never match.

The team leader is only in the QA Team: they can use requirement 2 but not requirement 1 (Administration).
"""
from NearBeach.models.audit_log import AuditLog
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.tests.utils.BaseApiClass import BaseApiClass
from NearBeach.utils.enums.audit_enums import AuditAction

QA_REQUIREMENT_URL = "/api/v1/requirement/2/requirement_item/"
QA_GROUP = 2


class RequirementItemCrudBase(BaseApiClass):
    username = "team_leader"
    password = "Test1234$"

    def _create(self, url=QA_REQUIREMENT_URL, **overrides):
        body = {"title": "Leader item", "group_list": [QA_GROUP], **overrides}
        return self.client.post(url, body, format="json")

    def _create_item(self):
        response = self._create()
        self.assertEqual(response.status_code, 201, response.data)
        return response.data["id"]

    def _entries(self, item_id, action):
        return AuditLog.objects.filter(object_type="requirement_item", object_id=item_id, action=action)


class RequirementItemCreateTests(RequirementItemCrudBase):
    def test_create_puts_the_item_in_the_requirement_of_the_url(self):
        response = self._create()

        self.assertEqual(response.status_code, 201, response.data)
        item = RequirementItem.objects.get(pk=response.data["id"])
        self.assertEqual(item.requirement_id, 2)
        self.assertEqual(item.title, "Leader item")
        self.assertEqual(item.creation_user.username, "team_leader")
        self.assertEqual(item.change_user.username, "team_leader")
        self.assertFalse(item.is_deleted)

    def test_a_new_item_is_not_the_same_id_as_its_requirement(self):
        self.assertNotEqual(self._create_item(), 2)

    def test_a_new_item_is_listed_in_its_requirement_only(self):
        item_id = self._create_item()

        listed = [item["id"] for item in self.client.get(QA_REQUIREMENT_URL).data["results"]]
        self.assertEqual(sorted(listed), [2, item_id])

    def test_a_new_item_can_be_read_back(self):
        item_id = self._create_item()

        response = self.client.get(f"{QA_REQUIREMENT_URL}{item_id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Leader item")

    def test_a_new_item_is_audited(self):
        item_id = self._create_item()

        self.assertEqual(self._entries(item_id, AuditAction.CREATE).count(), 1)

    def test_a_requirement_the_leader_cannot_use_is_refused(self):
        before = RequirementItem.objects.count()

        response = self._create("/api/v1/requirement/1/requirement_item/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(RequirementItem.objects.count(), before)

    def test_a_requirement_that_does_not_exist_is_not_found(self):
        before = RequirementItem.objects.count()

        response = self._create("/api/v1/requirement/3/requirement_item/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(RequirementItem.objects.count(), before)

    def test_bad_items_are_rejected_and_nothing_is_saved(self):
        bodies = {
            "no title": {"group_list": [QA_GROUP]},
            "blank title": {"title": "", "group_list": [QA_GROUP]},
            "group the leader is not in": {"title": "x", "group_list": [1]},
        }
        before = RequirementItem.objects.count()

        for name, body in bodies.items():
            with self.subTest(name):
                self.assertEqual(self.client.post(QA_REQUIREMENT_URL, body, format="json").status_code, 400)

        self.assertEqual(RequirementItem.objects.count(), before)


class RequirementItemUpdateTests(RequirementItemCrudBase):
    def test_updating_an_item_changes_that_item(self):
        item_id = self._create_item()

        response = self.client.patch(f"{QA_REQUIREMENT_URL}{item_id}/", {"title": "Renamed"}, format="json")

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(RequirementItem.objects.get(pk=item_id).title, "Renamed")

    def test_updating_an_item_leaves_the_item_with_the_requirements_id_alone(self):
        """Item 2 has the same id as requirement 2 - it must not be the one that gets saved"""
        item_id = self._create_item()
        original_title = RequirementItem.objects.get(pk=2).title

        self.client.patch(f"{QA_REQUIREMENT_URL}{item_id}/", {"title": "Renamed"}, format="json")

        self.assertEqual(RequirementItem.objects.get(pk=2).title, original_title)

    def test_updating_an_item_records_who_changed_it_and_audits_that_item(self):
        item_id = self._create_item()

        self.client.patch(f"{QA_REQUIREMENT_URL}{item_id}/", {"title": "Renamed"}, format="json")

        self.assertEqual(RequirementItem.objects.get(pk=item_id).change_user.username, "team_leader")
        entry = self._entries(item_id, AuditAction.UPDATE).get()
        self.assertEqual(entry.changes["title"]["new"], "Renamed")
        self.assertFalse(self._entries(2, AuditAction.UPDATE).exists())

    def test_items_that_are_not_in_the_requirement_are_not_found(self):
        original_title = RequirementItem.objects.get(pk=1).title
        cases = {
            "does not exist": f"{QA_REQUIREMENT_URL}99999/",
            "belongs to requirement 1": f"{QA_REQUIREMENT_URL}1/",
        }

        for name, url in cases.items():
            with self.subTest(name):
                self.assertEqual(self.client.patch(url, {"title": "Hijacked"}, format="json").status_code, 404)

        self.assertEqual(RequirementItem.objects.get(pk=1).title, original_title)


class RequirementItemDeleteTests(RequirementItemCrudBase):
    def test_deleting_an_item_is_a_soft_delete(self):
        item_id = self._create_item()

        response = self.client.delete(f"{QA_REQUIREMENT_URL}{item_id}/")

        self.assertEqual(response.status_code, 204)
        item = RequirementItem.objects.get(pk=item_id)
        self.assertTrue(item.is_deleted)
        self.assertEqual(item.change_user.username, "team_leader")

    def test_deleting_an_item_leaves_the_item_with_the_requirements_id_alone(self):
        item_id = self._create_item()

        self.client.delete(f"{QA_REQUIREMENT_URL}{item_id}/")

        self.assertFalse(RequirementItem.objects.get(pk=2).is_deleted)

    def test_a_deleted_item_leaves_the_list_and_is_audited_as_the_item(self):
        item_id = self._create_item()

        self.client.delete(f"{QA_REQUIREMENT_URL}{item_id}/")

        listed = [item["id"] for item in self.client.get(QA_REQUIREMENT_URL).data["results"]]
        self.assertEqual(listed, [2])
        self.assertEqual(self._entries(item_id, AuditAction.DELETE).count(), 1)
        self.assertFalse(AuditLog.objects.filter(object_type="requirement_item", object_id=2, action=AuditAction.DELETE).exists())

    def test_deleting_twice_is_not_found(self):
        item_id = self._create_item()
        self.client.delete(f"{QA_REQUIREMENT_URL}{item_id}/")

        self.assertEqual(self.client.delete(f"{QA_REQUIREMENT_URL}{item_id}/").status_code, 404)

    def test_items_that_are_not_in_the_requirement_are_not_found(self):
        for name, url in {
            "does not exist": f"{QA_REQUIREMENT_URL}99999/",
            "belongs to requirement 1": f"{QA_REQUIREMENT_URL}1/",
        }.items():
            with self.subTest(name):
                self.assertEqual(self.client.delete(url).status_code, 404)

        self.assertFalse(RequirementItem.objects.get(pk=1).is_deleted)
