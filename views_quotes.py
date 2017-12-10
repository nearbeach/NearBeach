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
    #test_form = test()

    # Load the template
    t = loader.get_template('NearBeach/quote_information_modules/new_line_item.html')

    # context
    c = {
        'quote_id': quote_id,
        'new_line_item_form': new_line_item_form(),
    }

    return HttpResponse(t.render(c, request))


