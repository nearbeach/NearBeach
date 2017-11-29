from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import  loader

@login_required(login_url='login')
def products_and_services(request, quote_id):
    # Load the template
    t = loader.get_template('NearBeach/quote_information_modules/products_and_services.html')

    # context
    c = {
        'quote_id': quote_id,
    }

    return HttpResponse(t.render(c, request))