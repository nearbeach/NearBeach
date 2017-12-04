from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import  loader
from NearBeach.forms import *

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
    test_form = test()

    # Load the template
    t = loader.get_template('NearBeach/quote_information_modules/new_line_item.html')

    # context
    c = {
        'quote_id': quote_id,
        'test_form': test_form,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def products_and_services(request, quote_id):
    # Load the template
    t = loader.get_template('NearBeach/quote_information_modules/products_and_services.html')

    # context
    c = {
        'quote_id': quote_id,
    }

    return HttpResponse(t.render(c, request))