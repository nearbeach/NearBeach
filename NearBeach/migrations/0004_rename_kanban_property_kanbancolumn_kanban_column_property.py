# Generated by Django 4.1.4 on 2023-02-01 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("NearBeach", "0003_kanbancolumn_kanban_property_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="kanbancolumn",
            old_name="kanban_property",
            new_name="kanban_column_property",
        ),
    ]
