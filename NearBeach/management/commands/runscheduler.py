from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q, F
from NearBeach import event_hooks

from NearBeach.models import (
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
    ScheduledObject,
    Task, Organisation, ListOfTaskStatus, ListOfProjectStatus, ObjectTemplateGroup,
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
        "object_status": "task_status",
        "status": ListOfTaskStatus,
    },
    "project": {
        "object": Project,
        "object_title": "project_name",
        "object_description": "project_description",
        "object_organisation": "organisation",
        "object_start_date": "project_start_date",
        "object_end_date": "project_end_date",
        "object_status": "project_status",
        "status": ListOfProjectStatus,
    }
}

event_hooks.register_event_type("task.create.scheduled_object", Task)
event_hooks.register_event_type("project.create.scheduled_object", Project)

class Command(BaseCommand):
    help = "Run this command to run the scheduled jobs within NearBeach. Setup a daily cron job"

    def handle(self, *args, **kwargs):
        scheduled_objects = ScheduledObject.objects.none()

        # Run each part
        scheduled_objects = scheduled_objects.union(self.run_set_day_of_the_week())
        scheduled_objects = scheduled_objects.union(self.run_weekly())
        scheduled_objects = scheduled_objects.union(self.run_fortnightly())
        scheduled_objects = scheduled_objects.union(self.run_monthly())
        scheduled_objects = scheduled_objects.union(self.run_start_of_the_month())
        scheduled_objects = scheduled_objects.union(self.run_end_of_the_month())
        scheduled_objects = scheduled_objects.union(self.run_x_days_before_end_of_the_month())

        # Loop through all objects and create them
        for single_object in scheduled_objects:
            self.create_object(single_object)

    @staticmethod
    def get_today():
        return datetime.datetime.today()

    @staticmethod
    def create_object(scheduled_object, *args, **kwargs):
        #TODO: Print off a log when creating these tasks/projects

        # Get the template
        template = ObjectTemplate.objects.get(object_template_id=scheduled_object.object_template_id)

        # Get the correct dictionary
        object_string = template.object_template_json["object_type"]
        object_dict = OBJECT_DICT[object_string]

        # Get the start and end date from the template
        template_start_date = datetime.datetime.strptime(
            template.object_template_json["object_start_date"],
            "%Y-%m-%dT%H:%M:%SZ"
        )
        template_end_date = datetime.datetime.strptime(
            template.object_template_json["object_end_date"],
            "%Y-%m-%dT%H:%M:%SZ"
        )

        # Setup the start date for the object
        object_start_date = datetime.datetime.today()
        object_start_date = object_start_date.replace(
            hour=template_start_date.hour,
            minute=template_start_date.minute,
            second=template_start_date.second,
            microsecond=0,
        )

        object_end_date = object_start_date + abs(template_end_date - template_start_date)

        # Organisation
        organisation_instance = Organisation.objects.get(
            organisation_id=template.object_template_json["object_organisation"],
        )

        # Status
        status = object_dict["status"].objects.filter(
            is_deleted=False,
        ).order_by(
            F"{object_string}_status_sort_order",
        ).first()

        # Setup the new template
        submit_object = object_dict["object"](
            change_user=User.objects.get(pk=1),
            creation_user=User.objects.get(pk=1),
            **{
                object_dict["object_title"]: template.object_template_json["object_title"],
                object_dict["object_description"]: template.object_template_json["object_description"],
                object_dict["object_organisation"]: organisation_instance,
                object_dict["object_start_date"]: object_start_date,
                object_dict["object_end_date"]: object_end_date,
                object_dict["object_status"]: status,
            },
        )
        submit_object.save()
        event_hooks.emit(f"{object_string}.create.scheduled_object", submit_object)

        # Loop through the group list and add them
        object_template_groups = ObjectTemplateGroup.objects.filter(
            is_deleted=False,
            object_template_id=template.object_template_id,
        )
        for group in object_template_groups:
            submit_object_assignment = ObjectAssignment(
                change_user=User.objects.get(pk=1),
                group_id_id=group.group_id,
                **{F"{object_string}_id": submit_object.pk }
            )
            submit_object_assignment.save()

        # Update the database for the last run
        scheduled_object.last_run = datetime.date.today()

        # If scheduled object has number of repetes, we increase the run count
        if scheduled_object.number_of_repeats >= 0:
            scheduled_object.run_count = scheduled_object.run_count + 1

        scheduled_object.save()

    def run_set_day_of_the_week(self):
        # Get today's date and day of the week
        todays_date = self.get_today()
        todays_day = calendar.day_name[todays_date.weekday()].lower()
        last_run = todays_date - datetime.timedelta(days=1)

        # Setup blank return query set
        query_set_results = ScheduledObject.objects.none()

        # Get data and process
        potential_scheduled_objects = ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_SET_DAY_OF_THE_WEEK,
                frequency_attribute__isnull=False,
                frequency_attribute__days_of_the_week__isnull=False,
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            ) & Q(
                Q(
                    last_run__isnull=True,
                ) | Q(
                    last_run__lte=last_run,
                )
            ) & Q(
                Q(
                    number_of_repeats=-1,
                ) | Q(
                    number_of_repeats__gte=0,
                    run_count__lte=F('number_of_repeats'),
                )
            )
        )

        # Loop through the potential and then deterine if they should be added to the return result
        for scheduled_object in potential_scheduled_objects:
            # Get JSON value
            frequency_attribute = scheduled_object.frequency_attribute
            days_of_the_week = frequency_attribute['days_of_the_week']

            if todays_day in days_of_the_week:
                # Using the union, we union on a query set of this results
                # I don't like this :'(
                # Refer to this -
                # https://stackoverflow.com/questions/29587382/how-to-add-an-model-instance-to-a-django-queryset
                query_set_results |= ScheduledObject.objects.filter(pk=scheduled_object.pk)

        # Return
        return query_set_results

    def run_weekly(self):
        todays_date = self.get_today()
        day_of_the_week = calendar.day_name[todays_date.weekday()]
        last_run = todays_date - datetime.timedelta(days=7)

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_WEEKLY,
                frequency_attribute__day_of_the_week=day_of_the_week.lower(),
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            ) & Q(
                Q(
                    last_run__isnull=True,
                ) | Q(
                    last_run__lte=last_run,
                )
            ) & Q(
                Q(
                    number_of_repeats=-1,
                ) | Q(
                    number_of_repeats__gte=0,
                    run_count__lte=F('number_of_repeats'),
                )
            )
        )

    def run_fortnightly(self):
        todays_date = self.get_today()
        day_of_the_week = calendar.day_name[todays_date.weekday()]
        last_run = todays_date - datetime.timedelta(days=14)

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_FORTNIGHTLY,
                frequency_attribute__day_of_the_week=day_of_the_week.lower(),
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            ) & Q(
                Q(
                    last_run__isnull=True
                ) | Q(
                    last_run__lte=last_run
                )
            )
        )

    def run_monthly(self):
        todays_date = self.get_today()
        last_run = todays_date - datetime.timedelta(days=14)

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_MONTHLY,
                start_date__lte=todays_date,
                start_date__day=todays_date.day,
                is_active=True,
            ) & Q(
                Q(
                    end_date__gte=todays_date,
                ) | Q(
                    end_date__isnull=True,
                )
            ) & Q(
                Q(
                    last_run__isnull=True
                ) | Q(
                    last_run__lte=last_run
                )
            )
        )

    def run_start_of_the_month(self):
        # If today is not the 1st - we will just leave
        todays_date = self.get_today()
        last_run = todays_date - datetime.timedelta(days=14)
        if todays_date.day != 1:
            return ScheduledObject.objects.none()

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
            ) & Q(
                Q(
                    last_run__isnull=True,
                ) | Q(
                    last_run__lte=last_run,
                )
            )
        )

    def run_end_of_the_month(self):
        # If today is not the end of the month - we will just leave
        todays_date = self.get_today()
        end_month_date = calendar.monthrange(todays_date.year, todays_date.month)[1]
        last_run = todays_date - datetime.timedelta(days=14)
        if todays_date.day != end_month_date:
            return ScheduledObject.objects.none()

        # Get data and process
        return ScheduledObject.objects.filter(
            Q(
                is_deleted=False,
                frequency=SCH_END_OF_THE_MONTH,
                start_date__lte=todays_date,
                is_active=True,
            ) & Q(
                Q(
                    end_date__year__gte=todays_date.year,
                    end_date__month__gte=todays_date.month,
                ) | Q(
                    end_date__isnull=True,
                )
            ) & Q(
                Q(
                    last_run__isnull=True,
                ) | Q(
                    last_run__lte=last_run,
                )
            )
        )

    def run_x_days_before_end_of_the_month(self):
        # If today's date is earlier than the 14th, just leave
        todays_date = self.get_today()
        last_run = todays_date - datetime.timedelta(days=14)
        if todays_date.day < 14:
            return ScheduledObject.objects.none()

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
            ) & Q(
                Q(
                    last_run__isnull=True,
                ) | Q(
                    last_run__lte=last_run,
                )
            )
        )
