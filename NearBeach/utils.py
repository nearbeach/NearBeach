from NearBeach.models import (
    Group,
    UserGroup,
    Organisation,
    PermissionSet,
)

def initalize_permission_sets(user):
    admin_set = PermissionSet(
        permission_set_name="Administration Permission Set",
        administration_assign_user_to_group=4,
        administration_create_group=4,
        administration_create_permission_set=4,
        administration_create_user=4,
        bug_client=4,
        customer=4,
        kanban_board=4,
        kanban_card=4,
        organisation=4,
        project=4,
        request_for_change=4,
        requirement=4,
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
        permission_set_name="Power Permission Set",
        administration_assign_user_to_group=0,
        administration_create_group=0,
        administration_create_permission_set=0,
        administration_create_user=0,
        bug_client=4,
        customer=4,
        kanban_card=4,
        organisation=4,
        project=4,
        requirement=4,
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
        permission_set_name="Normal Permission Set",
        administration_assign_user_to_group=0,
        administration_create_group=0,
        administration_create_permission_set=0,
        administration_create_user=0,
        bug_client=3,
        customer=3,
        kanban_card=3,
        organisation=3,
        project=3,
        requirement=3,
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
        permission_set_name="Read Only Permission Set",
        administration_assign_user_to_group=0,
        administration_create_group=0,
        administration_create_permission_set=0,
        administration_create_user=0,
        bug_client=1,
        customer=1,
        kanban_card=1,
        organisation=1,
        project=1,
        requirement=1,
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
    if not getattr(user, 'is_superuser', False):
        return

    # Create admin group
    admin_group = Group(
        group_name="Administration",
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
        organisation_name="No Organisation",
        organisation_website="https://nearbeach.org",
        organisation_email="noreply@nearbeach.org",
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
