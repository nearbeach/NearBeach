from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import  loader
from NearBeach.forms import *
from .models import *
from NearBeach.models import *
from django.db.models import Sum, F
from NearBeach.user_permissions import *


@login_required(login_url='login',redirect_field_name="")
def delete_line_item(request, line_item_id):
    # Delete the line item
    line_item = quote_product_and_service.objects.get(quotes_product_and_service_id = line_item_id)
    line_item.is_deleted = "TRUE"
    line_item.change_user=request.user
    line_item.save()

    #Return a blank page for fun
    t = loader.get_template('NearBeach/blank.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))
    #SoMuchFun


@login_required(login_url='login',redirect_field_name="")
def delete_responsible_customer(request,quote_id,customer_id):
    if request.method == "POST":
        quote_responsible_customer.objects.filter(
            is_deleted="FALSE",
            quote_id=quote.objects.get(quote_id=quote_id),
            customer_id=customer.objects.get(customer_id=customer_id)
        ).update(is_deleted="TRUE")
        #Return a blank page for fun
        t = loader.get_template('NearBeach/blank.html')

        # context
        c = {}

        return HttpResponse(t.render(c, request))
        #SoMuchFun
    else:
        return HttpResponseBadRequest("Delete Responsible Customer has to be done in POST")


@login_required(login_url='login',redirect_field_name="")
def list_of_line_items(request, quote_id):
    #Get data
    line_item_results = quote_product_and_service.objects.filter(
        is_deleted='FALSE',
        quote_id=quote_id,
    )

    product_line_items = quote_product_and_service.objects.filter(
        quote_id=quote_id,
        product_and_service__product_or_service='Product',
        is_deleted="FALSE",
    )

    service_line_items = quote_product_and_service.objects.filter(
        quote_id=quote_id,
        product_and_service__product_or_service='Service',
        is_deleted="FALSE",
    )


    # Load the template
    t = loader.get_template('NearBeach/quote_information/list_of_line_items.html')

    # context
    c = {
        'quote_id': quote_id,
        'line_item_results': line_item_results,
        'product_line_items': product_line_items,
        'service_line_items': service_line_items,
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login',redirect_field_name="")
def new_line_item(request,quote_id):
    quotes_results = quote.objects.get(quote_id=quote_id)

    permission_results =  return_user_permission_level(request, None,'quote')

    if request.POST:
        form = new_line_item_form(request.POST, request.FILES)
        if form.is_valid():
            #All data
            extracted_product_and_services = form.cleaned_data['product_and_service']
            quantity = form.cleaned_data['quantity']
            product_description = form.cleaned_data['product_description']
            discount_choice = form.cleaned_data['discount_choice']
            discount_percent = form.cleaned_data['discount_percent']
            discount_amount = form.cleaned_data['discount_amount']
            sales_price = form.cleaned_data['sales_price']
            product_price = form.cleaned_data['product_price']
            tax = form.cleaned_data['tax']
            tax_amount = form.cleaned_data['tax_amount']
            total = form.cleaned_data['total']
            product_note = form.cleaned_data['product_note']

            #Instances needed
            quote_instance = quote.objects.get(quote_id=quote_id)
            product_instance = product_and_service.objects.get(product_name = extracted_product_and_services)

            #Check to make sure they are not blank - default = 0
            if ((discount_percent == '') or (not discount_percent)): discount_percent = 0
            if ((discount_amount == '') or (not discount_amount)) : discount_amount = 0

            #Save line item
            submit_line_item = quote_product_and_service(
                product_and_service = product_instance,
                quantity = quantity,
                product_description = product_description,
                product_cost = product_instance.product_cost,
                discount_choice = discount_choice,
                discount_percent = discount_percent,
                discount_amount = discount_amount,
                product_price = product_price,
                tax = tax,
                tax_amount = tax_amount,
                total = total,
                product_note = product_note,
                change_user=request.user,
                quote_id=quote_instance.quote_id,
                sales_price=sales_price,
            )
            submit_line_item.save()



        else:
            print(form.errors)

    # Load the template
    t = loader.get_template('NearBeach/quote_information/new_line_item.html')

    # context
    c = {
        'quote_id': quote_id,
        'new_line_item_form': new_line_item_form(),
        'quote_permission': permission_results['quote'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login',redirect_field_name="")
def responsible_customer(request,quote_id, customer_id=''):
    permission_results = return_user_permission_level(request, None,'quote')

    if request.method == "POST":
        if customer_id == '':
            return HttpResponseBadRequest("Customer ID is required!")

        customer_instance = customer.objects.get(customer_id=customer_id)
        quote_instance = quote.objects.get(quote_id=quote_id)

        responsible_customer_save = quote_responsible_customer(
            customer_id=customer_instance,
            quote_id=quote_instance,
            change_user=request.user,
        )
        responsible_customer_save.save()
    #Get data
    responsible_customer_results = customer.objects.filter(
        customer_id__in=quote_responsible_customer.objects.filter(
            quote_id=quote_id,
            is_deleted="FALSE"
        ).values('customer_id').distinct())

    quote_results = quote.objects.get(quote_id=quote_id)


    """
    Obtain a list of all customer depending where the quote is connected to
    """
    if not quote_results.project_id == None:
        try:
            customer_results = customer.objects.filter(
                organisation_id=quote_results.project_id.organisation_id_id,
            ).exclude(customer_id__in=responsible_customer_results.values('customer_id'),)
        except:
            customer_results = None
    elif not quote_results.organisation_id == None:
        customer_results = customer.objects.filter(
            organisation_id=quote_results.organisation_id_id
        ).exclude(customer_id__in=responsible_customer_results.values('customer_id'),)
    elif not quote_results.task_id == None:
        customer_results = customer.objects.filter(
            customer_id__in=task_customer.objects.filter(
                is_deleted="FALSE",
                task_id=quote_results.task_id_id,
            ).values('customer_id')
        ).exclude(customer_id__in=responsible_customer_results.values('customer_id'))
    elif not quote_results.opportunity_id == None:
        try:
            customer_results = customer.objects.filter(
                organisation_id=quote_results.opportunity_id.organisation_id.organisation_id
            ).exclude(customer_id__in=responsible_customer_results.values('customer_id'),)
        except:
            try:
                customer_results = customer.objects.filter(
                    organisation_id=quote_results.opportunity_id.customer_id.customer_id
                ).exclude(customer_id__in=responsible_customer_results.values('customer_id'),)
            except:
                customer_results = ''
    elif not quote_results.customer_id == None:
        customer_results = customer.objects.filter(
            customer_id=quote_results.customer_id.customer_id
        ).exclude(customer_id__in=responsible_customer_results.values('customer_id'),)
    elif not quote_results.organisation_id == None:
        customer_results = customer.objects.filter(
            organisation_id=quote_results.organisation_id
        ).exclude(customer_id__in=responsible_customer_results.values('customer_id'),)

    # Load the template
    t = loader.get_template('NearBeach/quote_information/responsible_customer.html')

    # context
    c = {
        'quote_id': quote_id,
        'customer_results': customer_results,
        'responsible_customer_results': responsible_customer_results,
        'quote_permission': permission_results['quote'],

    }

    return HttpResponse(t.render(c, request))


# Extra functionality
"""
The following function helps change the cursor's results into useable
SQL that the html templates can read.
"""
from collections import namedtuple
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]