from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import  loader
from NearBeach.forms import *
from .models import *



@login_required(login_url='login')
def line_items(request, quote_id):
    # Load the template
    t = loader.get_template('NearBeach/quote_information_modules/line_items.html')

    # context
    c = {
        'quote_id': quote_id,
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def new_line_item(request,quote_id):
    if request.POST:
        form = new_line_item_form(request.POST, request.FILES)
        if form.is_valid():
            #Current user
            current_user = request.user

            #All data
            products_and_services = form.cleaned_data['products_and_services']
            quantity = form.cleaned_data['quantity']
            product_description = form.cleaned_data['product_description']
            product_cost = form.cleaned_data['product_cost']
            discount_choice = form.cleaned_data['discount_choice']
            discount_percent = form.cleaned_data['discount_percent']
            discount_amount = form.cleaned_data['discount_amount']
            product_price = form.cleaned_data['product_price']
            tax = form.cleaned_data['tax']
            tax_amount = form.cleaned_data['tax_amount']
            total = form.cleaned_data['total']
            product_note = form.cleaned_data['product_note']

            #Instances needed


            #Save line item


        else:
            print(form.errors)

    # Load the template
    t = loader.get_template('NearBeach/quote_information_modules/new_line_item.html')

    # context
    c = {
        'quote_id': quote_id,
        'new_line_item_form': new_line_item_form(),
    }

    return HttpResponse(t.render(c, request))


