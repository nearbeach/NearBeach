from django.contrib.auth.models import User
from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from NearBeach.views.tools.internal_functions import get_object_from_destination
from NearBeach.models import object_assignment

class TestInternalFunctions(TestCase):
    """
    Just testing the internal functions
    """
    fixtures = ['NearBeach_basic_setup.json']

    def test_kanban_board(self):
        # Get basic input object
        input_object = object_assignment.objects.filter(
            is_deleted=False,
        )

        # Get the objects
        response_kanban_board_1 = get_object_from_destination(input_object, 'kanban_board', 1)
        response_kanban_board_2 = get_object_from_destination(input_object, 'kanban_board', 2)

        # Make sure the first response is for QA Team
        self.assertEqual(response_kanban_board_1[0].group_id.group_name, 'QA Team')

        # Make sure there are no groups for second response
        self.assertEqual(len(response_kanban_board_2), 0)

    @staticmethod
    def test_organisation():
        # Get basic input object
        input_object = object_assignment.objects.filter(
            is_deleted=False,
        )

        # Get the objects
        _ = get_object_from_destination(input_object, 'organisation', 1)
        _ = get_object_from_destination(input_object, 'organisation', 2)

        # Make sure the first response is for QA Team
        # self.assertEqual(response_kanban_board_1[0].group_id.group_name, 'QA Team')

        # Make sure there are no groups for second response
        # self.assertEqual(len(response_kanban_board_2), 0)
