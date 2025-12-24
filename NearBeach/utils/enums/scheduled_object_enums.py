"""Module provides scheduled object enums for NearBeach"""
from django.db import models

# DEFINE GLOBALS
SCH_SET_DAY_OF_THE_WEEK = "Set Day of the Week"
SCH_WEEKLY = "Weekly"
SCH_FORTNIGHTLY = "Fortnightly"
SCH_MONTHLY = "Monthly"
SCH_START_OF_THE_MONTH = "Start of the Month"
SCH_END_OF_THE_MONTH = "End of the Month"
SCH_X_DAYS_BEFORE_END_OF_THE_MONTH = "X Days before End of the Month"
SCH_FIRST_BUSINESS_DAY_OF_THE_MONTH = "First Business Day of the Month"
SCH_LAST_BUSINESS_DAY_OF_THE_MONTH = "Last Business Day of the Month"


class ScheduledObjectEnum(models.TextChoices):
    """Class of enum values for Scheduled Objects"""
    SCH_SET_DAY_OF_THE_WEEK = SCH_SET_DAY_OF_THE_WEEK
    SCH_WEEKLY = SCH_WEEKLY
    SCH_FORTNIGHTLY = SCH_FORTNIGHTLY
    SCH_MONTHLY = SCH_MONTHLY
    SCH_START_OF_THE_MONTH = SCH_START_OF_THE_MONTH
    SCH_END_OF_THE_MONTH = SCH_END_OF_THE_MONTH
    SCH_X_DAYS_BEFORE_END_OF_THE_MONTH = SCH_X_DAYS_BEFORE_END_OF_THE_MONTH
    # SCH_FIRST_BUSINESS_DAY_OF_THE_MONTH = SCH_FIRST_BUSINESS_DAY_OF_THE_MONTH
    # SCH_LAST_BUSINESS_DAY_OF_THE_MONTH = SCH_LAST_BUSINESS_DAY_OF_THE_MONTH
