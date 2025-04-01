from django.test import TestCase
from collections import namedtuple
from NearBeach.management.commands.updatecrontab import Command, ContabTime


class ContabTimeTest(TestCase):

    def test_valid_validate_timestr(self):
        tests = [
            ContabTime.from_string("0 9 * * *"),       # Run at 9:00 AM every day
            ContabTime.from_string("0 9 * * 0"),       # Run at 9:00 AM every Sunday
            ContabTime.from_string("0 9-17 * * *"),    # Run every hour from 9:00 AM to 5:00 PM
            ContabTime.from_string("0 9 * * 1-5"),     # Run at 9:00 AM every Monday to Friday
            ContabTime.from_string("0 9 * * 0/5"),     # Run at 9:00 AM every 5 days starting from Sunday
            ContabTime.from_string("0 9-17/2 * * *"),  # Run every 2 hours from 9:00 AM to 5:00 PM
            ContabTime.from_string("0 7,9 * * *"),     # Run at 9:00 and 9:00 AM every day
        ]
        for tab in tests:
            with self.subTest(teststr=str(tab)):
                tab.validate()


    def test_invalid_validate_timestr(self):
        tests = [
            ContabTime.from_string("0 9:30 * *"),   # Invalid: Invalid character
            ContabTime.from_string("0 9 * * a"),    # Invalid: Invalid character
            ContabTime.from_string("0 9 * * *;"),   # Invalid: Invalid character
            ContabTime.from_string("0 9 * * *\n"),  # Invalid: Invalid character
            ContabTime.from_string("0 9 * * * *"),  # Invalid: Too many fields
            ContabTime.from_string("0 9 * *"),      # Invalid: Missing field
            ContabTime.from_string("60 * * *"),     # Invalid: Minutes out of valid range
            ContabTime.from_string("* 24 * *"),     # Invalid: Minutes out of valid range
            ContabTime.from_string("* * 32 * *"),   # Invalid: Day of month out of valid range
            ContabTime.from_string("* * * 13 *"),   # Invalid: Month out of valid range
            ContabTime.from_string("0 9 * * 8"),    # Invalid: Day of week out of valid range
        ]

        for tab in tests:
            with self.subTest(teststr=str(tab)):
                with self.assertRaises(ValueError):
                    tab.validate()
