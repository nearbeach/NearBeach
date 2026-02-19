from NearBeach.models.permission.group import Group
from NearBeach.models.permission.permission_set import PermissionSet
from NearBeach.models.organisation import Organisation
from NearBeach.models.user import UserGroup


def initalize_permission_sets(user):
    admin_set = PermissionSet(
        name="Administration Permission Set",
        administration_assign_user_to_group=4,
        administration_create_group=4,
        administration_create_permission_set=4,
        administration_create_user=4,
        customer=4,
        kanban_board=4,
        organisation=4,
        project=4,
        request_for_change=4,
        requirement=4,
        schedule_object=4,
        task=4,
        tag=4,
        document=1,
        kanban_note=1,
        project_note=1,
        task_note=1,
        requirement_note=1,
        requirement_item_note=1,
        change_user=user,
    )
    admin_set.save()

    power_user_set = PermissionSet(
        name="Power Permission Set",
        administration_assign_user_to_group=0,
        administration_create_group=0,
        administration_create_permission_set=0,
        administration_create_user=0,
        customer=4,
        organisation=4,
        project=4,
        requirement=4,
        schedule_object=4,
        task=4,
        tag=4,
        document=1,
        kanban_note=1,
        project_note=1,
        task_note=1,
        requirement_note=1,
        requirement_item_note=1,
        change_user=user,
    )
    power_user_set.save()

    normal_set = PermissionSet(
        name="Normal Permission Set",
        administration_assign_user_to_group=0,
        administration_create_group=0,
        administration_create_permission_set=0,
        administration_create_user=0,
        customer=3,
        organisation=3,
        project=3,
        requirement=3,
        schedule_object=1,
        task=3,
        tag=3,
        document=1,
        kanban_note=1,
        project_note=1,
        task_note=1,
        requirement_note=1,
        requirement_item_note=1,
        change_user=user,
    )
    normal_set.save()

    read_only_set = PermissionSet(
        name="Read Only Permission Set",
        administration_assign_user_to_group=0,
        administration_create_group=0,
        administration_create_permission_set=0,
        administration_create_user=0,
        customer=1,
        organisation=1,
        project=1,
        requirement=1,
        schedule_object=0,
        task=1,
        tag=1,
        document=1,
        kanban_note=1,
        project_note=1,
        task_note=1,
        requirement_note=1,
        requirement_item_note=1,
        change_user=user,
    )
    read_only_set.save()

    return {
        "admin": admin_set,
        "power": power_user_set,
        "normal": normal_set,
        "read_only": read_only_set,
    }


def initalize_admin_user(user, permission_set):
    if not getattr(user, "is_superuser", False):
        return

    # Create admin group
    admin_group = Group(
        name="Administration",
        change_user=user,
    )
    admin_group.save()

    # Add user to admin group
    admin_user_group = UserGroup(
        username=user,
        group=admin_group,
        permission_set=permission_set,
        change_user=user,
    )
    admin_user_group.save()


def initalize_org(user):
    # Create no organisation
    submit_organisation = Organisation(
        name="No Organisation",
        website="https://nearbeach.org",
        email="noreply@nearbeach.org",
        change_user=user,
    )
    submit_organisation.save()


def initalize_base_values(user):
    if not PermissionSet.objects.all():
        initalize_permission_sets(user)

    if not UserGroup.objects.all():
        admin_set = PermissionSet.objects.get(pk=1)
        initalize_admin_user(user, admin_set)

    if not Organisation.objects.all():
        initalize_org(user)
