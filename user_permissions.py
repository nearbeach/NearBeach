"""
This python script will return the user's permission level for ANY given permission
"""
import json

def return_user_permission_level(request, group_id,permission_section):
    #Default NO PERMISSION
    user_permission_level = 0

    #Get the cookie
    user_permissions = json.loads(request.session['NearBeach_Permissions'])

    for row in user_permissions:
        #Check to see if we are dealing with the correct group
        if row['fields']['groups'][0] == group_id:
            #Obtain the permission level for this group depending on the permission section
            permission_value = row['fields']['permission_set'][permission_section_to_number(permission_section)]

            #If permission_value > user_permission_value, update the later with the former
            if permission_value > user_permission_level:
                user_permission_level = permission_value
        elif group_id == None:
            """
            There is no group associated with this permission. Just navigate through all the permissions
            and determine if the user has access.
            """
            permission_value = row['fields']['permission_set'][permission_section_to_number(permission_section)]

            # If permission_value > user_permission_value, update the later with the former
            if permission_value > user_permission_level:
                user_permission_level = permission_value


    return user_permission_level



def permission_section_to_number(permission_section):
    switcher = {
        "permission_set_id": 0,
        "permission_set_name": 1,
        "administration_assign_users_to_groups": 2,
        "administration_create_groups": 3,
        "administration_create_permission_sets": 4,
        "administration_create_users": 5,
        "assign_campus_to_customer": 6,
        "associate_project_and_tasks": 7,
        "customer": 8,
        "invoice": 9,
        "invoice_product": 10,
        "opportunity": 11,
        "organisation": 12,
        "organisation_campus": 13,
        "project": 14,
        "requirement": 15,
        "requirement_link": 16,
        "task": 17,
        "documents": 18,
        "contact_history": 19,
        "project_history": 20,
        "task_history": 21,
    }
    return switcher.get(permission_section,0)