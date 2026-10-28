"""get_parent_object - child objects (requirement items, change tasks, kanban cards) have no groups of their own,
so permissions are checked against their parent."""
from django.test import TestCase

from NearBeach.models.kanban_board.kanban_card import KanbanCard
from NearBeach.models.request_for_change.change_task import ChangeTask
from NearBeach.models.requirement.requirement_item import RequirementItem
from NearBeach.utils.api.get_parent_object import get_parent_object


class GetParentObjectTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def test_objects_that_are_not_children_come_back_unchanged(self):
        for destination in ("project", "task", "requirement", "request_for_change", "kanban_board", "organisation"):
            with self.subTest(destination=destination):
                self.assertEqual(get_parent_object(destination, "7"), (destination, "7"))

    def test_a_requirement_item_gives_its_requirement(self):
        item = RequirementItem.objects.filter(is_deleted=False).first()

        self.assertEqual(get_parent_object("requirement_item", str(item.pk)), ("requirement", item.requirement_id))

    def test_a_change_task_gives_its_request_for_change(self):
        task = ChangeTask.objects.filter(is_deleted=False).first()

        self.assertEqual(get_parent_object("change_task", str(task.pk)), ("request_for_change", task.request_for_change_id))

    def test_a_kanban_card_gives_its_kanban_board(self):
        card = KanbanCard.objects.filter(is_deleted=False).first()

        self.assertEqual(get_parent_object("kanban_card", str(card.pk)), ("kanban_board", card.kanban_board_id))

    def test_the_location_id_can_be_a_number_or_a_string(self):
        """Urls give a string, other code gives an int"""
        item = RequirementItem.objects.filter(is_deleted=False).first()

        self.assertEqual(
            get_parent_object("requirement_item", item.pk),
            get_parent_object("requirement_item", str(item.pk)),
        )

    def test_a_child_that_does_not_exist_has_no_parent(self):
        for destination in ("requirement_item", "change_task", "kanban_card"):
            with self.subTest(destination=destination):
                self.assertEqual(get_parent_object(destination, "999999"), (None, None))

    def test_a_deleted_child_has_no_parent(self):
        item = RequirementItem.objects.filter(is_deleted=False).first()
        RequirementItem.objects.filter(pk=item.pk).update(is_deleted=True)

        self.assertEqual(get_parent_object("requirement_item", str(item.pk)), (None, None))
