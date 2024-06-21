from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from NearBeach.models import ObjectAssignment, ScheduledObject, ObjectTemplate, Task, Project, OBJECT_TEMPLATE_TYPE
from NearBeach.views.tools.internal_functions import lookup_choice_from_key

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
        # Run the functions in this particular order
        self.run_set_day_of_the_week()
        self.run_weekly()
        self.run_fortnightly()
        self.run_monthly()
        self.run_start_of_the_month()
        self.run_end_of_the_month()
        self.run_x_days_before_end_of_the_month()

    def create_object(self, scheduled_object, *args, **kwargs):
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
                object_dict["object_organisation"]: template.object_template_json["object_organisation"],
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

        return

    def run_set_day_of_the_week(self):
        # Get today's date and day of the week
        todays_date = datetime.date.today()
        todays_day = calendar.day_name[todays_date.weekday()].lower()

        # Get data and process
        scheduled_objects = ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency="Weekly",
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

        for scheduled_object in scheduled_objects:
            # Check to make sure our day is within the scheduled Object
            if todays_day in scheduled_object.frequency_attribute["days_of_the_week"]:
                self.create_object(scheduled_object=scheduled_object)

        return

    def run_weekly(self):
        todays_date = datetime.date.today()
        day_of_the_week = calendar.day_name[todays_date.weekday()]

        # Get data and process
        scheduled_objects = ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency="Weekly",
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

        # Create the objects
        for scheduled_object in scheduled_objects:
            self.create_object(scheduled_object=scheduled_object)

        return

    def run_fortnightly(self):
        todays_date = datetime.date.today()
        day_of_the_week = calendar.day_name[todays_date.weekday()]
        last_run = todays_date - datetime.timedelta(days=14)

        # Get data and process
        scheduled_objects = ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency="Fortnightly",
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

        # Create the objects
        for scheduled_object in scheduled_objects:
            self.create_object(scheduled_object=scheduled_object)

        return

    def run_monthly(self):
        todays_date = datetime.date.today()
        last_run = todays_date - datetime.timedelta(days=14)

        # Get data and process
        scheduled_objects = ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency="Monthly",
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

        # Create the objects
        for scheduled_object in scheduled_objects:
            # Check to make sure the monthly day matches today's day
            if scheduled_object.start_date.day == todays_date.day:
                self.create_object(scheduled_object=scheduled_object)

        return

    def run_start_of_the_month(self):
        # If today is not the 1st - we will just leave
        todays_date = datetime.date.today()
        if todays_date.day != 1:
            return

        # Get data and process
        scheduled_objects = ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency="Start of the Month",
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

        # Create the objects
        for scheduled_object in scheduled_objects:
            self.create_object(scheduled_object=scheduled_object)

        return

    def run_end_of_the_month(self):
        # If today is not the end of the month - we will just leave
        todays_date = datetime.date.today()
        end_month_date = calendar.monthrange(todays_date.year, todays_date.month)[1]
        if todays_date.day != end_month_date:
            return

        # Get data and process
        scheduled_objects = ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency="End of the Month",
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

        # Create the objects
        for scheduled_object in scheduled_objects:
            self.create_object(scheduled_object=scheduled_object)

        return

    def run_x_days_before_end_of_the_month(self):
        # If today's date is earlier than the 14th, just leave
        todays_date = datetime.date.today()
        if todays_date.day < 14:
            return

        # Get the end date
        end_month_date = calendar.monthrange(todays_date.year, todays_date.month)[1]
        days_before = end_month_date - todays_date.day

        # Get data and process
        scheduled_objects = ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency="X Days before End of the Month",
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

        # Loop through the data and see if the conditions are met
        for scheduled_object in scheduled_objects:
            self.create_object(scheduled_object=scheduled_object)

        return
