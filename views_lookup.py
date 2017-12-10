from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers


@login_required(login_url='login')
def lookup_product(request, product_id):
    product_results = products_and_services.objects.filter(product_id=product_id)
    data = serializers.serialize("json", product_results)
    return HttpResponse(data, content_type='application/json')
