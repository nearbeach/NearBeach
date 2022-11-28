from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from NearBeach.decorators.check_user_permissions import check_user_customer_permissions
from NearBeach.models import customer, document, document_permission, list_of_title, organisation
from NearBeach.forms import CustomerForm, NewCustomerForm, ProfilePictureForm
from NearBeach.views.document_views import handle_file_upload, set_object_from_destination

import boto3

@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=1)
def customer_information(request, customer_id, *args, **kwargs):
    """
    :param request:
    :param customer_id:
    :return:
    """
    # Find out if the user is read only - if they are send them to the read only

    # Get customer data
    customer_results = customer.objects.get(customer_id=customer_id)

    organisation_results = organisation.objects.filter(
        organisation_id=customer_results.organisation_id,
    )

    title_list = list_of_title.objects.filter()

    # Get tempalte
    t = loader.get_template("NearBeach/customers/customer_information.html")

    # Context
    c = {
        "customer_results": serializers.serialize("json", [customer_results]),
        "nearbeach_title": f"Customer Information {customer_id}",
        "organisation_results": serializers.serialize("json", organisation_results),
        "title_list": serializers.serialize("json", title_list),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=2)
def customer_information_save(request, customer_id, *args, **kwargs):
    """
    :param request:
    :param customer_id:
    :return:
    """
    # ADD IN USER PERMISSION CHECKS

    # Get form data
    form = CustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the customer instance
    customer_results = customer.objects.get(customer_id=customer_id)

    # Update the fields
    customer_results.customer_title = form.cleaned_data["customer_title"]
    customer_results.customer_first_name = form.cleaned_data["customer_first_name"]
    customer_results.customer_last_name = form.cleaned_data["customer_last_name"]
    customer_results.customer_email = form.cleaned_data["customer_email"]

    # Save
    customer_results.save()

    # Return back a sucessful statement
    return HttpResponse("Success")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=2)
def customer_update_profile(request, customer_id, *args, **kwargs):
    """ """
    form = ProfilePictureForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Method
    # 1. Create a private document (table document)
    # 2. Connect the document foreign key to the customer
    # Notes - the permissions will check both customers/organisations
    # to see if this image is connected to them - if it is pass check
    file = form.cleaned_data["file"]
    document_description = str(file)

    # Add the document row
    document_submit = document(
        change_user=request.user,
        document_description=document_description,
    )
    document_submit.save()

    # Add the document location
    document_submit.document = f"private/{document_submit.document_key}/{file}"
    document_submit.save()

    # Add the document permission row
    document_permission_submit = document_permission(
        change_user=request.user,
        document_key=document_submit,
    )
    document_permission_submit = set_object_from_destination(
        document_permission_submit, "customer", customer_id
    )
    document_permission_submit.save()

    # Get current document results to send back
    document_results = document_permission.objects.filter(
        is_deleted=False,
        document_key=document_submit,
    ).values(
        "document_key_id",
        "document_key__document_description",
        "document_key__document_url_location",
        "document_key__document",
        "folder",
    )

    # Handle the document upload
    if hasattr(settings, "AWS_ACCESS_KEY_ID"):
        # Use boto to upload the file
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        # Upload a new file
        s3.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            f"private/{document_submit.document_key}/{file}",
        )
    else:
        print("Before Handle file upload")
        handle_file_upload(request.FILES["file"], document_results, file)
        print("After Handle File Upload")

    # Update the customer
    print("Update Customer")
    update_customer = customer.objects.get(customer_id=customer_id)
    update_customer.customer_profile_picture = document_submit
    update_customer.save()
    print("Customer Updated")

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def get_profile_picture(request, customer_id):
    """
    :param request:
    :param customer_id:
    :return:
    """
    customer_results = customer.objects.get(customer_id=customer_id)

    # Just return the customer profile picture
    return HttpResponse(
        f"/private/{customer_results.customer_profile_picture.document_key}"
    )


@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=3)
def new_customer(request, *args, **kwargs):
    """
    :param request:
    :return:
    """
    # Get user permission

    # Get data
    title_list = list_of_title.objects.filter(
        is_deleted=False,
    )

    # Get templates
    t = loader.get_template("NearBeach/customers/new_customers.html")

    # Get Context
    c = {
        "nearbeach_title": "New Customer",
        "title_list": serializers.serialize("json", title_list),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=2)
def new_customer_save(request, *args, **kwargs):
    """
    :param reqeust:
    :return:
    """
    # CHECK USER PERMISSIONS -- NEED TO ADD THIS IN!

    # Get Form data
    form = NewCustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    customer_submit = customer(
        change_user=request.user,
        customer_title=form.cleaned_data["customer_title"],
        customer_first_name=form.cleaned_data["customer_first_name"],
        customer_last_name=form.cleaned_data["customer_last_name"],
        customer_email=form.cleaned_data["customer_email"],
    )

    # If the organisation is not null in the form - set the data
    if form.cleaned_data["organisation"]:
        customer_submit.organisation = form.cleaned_data["organisation"]

    # Save the data
    customer_submit.save()

    # Send back the URL to the new customer
    return HttpResponse(
        reverse("customer_information", args={customer_submit.customer_id})
    )
