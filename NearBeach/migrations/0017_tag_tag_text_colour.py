# Generated by Django 4.2.7 on 2023-11-29 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("NearBeach", "0016_document_document_upload_successfully"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="tag_text_colour",
            field=models.CharField(default="#ffffff", max_length=7),
        ),
    ]
