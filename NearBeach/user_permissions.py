"""
This python script will return the user's permission level for ANY given permission
"""
import json
from .models import *
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.urls import reverse

"""
Permission table
0 - No permission
1 - Read only
2 - Edit permission
3 - Create permission
4 - Admin/Delete permission
"""
def return_user_permission_level(request, group_list,permission_field):
    """

    :param request:
    :param group: limits data to a certain group - Null if no group
    :param permission_field: which permission field we will be looking at. The available list is;
        permission_set_id
        permission_set_name
        administration_assign_users_to_group
        administration_create_group
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
        request_for_change
        requirement
        requirement_link
        task
        document
        contact_history
        project_history
        task_history

        Please note - if you want to look up more than ONE permission, please include them in [] brackets. For example if
        you would like to look up; project, project_history, and document, then you would use ['project','project_history','document']
    :param min_permission_level: tells us what is the minimum level the user has to be, if they do not meet this requirement
        then the system will formward them onto the permission denied page. Default is 1 (read only)
    :return:
    """

    #Make sure the permission_field is an array/list
    if not isinstance(permission_field, list):
        permission_field = [permission_field]

    #Default NO PERMISSION
    user_permission_level = {}

    """
    If the user is a superuser, we will return 4 no matter what. This part of the script will see if the user is actually
    a super user. If they are then it will return 4 for everything.
    """
    if request.user.is_superuser == True:
        #Add 4 to all permissions
        for row in permission_field:
            user_permission_level[row] = 4
        #User can add new items and do administration
        user_permission_level['new_item'] = 4
        user_permission_level['administration'] = 4
        return user_permission_level

    """
    We are now left with the normal users. We will need to first check to see if there are any groups that have been
    passed through. If no groups, then we check the max permission for those attributes.
    
    If the groups have been passed through, we will check to make sure that the end user has permissions for those 
    particular groups against those particular permission sets.
    """
    for row in permission_field:
        """
        We want to break out of this for loop if the entry is "". This should only occur when the user is looking at their
        profile. The user does not need permission to look at their profile.
        """
        if row == "":
            break


        #Users have no groups
        if group_list == None:
            #There is no group. Select the max value :)
            user_groups_results = user_group.objects.filter(
                is_deleted="FALSE",
                username=request.user,
                permission_set__is_deleted="FALSE",
            ).aggregate(Max('permission_set__' + row))
            user_permission_level[row] = user_groups_results['permission_set__' + row + '__max']
        else:
            #There is a group, lets find all permissions connected with this group :) and return the max :)
            #Default is 0
            group_permission = 0
            for group_id in group_list:
                #Grab user's permission for that group
                user_groups_results = user_group.objects.filter(
                    is_deleted="FALSE",
                    username=request.user,
                    permission_set__is_deleted="FALSE",
                    group_id=group_id['group_id'],
                ).aggregate(Max('permission_set__' + row))

                #Get the max value for the permission
                if not user_groups_results['permission_set__' + row + '__max'] == None:
                    if group_permission < user_groups_results['permission_set__' + row + '__max']:
                        group_permission = user_groups_results['permission_set__' + row + '__max']


            user_permission_level[row] = group_permission


    """
    The following code is for the menu. We will need to find out if a user can actually ADD any items and do any
    administration.
    """
    permission_results = user_group.objects.filter(
        is_deleted="FALSE",
        username=request.user,
        permission_set__is_deleted="FALSE",
    ).aggregate(
        Max('permission_set__project'),
        Max('permission_set__task'),
        Max('permission_set__requirement'),
        Max('permission_set__request_for_change'),
        Max('permission_set__organisation'),
        Max('permission_set__customer'),
        Max('permission_set__administration_assign_user_to_group'),
        Max('permission_set__administration_create_group'),
        Max('permission_set__administration_create_permission_set'),
        Max('permission_set__administration_create_user'),
    )

    user_permission_level['new_item'] = max(
        permission_results['permission_set__project__max'],
        permission_results['permission_set__task__max'],
        permission_results['permission_set__requirement__max'],
        permission_results['permission_set__organisation__max'],
        permission_results['permission_set__customer__max'],
    )
    user_permission_level['administration'] = max(
        permission_results['permission_set__administration_assign_user_to_group__max'],
        permission_results['permission_set__administration_create_group__max'],
        permission_results['permission_set__administration_create_permission_set__max'],
        permission_results['permission_set__administration_create_user__max'],
    )
    #END TEMP CODE

    return user_permission_level