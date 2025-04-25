from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from NearBeach.decorators.check_user_permissions.customer_permissions import check_user_customer_permissions
from NearBeach.forms import CustomerForm, NewCustomerForm, ProfilePictureForm
from NearBeach.models import Customer, ListOfTitle, Organisation, ObjectAssignment
from NearBeach.views.document_views import handle_document_permissions
from NearBeach.views.theme_views import get_theme


@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=1)
def customer_information(request, customer_id, *args, **kwargs):
    """
    Render the customer information page
    :param request:
    :param customer_id: the customer information we want to render
    :return: Customer Information page
    """
    # Find out if the user is read only - if they are send them to the read only

    # Get customer data
    customer_results = Customer.objects.filter(
        customer_id=customer_id,
        is_deleted=False
    )
    if len(customer_results) == 0:
        raise Http404

    customer_results = customer_results[0]

    organisation_results = Organisation.objects.filter(
        organisation_id=customer_results.organisation_id,
    )

    title_list = ListOfTitle.objects.filter()

    # Get tempalte
    t = loader.get_template("NearBeach/customers/customer_information.html")

    # Context
    c = {
        "customer_results": serializers.serialize("json", [customer_results]),
        "nearbeach_title": f"Customer Information {customer_id}",
        "need_tinymce": False,
        "organisation_results": serializers.serialize("json", organisation_results),
        "theme": get_theme(request),
        "title_list": serializers.serialize("json", title_list),
        "user_level": kwargs["user_level"],
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=4)
def customer_information_delete(request, customer_id, *args, **kwargs):
    """
    Delete the customer
    """
    Customer.objects.filter(
        customer_id=customer_id
    ).update(
        is_deleted=True,
    )

    # Delete any object association with this customer
    ObjectAssignment.objects.filter(
        is_deleted=False,
        customer_id=customer_id,
    ).update(
        is_deleted=True
    )

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=2)
def customer_information_save(request, customer_id, *args, **kwargs):
    """
    Save the customer information
    :param request:
    :param customer_id: The id of the customer we want to save
    :return: Success 200
    """
    # ADD IN USER PERMISSION CHECKS

    # Get form data
    form = CustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the customer instance
    customer_results = Customer.objects.get(customer_id=customer_id)

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
    """
    The node which will update a customer's profile picture
    :param: customer_id: The customer's id who we are updating the picture for
    :return: Success 200
    """
    form = ProfilePictureForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    file = form.cleaned_data["file"]
    document_description = str(file)

    # Check file size
    if file.size > 250 * 1024:
        return HttpResponseBadRequest("File size too large")

    # Upload the document
    document_submit, _ = handle_document_permissions(
        request,
        request.FILES["file"],
        file,
        document_description,
        "customer",
        customer_id,
        0,
        True,
    )

    # Update the customer
    update_customer = Customer.objects.get(customer_id=customer_id)
    update_customer.customer_profile_picture = document_submit
    update_customer.save()

    return HttpResponse("")


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
def get_profile_picture(request, customer_id):
    """
    Wrapper for the profile picture - profile pictures are hidden through the private
    document method
    :param request:
    :param customer_id: The customer id who's profile we want to view
    :return:
    """
    customer_results = Customer.objects.get(customer_id=customer_id)

    # Just return the customer profile picture
    return HttpResponse(
        f"/private/{customer_results.customer_profile_picture.document_key}"
    )


@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=3)
def new_customer(request, *args, **kwargs):
    """
    Loads up the new customer page
    :param request:
    :return:
    """
    # Get user permission

    # Get data
    title_list = ListOfTitle.objects.filter(
        is_deleted=False,
    )

    # Get templates
    t = loader.get_template("NearBeach/customers/new_customers.html")

    # Get Context
    c = {
        "need_tinymce": False,
        "nearbeach_title": "New Customer",
        "title_list": serializers.serialize("json", title_list),
        "theme": get_theme(request),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url="login", redirect_field_name="")
@check_user_customer_permissions(min_permission_level=2)
def new_customer_save(request, *args, **kwargs):
    """
    Saves the new customer
    :param reqeust:
    :return:
    """
    # CHECK USER PERMISSIONS -- NEED TO ADD THIS IN!

    # Get Form data
    form = NewCustomerForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    customer_submit = Customer(
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
