from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from .namedtuplefetchall import *
import simplejson

@login_required(login_url='login')
def lookup_product(request, product_id):
    product_results = products_and_services.objects.filter(product_id=product_id)
    data = serializers.serialize("json", product_results)
    return HttpResponse(data, content_type='application/json')


@login_required(login_url='login')
def user_permissions(request):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT DISTINCT 
      auth_user.id
    , auth_user.username
    , groups.group_id
    , groups.group_name
    , permission_set.*
    
    FROM
      user_groups JOIN auth_user
        ON auth_user.id = user_groups.username_id
        AND auth_user.id = %s
        
        JOIN permission_set
        ON user_groups.permission_set_id = permission_set.permission_set_id
        --AND permission_set.is_deleted = "FALSE"
        
        JOIN groups
        ON user_groups.groups_id = groups.group_id
        AND groups.is_deleted = "FALSE"
        
      
      
    WHERE 1=1
    
    AND user_groups.is_deleted = "FALSE"
    
    GROUP BY   auth_user.id, groups.group_name
    
    """,[ request.user.id ])
    permission_results = namedtuplefetchall(cursor)

    print(permission_results)

    #__setitem__('USER_PERMISSIONS', permission_results)
    request.session['USER_PERMISSIONS'] = permission_results

    """
    TEMP CODE
    """
    user_permission = request.session['USER_PERMISSIONS']

    """
    END TEMP CODE
    """



    #pset = permission_set.objects.all()
    pset = group_permissions.objects.select_related('permission_set','groups').all()
    data = serializers.serialize("json", pset)
    return HttpResponse(data, content_type="application/json")

