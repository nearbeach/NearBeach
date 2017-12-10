from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.http import JsonResponse

@login_required(login_url='login')
def lookup_product(request, product_id):
    #Get Data
    product_results = serializers.serialize(
        'json',
        products_and_services.objects.filter(product_id=product_id),
    )
    return JsonResponse(product_results, safe=False)