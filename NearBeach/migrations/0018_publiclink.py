# Generated by Django 5.0 on 2023-12-11 09:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("NearBeach", "0017_tag_tag_text_colour"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PublicLink",
            fields=[
                ("public_link_id", models.UUIDField(primary_key=True, serialize=False)),
                ("public_link_is_active", models.BooleanField(default=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "change_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_change_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "creation_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_creation_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "kanban_board",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.kanbanboard",
                    ),
                ),
                (
                    "kanban_card",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.kanbancard",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.project",
                    ),
                ),
                (
                    "request_for_change",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.requestforchange",
                    ),
                ),
                (
                    "requirement",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.requirement",
                    ),
                ),
                (
                    "requirement_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.requirementitem",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NearBeach.task",
                    ),
                ),
            ],
        ),
    ]
