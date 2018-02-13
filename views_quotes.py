from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import  loader
from NearBeach.forms import *
from .models import *
from NearBeach.models import *
from django.db.models import Sum, F
from NearBeach.user_permissions import *


@login_required(login_url='login')
def delete_line_item(request, line_item_id):
    # Delete the line item
    line_item = quotes_products_and_services.objects.get(quotes_products_and_services_id = line_item_id)
    line_item.is_deleted = "TRUE"
    line_item.change_user=request.user
    line_item.save()

    #Return a blank page for fun
    t = loader.get_template('NearBeach/blank.html')

    # context
    c = {}

    return HttpResponse(t.render(c, request))
    #SoMuchFun




@login_required(login_url='login')
def list_of_line_items(request, quote_id):
    #Get data
    line_item_results = quotes_products_and_services.objects.filter(
        is_deleted='FALSE',
        quote_id=quote_id,
    )

    product_line_items = quotes_products_and_services.objects.filter(
        quote_id=quote_id,
        products_and_services__product_or_service='Product',
        is_deleted="FALSE",
    )

    service_line_items = quotes_products_and_services.objects.filter(
        quote_id=quote_id,
        products_and_services__product_or_service='Service',
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



@login_required(login_url='login')
def new_line_item(request,quote_id):
    quotes_results = quotes.objects.get(quote_id=quote_id)

    quote_permission = 0

    if request.session['is_superuser'] == True:
        quote_permission = 4
    else:
        pp_results = return_user_permission_level(request, None,'quote')
        print(pp_results)

        if pp_results > quote_permission:
            quote_permission = pp_results

    if request.POST:
        form = new_line_item_form(request.POST, request.FILES)
        if form.is_valid():
            #All data
            extracted_product_and_services = form.cleaned_data['products_and_services']
            quantity = form.cleaned_data['quantity']
            product_description = form.cleaned_data['product_description']
            product_price = form.cleaned_data['product_price']
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
            quote_instance = quotes.objects.get(quote_id=quote_id)
            product_instance = products_and_services.objects.get(product_name = extracted_product_and_services)

            #Check to make sure they are not blank - default = 0
            if ((discount_percent == '') or (not discount_percent)): discount_percent = 0
            if ((discount_amount == '') or (not discount_amount)) : discount_amount = 0


            print("products_and_services: " + str(products_and_services))
            print("quantity: " + str(quantity))
            print("product_description: " + str(product_description))
            print("product_price: " + str(product_price))
            print("discount_choice: " + str(discount_choice))
            print("discount_percent: " + str(discount_percent))
            print("discount_amount: " + str(discount_amount))
            print("product_price: " + str(product_price))
            print("tax: " + str(tax))
            print("tax_amount: " + str(tax_amount))
            print("total: " + str(total))
            print("product_note: " + str(product_note))
            print("quote_id: " + str(quote_instance))


            #Save line item
            submit_line_item = quotes_products_and_services(
                products_and_services = product_instance,
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
        'quote_permission': quote_permission,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def responsible_customer(request,quote_id, customer_id=''):
    if request.method == "POST":
        if customer_id == '':
            return HttpResponseBadRequest("Customer ID is required!")

        customer_instance = customers.objects.get(customer_id=customer_id)
        quote_instance = quotes.objects.get(quote_id=quote_id)

        responsible_customer_save = quote_responsible_customers(
            customer_id=customer_instance,
            quote_id=quote_instance,
            change_user=request.user,
        )
        responsible_customer_save.save()
    #Get data
    responsible_customer_results = customers.objects.filter(
        customer_id__in=quote_responsible_customers.objects.filter(
            quote_id=quote_id,
            is_deleted="FALSE"
        ).values('customer_id').distinct())

    quote_results = quotes.objects.get(quote_id=quote_id)

    if not quote_results.project_id == None:
        customer_results = customers.objects.filter(
            organisations_id=quote_results.project_id.organisations_id.organisations_id)
    elif not quote_results.task_id == None:
        customer_results = customers.objects.filter(
            organisations_id=quote_results.task_id.organisations_id.organisations_id)
    elif not quote_results.opportunity_id == None:
        customer_results = customers.objects.filter(organisations_id=quote_results.opportunity_id.organisations_id.organisations_id)

    # Load the template
    t = loader.get_template('NearBeach/quote_information/responsible_customer.html')

    # context
    c = {
        'quote_id': quote_id,
        'customer_results': customer_results,
        'responsible_customer_results': responsible_customer_results,

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