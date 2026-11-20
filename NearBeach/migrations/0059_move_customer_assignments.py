from django.db import migrations


TARGETS = ("project", "task", "requirement")
OTHER_FIELDS = (
    "assigned_user", "group", "requirement_item", "kanban_board", "kanban_card",
    "request_for_change", "organisation", "change_task", "meta_object",
)
TEXT_FIELDS = ("meta_object_title", "meta_object_status", "link_relationship", "parent_link")
COPY_FIELDS = ("customer", *TARGETS, "creation_user", "change_user")


def copy_rows(source, destination, queryset, alias):
    while batch := list(queryset.order_by("pk")[:500]):
        for row in batch:
            values = {f"{field}_id": getattr(row, f"{field}_id") for field in COPY_FIELDS}
            copied = destination.objects.using(alias).create(is_deleted=row.is_deleted, **values)
            destination.objects.using(alias).filter(pk=copied.pk).update(
                date_created=row.date_created, date_modified=row.date_modified
            )
        source.objects.using(alias).filter(pk__in=[row.pk for row in batch]).delete()


def forward(apps, schema_editor):
    legacy = apps.get_model("NearBeach", "ObjectAssignment")
    dedicated = apps.get_model("NearBeach", "CustomerAssignment")
    alias = schema_editor.connection.alias
    for target in TARGETS:
        rows = legacy.objects.using(alias).filter(
            customer__isnull=False, **{f"{target}__isnull": False}
        )
        pure_rows = rows.filter(
            **{f"{field}__isnull": True for field in (*TARGETS, *OTHER_FIELDS) if field != target},
            **dict.fromkeys(TEXT_FIELDS, ""),
        )
        if rows.count() != pure_rows.count():
            raise RuntimeError(f"Mixed customer assignments found for {target}; review before migrating.")
        copy_rows(legacy, dedicated, pure_rows, alias)


def backward(apps, schema_editor):
    legacy = apps.get_model("NearBeach", "ObjectAssignment")
    dedicated = apps.get_model("NearBeach", "CustomerAssignment")
    alias = schema_editor.connection.alias
    copy_rows(dedicated, legacy, dedicated.objects.using(alias).all(), alias)


class Migration(migrations.Migration):
    dependencies = [("NearBeach", "0058_customer_assignment")]
    operations = [migrations.RunPython(forward, backward, atomic=True)]
