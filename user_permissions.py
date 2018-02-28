"""
This python script will return the user's permission level for ANY given permission
"""
import json
from .models import *
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.urls import reverse


def return_user_permission_level(request, group_id,permission_field):
    """

    :param request:
    :param group_id: limits data to a certain group - Null if no group
    :param permission_field: which permission field we will be looking at. The available list is;
        permission_set_id
        permission_set_name
        administration_assign_users_to_groups
        administration_create_groups
        administration_create_permission_sets
        administration_create_users
        assign_campus_to_customer
        associate_project_and_tasks
        customer
        invoice
        invoice_product
        opportunity
        organisation
        organisation_campus
        project
        quote
        requirement
        requirement_link
        task
        documents
        contact_history
        project_history
        task_history
    :param min_permission_level: tells us what is the minimum level the user has to be, if they do not meet this requirement
        then the system will formward them onto the permission denied page. Default is 1 (read only)
    :return:
    """
    #Default NO PERMISSION
    user_permission_level = 0

    #Look into the SQL for that particular field and return it.
    if request.user.is_superuser == True:
        return 4

    """
    TEMP CODE
    ~~~~~~~~~
    field='project_id'
    results = project.objects.filter(is_deleted="FALSE").values(field).aggregate(Max(field))
    results[field + "__max"]
    """


    if group_id == None:
        #There is no group id. Select the max value :)
        user_groups_results = user_groups.objects.filter(
            is_deleted="FALSE",
            username=request.user,
            permission_set__is_deleted="FALSE",
        ).aggregate(Max('permission_set__' + permission_field))
        user_permission_level = user_groups_results['permission_set__' + permission_field + '__max']
    else:
        #There is a group, lets find all permissions connected with this group :)
        group_instance = groups.objects.get(group_id=group_id)

        user_groups_results = user_groups.objects.filter(
            is_deleted="FALSE",
            username=request.user,
            permission_set__is_deleted="FALSE",
            groups_id=group_instance,
        ).aggregate(Max('permission_set__' + permission_field))
        user_permission_level = user_groups_results['permission_set__' + permission_field + '__max']

    return user_permission_level