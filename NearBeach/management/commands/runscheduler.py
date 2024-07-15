from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from NearBeach.views.tools.internal_functions import lookup_choice_from_key
from NearBeach.models import (
    OBJECT_TEMPLATE_TYPE,
    ObjectAssignment,
    ObjectTemplate,
    Project,
    SCH_SET_DAY_OF_THE_WEEK,
    SCH_WEEKLY,
    SCH_FORTNIGHTLY,
    SCH_MONTHLY,
    SCH_START_OF_THE_MONTH,
    SCH_END_OF_THE_MONTH,
    SCH_X_DAYS_BEFORE_END_OF_THE_MONTH,
    SCH_FIRST_BUSINESS_DAY_OF_THE_MONTH,
    SCH_LAST_BUSINESS_DAY_OF_THE_MONTH,
    ScheduledObject,
    Task,
)

User = get_user_model()

import datetime
import calendar

OBJECT_DICT = {
    "task": {
        "object": Task,
        "object_title": "task_short_description",
        "object_description": "task_long_description",
        "object_organisation": "organisation",
        "object_start_date": "task_start_date",
        "object_end_date": "task_end_date",
    },
    "project": {
        "object": Project,
        "object_title": "project_name",
        "object_description": "project_description",
        "object_organisation": "organisation",
        "object_start_date": "project_start_date",
        "object_end_date": "project_end_date",
    }
}


class Command(BaseCommand):
    help = "Run this command to run the scheduled jobs within NearBeach"

    def handle(self, *args, **kwargs):
        scheduled_objects = []
        #
        # # Run the functions in this particular order
        # scheduled_objects.extend(self.run_set_day_of_the_week())
        # scheduled_objects.extend(self.run_weekly())
        # scheduled_objects.extend(self.run_fortnightly())
        # scheduled_objects.extend(self.run_monthly())
        # scheduled_objects.extend(self.run_start_of_the_month())
        # scheduled_objects.extend(self.run_end_of_the_month())
        # scheduled_objects.extend(self.run_x_days_before_end_of_the_month())
        #
        # print(scheduled_objects)
        #
        # # Create the scheduled objects
        # for scheduled_object in scheduled_objects:
        #     self.create_object(scheduled_object=scheduled_object)


    def create_object(self, scheduled_object, *args, **kwargs):
        #TODO: Print off a log when creating these tasks/projects

        # Get the template
        template = ObjectTemplate.objects.get(object_template_id=scheduled_object.object_template_id)

        # Get the correct dictionary
        object_string = lookup_choice_from_key(
            OBJECT_TEMPLATE_TYPE,  # Choices
            template.object_template_id,  # Key
        )
        object_dict = OBJECT_DICT[object_string]

        # Setup the new template
        submit_object = object_dict["object"](
            create_user=User.objects.get(pk=1),
            **{
                object_dict["object_title"]: template.object_template_json["object_title"],
                object_dict["object_description"]: template.object_template_json["object_description"],
                object_dict["object_organisation_id"]: template.object_template_json["object_organisation"],
                object_dict["object_start_date"]: template.object_template_json["object_start_date"],
                object_dict["object_end_date"]: template.object_template_json["object_end_date"]
           },
        )
        submit_object.save()

        # Loop through the group list and add them
        for group_id in template.object_template_json["group_list"]:
            submit_object_assignment = ObjectAssignment(
                create_user=User.objects.get(pk=1),
                group_id_id=group_id,
                **{F"{object_string}_id": submit_object.pk }
            )
            submit_object_assignment.save()

        return


    def run_set_day_of_the_week(self):
        # Get today's date and day of the week
        todays_date = datetime.date.today()
        todays_day = calendar.day_name[todays_date.weekday()].lower()

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_SET_DAY_OF_THE_WEEK,
                start_date__lte=todays_date,
                is_active=True,
                # frequency_attribute__icontains=todays_day,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            )
        )

        # return [
        #     scheduled_object
        #     for scheduled_object in scheduled_objects
        #     # Check to make sure our day is within the scheduled Object
        #     if todays_day in scheduled_object.frequency_attribute["days_of_the_week"]
        # ]


    def run_weekly(self):
        todays_date = datetime.date.today()
        day_of_the_week = calendar.day_name[todays_date.weekday()]

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_WEEKLY,
                frequency_attribute__day_of_the_week=day_of_the_week,
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            )
        )


    def run_fortnightly(self):
        todays_date = datetime.date.today()
        day_of_the_week = calendar.day_name[todays_date.weekday()]
        last_run = todays_date - datetime.timedelta(days=14)

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_FORTNIGHTLY,
                frequency_attribute__day_of_the_week=day_of_the_week,
                last_run__gte=last_run,
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            )
        )


    def run_monthly(self):
        todays_date = datetime.date.today()
        last_run = todays_date - datetime.timedelta(days=14)

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_MONTHLY,
                last_run__gte=last_run,
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            )
        )


    def run_start_of_the_month(self):
        # If today is not the 1st - we will just leave
        todays_date = datetime.date.today()
        if todays_date.day != 1:
            return []

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_START_OF_THE_MONTH,
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            )
        )


    def run_end_of_the_month(self):
        # If today is not the end of the month - we will just leave
        todays_date = datetime.date.today()
        end_month_date = calendar.monthrange(todays_date.year, todays_date.month)[1]
        if todays_date.day != end_month_date:
            return []

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_END_OF_THE_MONTH,
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            )
        )


    def run_x_days_before_end_of_the_month(self):
        # If today's date is earlier than the 14th, just leave
        todays_date = datetime.date.today()
        if todays_date.day < 14:
            return []

        # Get the end date
        end_month_date = calendar.monthrange(todays_date.year, todays_date.month)[1]
        days_before = end_month_date - todays_date.day

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_X_DAYS_BEFORE_END_OF_THE_MONTH,
                frequency_attribute__days_before=days_before,
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            )
        )
