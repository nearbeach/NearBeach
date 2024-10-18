from collections import namedtuple

from django.test import TestCase
from NearBeach.management.commands.runscheduler import Command
from NearBeach.models import ScheduledObject
from unittest import mock

import datetime


SCHEDULETest = namedtuple(
    "SCHEDULETest",
    ["year", "month", "day", "expected_ids"],
    defaults=[2024, 1, 1, [1]]
)


class RunSchedulerTest(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    # @mock.patch(Command.get_today)
    @mock.patch('NearBeach.management.commands.runscheduler.Command.get_today')
    def test_run_set_day_of_the_week(self, mock_get_today):
        # Data Array for loop
        data_array = [
            SCHEDULETest(2023, 12, 1, []),
            SCHEDULETest(2023, 12, 2, []),
            SCHEDULETest(2023, 12, 3, []),
            SCHEDULETest(2023, 12, 4, []),
            SCHEDULETest(2023, 12, 5, []),
            SCHEDULETest(2023, 12, 6, []),
            SCHEDULETest(2023, 12, 7, []),
            SCHEDULETest(2024, 1, 1, [1]),
            SCHEDULETest(2024, 1, 2, []),
            SCHEDULETest(2024, 1, 3, [1]),
            SCHEDULETest(2024, 1, 4, []),
            SCHEDULETest(2024, 1, 5, [1]),
            SCHEDULETest(2024, 1, 6, []),
            SCHEDULETest(2024, 1, 7, []),
            SCHEDULETest(2024, 1, 8, [1]),
            SCHEDULETest(2024, 1, 9, []),
            SCHEDULETest(2024, 1, 10, [1]),
            SCHEDULETest(2024, 1, 11, []),
            SCHEDULETest(2024, 1, 12, [1]),
            SCHEDULETest(2024, 1, 13, []),
            SCHEDULETest(2024, 1, 14, []),
            SCHEDULETest(2024, 2, 1, []),
            SCHEDULETest(2024, 2, 2, []),
            SCHEDULETest(2024, 2, 3, []),
            SCHEDULETest(2024, 2, 4, []),
            SCHEDULETest(2024, 2, 5, []),
            SCHEDULETest(2024, 2, 6, []),
            SCHEDULETest(2024, 2, 7, []),
        ]
        
        for data in data_array:
            # Arrange
            expected_results = ScheduledObject.objects.filter(pk__in=data.expected_ids)
            mock_get_today.return_value = datetime.date(data.year, data.month, data.day)

            # Act
            results = Command().run_set_day_of_the_week()

            # Assert
            self.assertEqual(
                list(expected_results.values("pk")),
                list(results.values("pk")),
                F"Run set day of the week: Date: {data.year}-{data.month}-{data.day}"
            )
            # self.assertTrue(False)

    @mock.patch('NearBeach.management.commands.runscheduler.Command.get_today')
    def test_run_weekly(self, mock_get_today):
        # Data Array for loop
        data_array = [
            SCHEDULETest(2023, 12, 1, []),
            SCHEDULETest(2023, 12, 2, []),
            SCHEDULETest(2023, 12, 3, []),
            SCHEDULETest(2023, 12, 4, []),
            SCHEDULETest(2023, 12, 5, []),
            SCHEDULETest(2023, 12, 6, []),
            SCHEDULETest(2023, 12, 7, []),
            SCHEDULETest(2024, 1, 1, [2]),
            SCHEDULETest(2024, 1, 2, []),
            SCHEDULETest(2024, 1, 3, []),
            SCHEDULETest(2024, 1, 4, []),
            SCHEDULETest(2024, 1, 5, []),
            SCHEDULETest(2024, 1, 6, []),
            SCHEDULETest(2024, 1, 7, []),
            SCHEDULETest(2024, 1, 8, [2]),
            SCHEDULETest(2024, 1, 9, []),
            SCHEDULETest(2024, 1, 10, []),
            SCHEDULETest(2024, 1, 11, []),
            SCHEDULETest(2024, 1, 12, []),
            SCHEDULETest(2024, 1, 13, []),
            SCHEDULETest(2024, 1, 14, []),
            SCHEDULETest(2024, 2, 1, []),
            SCHEDULETest(2024, 2, 2, []),
            SCHEDULETest(2024, 2, 3, []),
            SCHEDULETest(2024, 2, 4, []),
            SCHEDULETest(2024, 2, 5, []),
            SCHEDULETest(2024, 2, 6, []),
            SCHEDULETest(2024, 2, 7, []),
        ]

        for data in data_array:
            # Arrange
            expected_results = ScheduledObject.objects.filter(pk__in=data.expected_ids)
            mock_get_today.return_value = datetime.date(data.year, data.month, data.day)

            # Act
            results = Command().run_weekly()

            # Assert
            self.assertEqual(
                list(expected_results.values("pk")),
                list(results.values("pk")),
                F"Run set day of the week: Date: {data.year}-{data.month}-{data.day}. Expected: {data.expected_ids}"
            )
            # self.assertTrue(False)
            
            

    @mock.patch('NearBeach.management.commands.runscheduler.Command.get_today')
    def test_run_fortnightly(self, mock_get_today):
        # Data Array for loop
        data_array = [
            SCHEDULETest(2023, 12, 1, []),
            SCHEDULETest(2023, 12, 2, []),
            SCHEDULETest(2023, 12, 3, []),
            SCHEDULETest(2023, 12, 4, []),
            SCHEDULETest(2023, 12, 5, []),
            SCHEDULETest(2023, 12, 6, []),
            SCHEDULETest(2023, 12, 7, []),
            SCHEDULETest(2023, 12, 8, []),
            SCHEDULETest(2023, 12, 9, []),
            SCHEDULETest(2023, 12, 10, []),
            SCHEDULETest(2023, 12, 11, []),
            SCHEDULETest(2023, 12, 12, []),
            SCHEDULETest(2023, 12, 13, []),
            SCHEDULETest(2023, 12, 14, []),
            SCHEDULETest(2023, 12, 15, []),
            SCHEDULETest(2023, 12, 16, []),
            SCHEDULETest(2023, 12, 17, []),
            SCHEDULETest(2023, 12, 18, []),
            SCHEDULETest(2023, 12, 19, []),
            SCHEDULETest(2023, 12, 20, []),
            SCHEDULETest(2023, 12, 21, []),
            SCHEDULETest(2023, 12, 22, []),
            SCHEDULETest(2023, 12, 23, []),
            SCHEDULETest(2023, 12, 24, []),
            SCHEDULETest(2023, 12, 25, []),
            SCHEDULETest(2023, 12, 26, []),
            SCHEDULETest(2023, 12, 27, []),
            SCHEDULETest(2023, 12, 28, []),
            SCHEDULETest(2023, 12, 29, []),
            SCHEDULETest(2023, 12, 30, []),
            SCHEDULETest(2023, 12, 31, []),
            SCHEDULETest(2024, 1, 1, []),
            SCHEDULETest(2024, 1, 2, []),
            SCHEDULETest(2024, 1, 3, []),
            SCHEDULETest(2024, 1, 4, []),
            SCHEDULETest(2024, 1, 5, []),
            SCHEDULETest(2024, 1, 6, [3]),
            SCHEDULETest(2024, 1, 7, []),
            SCHEDULETest(2024, 1, 8, []),
            SCHEDULETest(2024, 1, 9, []),
            SCHEDULETest(2024, 1, 10, []),
            SCHEDULETest(2024, 1, 11, []),
            SCHEDULETest(2024, 1, 12, []),
            SCHEDULETest(2024, 1, 13, []),
            SCHEDULETest(2024, 1, 14, []),
            SCHEDULETest(2024, 1, 15, []),
            SCHEDULETest(2024, 1, 16, []),
            SCHEDULETest(2024, 1, 17, []),
            SCHEDULETest(2024, 1, 18, []),
            SCHEDULETest(2024, 1, 19, []),
            SCHEDULETest(2024, 1, 20, [12]),
            SCHEDULETest(2024, 1, 21, []),
            SCHEDULETest(2024, 1, 22, []),
            SCHEDULETest(2024, 1, 23, []),
            SCHEDULETest(2024, 1, 24, []),
            SCHEDULETest(2024, 1, 25, []),
            SCHEDULETest(2024, 1, 26, []),
            SCHEDULETest(2024, 1, 27, []),
            SCHEDULETest(2024, 1, 28, []),
            SCHEDULETest(2024, 1, 29, []),
            SCHEDULETest(2024, 1, 30, []),
            SCHEDULETest(2024, 1, 31, []),
            SCHEDULETest(2024, 2, 1, []),
            SCHEDULETest(2024, 2, 2, []),
            SCHEDULETest(2024, 2, 3, []),
            SCHEDULETest(2024, 2, 4, []),
            SCHEDULETest(2024, 2, 5, []),
            SCHEDULETest(2024, 2, 6, []),
            SCHEDULETest(2024, 2, 7, []),
            SCHEDULETest(2024, 2, 8, []),
            SCHEDULETest(2024, 2, 9, []),
            SCHEDULETest(2024, 2, 10, []),
            SCHEDULETest(2024, 2, 11, []),
            SCHEDULETest(2024, 2, 12, []),
            SCHEDULETest(2024, 2, 13, []),
            SCHEDULETest(2024, 2, 14, []),
            SCHEDULETest(2024, 2, 15, []),
            SCHEDULETest(2024, 2, 16, []),
            SCHEDULETest(2024, 2, 17, []),
            SCHEDULETest(2024, 2, 18, []),
            SCHEDULETest(2024, 2, 19, []),
            SCHEDULETest(2024, 2, 20, []),
            SCHEDULETest(2024, 2, 21, []),
        ]

        for data in data_array:
            # Arrange
            expected_results = ScheduledObject.objects.filter(pk__in=data.expected_ids)
            mock_get_today.return_value = datetime.date(data.year, data.month, data.day)

            # Act
            results = Command().run_fortnightly()

            # Assert
            self.assertEqual(
                list(expected_results.values("pk")),
                list(results.values("pk")),
                F"Run set day of the week: Date: {data.year}-{data.month}-{data.day}. Expected: {data.expected_ids}"
            )
            # self.assertTrue(False)

