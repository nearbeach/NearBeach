from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("NearBeach", "0017_request_for_change_rfc_status_update"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                (
                    "UPDATE request_for_change SET rfc_status_update_id=rfc_status WHERE 1=1"
                )
            ]
        )
    ]
