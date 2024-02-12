from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from NearBeach.decorators.check_user_permissions.object_permissions import check_specific_object_permissions
from NearBeach.decorators.check_user_permissions.admin_permissions import check_user_admin_permissions
from NearBeach.forms import Tag, NewTagForm, TagForm


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_admin_permissions(min_permission_level=4, permission_lookup="tag")
def delete_tag(request, tag_id, *args, **kwargs):
    # Delete Tag
    update_tag = Tag.objects.get(tag_id=tag_id)
    update_tag.is_deleted = True
    update_tag.save()

    # Return blank
    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=3, object_lookup="tag")
def new_tag(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Get form data
    form = NewTagForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create a new tag
    submit_tag = Tag(
        tag_name=form.cleaned_data["tag_name"],
        tag_colour=form.cleaned_data["tag_colour"],
        tag_text_colour=form.cleaned_data["tag_text_colour"],
        change_user=request.user,
    )
    submit_tag.save()

    # Get the object and send back to the users
    tag_result = Tag.objects.get(tag_id=submit_tag.tag_id)

    return HttpResponse(
        serializers.serialize("json", [tag_result]), content_type="application/json"
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_specific_object_permissions(min_permission_level=2, object_lookup="tag")
def save_tag(request, *args, **kwargs):
    """
    :param request:
    :param task_id:
    :return:
    """
    # Get form data
    form = TagForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the data to manipulate
    update_tag = Tag.objects.get(tag_id=form.cleaned_data["tag_id"])

    # Update the required fields
    update_tag.tag_name = form.cleaned_data["tag_name"]
    update_tag.tag_colour = form.cleaned_data["tag_colour"]
    update_tag.tag_text_colour = form.cleaned_data["tag_text_colour"]
    update_tag.change_user = request.user

    # Save data
    update_tag.save()

    return HttpResponse("")
