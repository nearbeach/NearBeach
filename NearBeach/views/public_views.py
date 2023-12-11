from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from NearBeach.decorators.check_destination import check_destination
from NearBeach.views.object_data_views import set_object_from_destination, get_object_from_destination
from NearBeach.models import PublicLink
from NearBeach.forms import PublicLinkDeleteForm, PublicLinkUpdateForm

import json

@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@csrf_protect
@check_destination()
def create_public_link(request, destination, location_id):
    # Create new public link
    submit_public_link = PublicLink(
        change_user=request.user,
    )

    # Assign to the destination/location
    submit_public_link = set_object_from_destination(
        submit_public_link, destination, location_id
    )

    # Save
    submit_public_link.save()

    # Return the data we have
    public_link_results = get_public_link_results(destination, location_id)

    return HttpResponse(
        public_link_results,
        content_type="application/json",
    )


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def delete_public_link(request):
    form = PublicLinkDeleteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Delete the data
    PublicLink.objects.filter(
        public_link_id=form.cleaned_data["public_link_id"],
    ).update(
        is_deleted=True,
    )

    return HttpResponse()


# Internal function
def get_public_link_results(destination, location_id):
    public_link_results = PublicLink.objects.filter(
        is_deleted=False,
    )

    public_link_results = get_object_from_destination(
        public_link_results, destination, location_id
    )

    # Shape the data
    public_link_results = public_link_results.values(
        "public_link_id",
        "public_link_is_active",
    )

    # Send back json data
    return json.dumps(list(public_link_results), cls=DjangoJSONEncoder)


@login_required(login_url="login", redirect_field_name="")
@check_destination()
def get_public_links(request, destination, location_id):
    # Return the data we have
    public_link_results = get_public_link_results(destination, location_id)

    return HttpResponse(
        public_link_results,
        content_type="application/json"
    )


@check_destination()
def public_link(request, destination, location_id, public_link_id):
    return HttpResponse()


@login_required(login_url="login", redirect_field_name="")
def update_public_link(request):
    form = PublicLinkUpdateForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Update the data
    PublicLink.objects.filter(
        public_link_id=form.cleaned_data["public_link_id"],
    ).update(
        public_link_is_active=form.cleaned_data["public_link_is_active"]
    )

    return HttpResponse()
