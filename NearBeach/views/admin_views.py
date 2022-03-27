from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from NearBeach.forms import AdminAddUserForm, PasswordResetForm, UpdateGroupLeaderStatusForm
from NearBeach.models import user_group


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_user(request):
    """
    :param request:
    :return:
    """
    # Add in user permissions

    # Check the form data
    form = AdminAddUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    """
    We can assume that there are;
    - Single User
    - Multiple Groups
    - Multiple Permission Sets

    We need to loop through these permutations, and add them into the database
    """
    # print("Permission Sets %s" % form.cleaned_data['permission_set'])

    group_results = form.cleaned_data['group']
    permission_set_results = form.cleaned_data['permission_set']
    user_results = form.cleaned_data['username']

    # Simple double for loops
    for single_group in group_results:
        for single_permission_set in permission_set_results:
            submit_user = user_group(
                username=user_results,
                permission_set=single_permission_set,
                group=single_group,
                change_user=request.user,
            )
            submit_user.save()

    return HttpResponse("")


@require_http_methods(['POST'])
def update_group_leader_status(request, destination):
    """
    This function will update the user's group leader status against a particular group.
    :param request: Normal stuff.
    :return:
    """
    form = UpdateGroupLeaderStatusForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Start filtering the user_group
    user_group_update = user_group.objects.filter(
        is_deleted=False,
        username=form.cleaned_data['username'],
    )

    # Depending on the destination - depends what else we filter on
    if destination == 'group':
        user_group_update.filter(
            group=form.cleaned_data['group'].first(),
        ).update(group_leader=form.cleaned_data['group_leader'])
    elif destination == 'permission_set':
        user_group_update.filter(
            permission_set=form.cleaned_data['permission_set'].first(),
        ).update(group_leader=form.cleaned_data['group_leader'])

    return HttpResponse("")


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def update_user_password(request):
    """
    """
    # Get form data
    form = PasswordResetForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the User object
    user_update = form.cleaned_data['username']
    user_update.set_password(form.cleaned_data['password'])
    user_update.save()

    return HttpResponse("")
