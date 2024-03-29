# Generated by Django 5.0 on 2023-12-27 06:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def initialise_data(apps, schema_editor):
    """
    This will insert the default status for both projects and tasks.
    """
    db_alias = schema_editor.connection.alias

    # Projects
    list_of_project_status = apps.get_model("NearBeach", "ListOfProjectStatus")
    list_of_project_status.objects.using(db_alias).bulk_create(
        [
            list_of_project_status(
                project_status_id=1,
                project_status="New",
                project_higher_order_status="Backlog",
                project_status_order=1
            ),
            list_of_project_status(
                project_status_id=2,
                project_status="Backlog",
                project_higher_order_status="Backlog",
                project_status_order=2
            ),
            list_of_project_status(
                project_status_id=3,
                project_status="Blocked",
                project_higher_order_status="Blocked",
                project_status_order=3
            ),
            list_of_project_status(
                project_status_id=4,
                project_status="In Progress",
                project_higher_order_status="Normal",
                project_status_order=4
            ),
            list_of_project_status(
                project_status_id=5,
                project_status="Test/Review",
                project_higher_order_status="Normal",
                project_status_order=5
            ),
            list_of_project_status(
                project_status_id=6,
                project_status="Closed",
                project_higher_order_status="Closed",
                project_status_order=6
            ),
        ]
    )

    # Tasks
    list_of_task_status = apps.get_model("NearBeach", "ListOfTaskStatus")
    list_of_task_status.objects.using(db_alias).bulk_create(
        [
            list_of_task_status(
                task_status_id=1,
                task_status="New",
                task_higher_order_status="Backlog",
                task_status_order=1,
            ),
            list_of_task_status(
                task_status_id=2,
                task_status="Backlog",
                task_higher_order_status="Backlog",
                task_status_order=2,
            ),
            list_of_task_status(
                task_status_id=3,
                task_status="Blocked",
                task_higher_order_status="Blocked",
                task_status_order=3,
            ),
            list_of_task_status(
                task_status_id=4,
                task_status="In Progress",
                task_higher_order_status="Normal",
                task_status_order=4,
            ),
            list_of_task_status(
                task_status_id=5,
                task_status="Test/Review",
                task_higher_order_status="Normal",
                task_status_order=5,
            ),
            list_of_task_status(
                task_status_id=6,
                task_status="Closed",
                task_higher_order_status="Closed",
                task_status_order=6,
            ),
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("NearBeach", "0019_alter_publiclink_public_link_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="kanbancolumn",
            name="kanban_column_property",
            field=models.CharField(
                choices=[
                    ("Backlog", "Backlog"),
                    ("Normal", "Normal"),
                    ("Blocked", "Blocked"),
                    ("Closed", "Closed"),
                ],
                default="Normal",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="ListOfProjectStatus",
            fields=[
                (
                    "project_status_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("project_status", models.CharField(max_length=100)),
                (
                    "project_higher_order_status",
                    models.CharField(
                        choices=[
                            ("Backlog", "Backlog"),
                            ("Normal", "Normal"),
                            ("Blocked", "Blocked"),
                            ("Closed", "Closed"),
                        ],
                        default="Backlog",
                        max_length=10,
                    ),
                ),
                ("project_status_order", models.PositiveIntegerField(default=0)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "change_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_change_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ListOfTaskStatus",
            fields=[
                (
                    "task_status_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("task_status", models.CharField(max_length=100)),
                (
                    "task_higher_order_status",
                    models.CharField(
                        choices=[
                            ("Backlog", "Backlog"),
                            ("Normal", "Normal"),
                            ("Blocked", "Blocked"),
                            ("Closed", "Closed"),
                        ],
                        default="Backlog",
                        max_length=10,
                    ),
                ),
                ("task_status_order", models.PositiveIntegerField(default=0)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "change_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_change_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RunPython(initialise_data, reverse_code=migrations.RunPython.noop),
    ]
