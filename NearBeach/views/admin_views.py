from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from NearBeach.forms import AdminAddUserForm, PasswordResetForm
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


