from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.forms import ProfilePictureForm, User, UpdateUserForm
from NearBeach.models import UserProfilePicture
from NearBeach.views.theme_views import get_theme, update_theme

import json

from NearBeach.views.document_views import handle_document_permissions


@login_required(login_url="login", redirect_field_name="")
def get_profile_picture(request):
    # Get the user profile
    user_profile = UserProfilePicture.objects.get(username=request.user)

    # Return the JSON
    return JsonResponse(
        {
            "profile_picture": user_profile.document_id,
        }
    )


@login_required(login_url="login", redirect_field_name="")
def profile_information(request):
    """ """
    # Get user data
    user_results = User.objects.filter(username=request.user).values(
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
    )

    user_profile = UserProfilePicture.objects.filter(username=request.user)

    # Get template
    t = loader.get_template("NearBeach/profile/profile_information.html")

    # Construct Context
    c = {
        "nearbeach_title": "Profile Information",
        "user_profile": serializers.serialize("json", user_profile),
        "user_results": json.dumps(list(user_results), cls=DjangoJSONEncoder),
        "need_tinymce": False,
        "theme": get_theme(request),
        "username": request.user.id,
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def update_data(request):
    """ """
    # Get form data
    form = UpdateUserForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the theme
    theme = form.cleaned_data["theme"]
    update_theme(request, theme)

    # Extract out the user results
    user_update = request.user
    user_update.first_name = form.cleaned_data["first_name"]
    user_update.last_name = form.cleaned_data["last_name"]
    user_update.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def update_profile(request):
    # Extract out
    form = ProfilePictureForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    file = form.cleaned_data["file"]
    document_description = str(file)

    # Check file size
    if file.size > 250 * 1024:
        return HttpResponseBadRequest("Profile Picture too large. Please use 250Kb")

    # Upload the document
    document_submit, _ = handle_document_permissions(
        request,
        request.FILES["file"],
        file,
        document_description,
        "user",
        request.user.id,
        0,
        True,
    )

    # Update user profile
    # Determine if there is already a user profile
    user_profile_results = UserProfilePicture.objects.filter(
        username_id=request.user.id
    )

    if len(user_profile_results) == 0:
        # Not profile picture - create one
        user_profile_results = UserProfilePicture(
            username=request.user,
            document=document_submit,
            change_user=request.user,
        )
    else:
        # Profile already exists - so just update it
        user_profile_results = UserProfilePicture.objects.get(
            username_id=request.user.id
        )
        user_profile_results.document = document_submit

    user_profile_results.save()

    return HttpResponse("")
