#Import NearBeach Modules
from .forms import *
from .models import *
from .private_media import *

#Import django Modules
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Q, Min
from django.http import HttpResponse,HttpResponseForbidden, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.urls import reverse
from .misc_functions import *
from .user_permissions import return_user_permission_level


#import python modules
import datetime, json, simplejson, urllib, urllib2

#permission_set_form

@login_required(login_url='login')
def group_information(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_groups')

    if permission_results['administration_create_groups'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    #Load template
    t = loader.get_template('NearBeach/group_information.html')

    # context
    c = {
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def group_information_add_permission_set(request, group_id):
    permission_results = return_user_permission_level(request, None, ['administration_create_groups','administration_create_permission_sets'])

    if permission_results['administration_create_groups'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))


    if request.method == "POST" and permission_results['administration_create_groups'] > 2:
        form = add_permission_set_to_group_form(request.POST)
        if form.is_valid():
            submit_group_permission = group_permissions(
                permission_set=form.cleaned_data['permission_set_name'],
                groups=groups.objects.get(group_id=group_id),
            )
            submit_group_permission.save()
            print("SAVED")
        else:
            print(form.errors)


    permission_set_results = permission_set.objects.filter(
        is_deleted='FALSE',
    )

    #Load template
    t = loader.get_template('NearBeach/groups/groups_add_permission_set.html')

    # context
    c = {
        'permission_set_results': permission_set_results,
        'form': add_permission_set_to_group_form,
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def group_information_create(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_groups')

    if permission_results['administration_create_groups'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        form = groups_form(request.POST)
        if form.is_valid():
            submit_group = groups(
                group_name=form.cleaned_data['group_name'],
                change_user=request.user,
            )
            submit_group.save()

        else:
            print(form.errors)
    #Load template
    t = loader.get_template('NearBeach/groups/groups_create.html')

    # context
    c = {
        'groups_form': groups_form(),
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def group_information_edit(request, group_id):
    permission_results = return_user_permission_level(request, None,['administration_assign_users_to_groups','administration_create_groups'])

    if permission_results['administration_create_groups'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        form = groups_form(request.POST, instance=groups.objects.get(group_id=group_id))
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    #Load template
    t = loader.get_template('NearBeach/groups/groups_edit.html')

    # context
    c = {
        'groups_form': groups_form(instance=groups.objects.get(group_id=group_id)),
        'user_permission': permission_results['administration_assign_users_to_groups'],
        'group_permission': permission_results['administration_create_groups'],
        'group_id': group_id,
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def group_information_edit_users(request, group_id):
    permission_results = return_user_permission_level(request, None,'administration_assign_users_to_groups')

    if permission_results['administration_assign_users_to_groups'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))


    if request.method == "POST" and permission_results['administration_assign_users_to_groups'] > 2:
        print(request.POST.get('permission_set'))
        permission_set_instance=permission_set.objects.get(permission_set_id=request.POST.get('permission_set'))
        #Get the new user
        submit_user_groups = user_groups(
            username = User.objects.get(id=request.POST.get('user_id')),
            permission_set=permission_set_instance,
            change_user = request.user,
            #groups_id=groups.objects.get(group_id=group_id),
            groups_id=group_id,
        )
        print("Saving user permissions")
        submit_user_groups.save()

    #List of users in group, and list of users to add
    user_groups_results = user_groups.objects.filter(
        is_deleted="FALSE",
        groups_id=group_id,
    ).order_by('username','permission_set')
    #.distinct().orderby('username','permission_set')
    user_results = User.objects.all()
    permission_set_results = group_permissions.objects.filter(
        #is_deleted='FALSE',
        groups_id=group_id,
    )



    #Load template
    t = loader.get_template('NearBeach/groups/groups_edit_users.html')
    c = {
        'user_groups_results': user_groups_results,
        'user_results': user_results,
        'user_permission': permission_results['administration_assign_users_to_groups'],
        'permission_set_results': permission_set_results,
        'group_id': group_id,
    }

    # context

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def group_information_list(request):
    permission_results = return_user_permission_level(request, None,'administration_create_groups')


    if permission_results['administration_create_groups'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    group_results = groups.objects.filter(
        is_deleted="FALSE"
    )

    #Load template
    t = loader.get_template('NearBeach/groups/groups_list.html')

    # context
    c = {
        'group_results': group_results,
        'group_permissions': group_permissions,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def list_of_taxes_deactivate(request,tax_id):
    if request.method == "POST":
        tax_instance = list_of_taxes.objects.get(tax_id=tax_id)
        if tax_instance.is_deleted == "FALSE":
            tax_instance.is_deleted = "TRUE"
        else:
            tax_instance.is_deleted = "FALSE"
        tax_instance.save()

        #Return blank page
        t = loader.get_template('NearBeach/blank.html')

        c= {}

        return HttpResponse(t.render(c, request))
    else:
        return HttpResponseBadRequest("Sorry, can only be done through POST")


@login_required(login_url='login')
def list_of_taxes_edit(request,tax_id):
    tax_result = list_of_taxes.objects.get(pk=tax_id)
    if request.method == "POST":
        form = list_of_taxes_form(request.POST)
        if form.is_valid():
            tax_result.tax_amount = form.cleaned_data['tax_amount']
            tax_result.tax_description = form.cleaned_data['tax_description']
            tax_result.save()

    #Load template
    t = loader.get_template('NearBeach/list_of_taxes/list_of_taxes_edit.html')

    # context
    c = {
        'list_of_taxes_form': list_of_taxes_form(instance=tax_result),
        'tax_id': tax_id,
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def list_of_taxes_information(request):
    permission_results = return_user_permission_level(request, None, 'tax')

    if permission_results['tax'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    #Load template
    t = loader.get_template('NearBeach/list_of_taxes/list_of_taxes_information.html')

    # context
    c = {
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))




@login_required(login_url='login')
def list_of_taxes_list(request):
    permission_results = return_user_permission_level(request, None, 'tax')

    if permission_results['tax'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    list_of_taxes_results = list_of_taxes.objects.all().order_by('tax_amount') #No taxes are deleted, only disabled.

    #Load template
    t = loader.get_template('NearBeach/list_of_taxes/list_of_taxes_list.html')

    # context
    c = {
        'list_of_taxes_results': list_of_taxes_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def list_of_taxes_new(request):
    if request.method == "POST":
        form = list_of_taxes_form(request.POST)
        if form.is_valid():
            tax_submit = list_of_taxes(
                tax_amount = form.cleaned_data['tax_amount'],
                tax_description = form.cleaned_data['tax_description'],
                change_user = request.user,
            )
            tax_submit.save()
        else:
            print(form.errors)

    #Load template
    t = loader.get_template('NearBeach/list_of_taxes/list_of_taxes_new.html')

    # context
    c = {
        'list_of_taxes_form': list_of_taxes_form()
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def new_user(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_users')

    if permission_results['administration_create_users'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    errors = ''
    if request.method == "POST" and permission_results['administration_create_users'] == 4:
        form = user_information_form(request.POST)

        if form.is_valid():
            form.save()

            """
            For new users
            ~~~~~~~~~~~~~
            - If password fields are left blank, generate random password
            - If password fields do not match, send back errors
            - If password fields match, save password against the new user
            """
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if not password1 == password2:
                errors = '<li>PASSWORDS ARE NOT THE SAME<li>'
            else:
                if password1 == "":
                    # Passwords are blank - generate a new password for the user
                    password1 = User.objects.make_random_password()

                # Save the password
                user_instance = User.objects.get(username=form.cleaned_data['username'])
                user_instance.set_password(password1)
                user_instance.save()

                # Go to the new profile of the user
                return HttpResponseRedirect(reverse('user_information', args={user_instance.id}))

        else:
            print(form.errors)
            errors = form.errors

    #Load template
    t = loader.get_template('NearBeach/new_user.html')

    # context
    c = {
        'user_information_form': user_information_form(),
        'is_superuser': request.session['is_superuser'],
        'errors': errors,
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def permission_set_information(request):
    permission_results = return_user_permission_level(request, None,'administration_create_permission_sets')

    if permission_results['administration_create_permission_sets'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    #Load template
    t = loader.get_template('NearBeach/permission_set_information.html')

    # context
    c = {
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def permission_set_information_create(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_sets')

    if permission_results['administration_create_permission_sets'] < 3:
        return HttpResponseRedirect(reverse('permission_denied'))


    save_errors = None
    print(request.method)
    if request.method == "POST":
        print("POST")
        form = permission_set_form(request.POST)
        if form.is_valid():
            #Try and save the form.
            permission_set_name = form.cleaned_data['permission_set_name']
            administration_assign_users_to_groups = form.cleaned_data['administration_assign_users_to_groups']
            administration_create_groups = form.cleaned_data['administration_create_groups']
            administration_create_permission_sets = form.cleaned_data['administration_create_permission_sets']
            administration_create_users = form.cleaned_data['administration_create_users']
            assign_campus_to_customer = form.cleaned_data['assign_campus_to_customer']
            associate_project_and_tasks = form.cleaned_data['associate_project_and_tasks']
            customer = form.cleaned_data['customer']
            invoice = form.cleaned_data['invoice']
            invoice_product = form.cleaned_data['invoice_product']
            opportunity = form.cleaned_data['opportunity']
            organisation = form.cleaned_data['organisation']
            organisation_campus = form.cleaned_data['organisation_campus']
            project = form.cleaned_data['project']
            requirement = form.cleaned_data['requirement']
            requirement_link = form.cleaned_data['requirement_link']
            task = form.cleaned_data['task']
            documents = form.cleaned_data['documents']
            contact_history = form.cleaned_data['contact_history']
            project_history = form.cleaned_data['project_history']
            task_history = form.cleaned_data['task_history']

            submit_permission_set = permission_set(
                permission_set_name=permission_set_name,
                administration_assign_users_to_groups=administration_assign_users_to_groups,
                administration_create_groups=administration_create_groups,
                administration_create_permission_sets=administration_create_permission_sets,
                administration_create_users=administration_create_users,
                assign_campus_to_customer=assign_campus_to_customer,
                associate_project_and_tasks=associate_project_and_tasks,
                customer=customer,
                invoice=invoice,
                invoice_product=invoice_product,
                opportunity=opportunity,
                organisation=organisation,
                organisation_campus=organisation_campus,
                project=project,
                requirement=requirement,
                requirement_link=requirement_link,
                task=task,
                documents=documents,
                contact_history=contact_history,
                project_history=project_history,
                task_history=task_history,
                change_user=request.user,
            )
            if not submit_permission_set.save():
                save_errors = "Did not save!"
            else:
                #Load blank page
                t = loader.get_template('NearBeach/blank.html')

                c = {
                }

                return HttpResponse(t.render(c,request))


        else:
            print(form.errors)

    # Load template
    t = loader.get_template('NearBeach/permission_set_information/permission_set_create.html')

    # context
    c = {
        'permission_set_form': permission_set_form(request.POST or None),
        'save_errors': save_errors,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def permission_set_information_edit(request, permission_set_id):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_sets')

    if permission_results['administration_create_permission_sets'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    save_errors = None
    if request.method == "POST":
        form = permission_set_form(
            request.POST,
            instance=permission_set.objects.get(permission_set_id=permission_set_id)
        )
        if form.is_valid():
            form.save()

            # Load blank page
            t = loader.get_template('NearBeach/blank.html')

            c = {
            }

            return HttpResponse(t.render(c, request))


        else:
            print(form.errors)

    # Load template
    t = loader.get_template('NearBeach/permission_set_information/permission_set_edit.html')

    permission_set_results = permission_set.objects.get(permission_set_id=permission_set_id)

    initial = {
        'permission_set_name' : permission_set_results.permission_set_name,
        'administration_assign_users_to_groups' : permission_set_results.administration_assign_users_to_groups,
        'administration_create_groups' : permission_set_results.administration_create_groups,
        'administration_create_permission_sets' : permission_set_results.administration_create_permission_sets,
        'administration_create_users' : permission_set_results.administration_create_users,
        'assign_campus_to_customer' : permission_set_results.assign_campus_to_customer,
        'associate_project_and_tasks' : permission_set_results.associate_project_and_tasks,
        'customer' : permission_set_results.customer,
        'invoice' : permission_set_results.invoice,
        'invoice_product' : permission_set_results.invoice_product,
        'opportunity' : permission_set_results.opportunity,
        'organisation' : permission_set_results.organisation,
        'organisation_campus' : permission_set_results.organisation_campus,
        'project' : permission_set_results.project,
        'requirement' : permission_set_results.requirement,
        'requirement_link' : permission_set_results.requirement_link,
        'task' : permission_set_results.task,
        'documents' : permission_set_results.documents,
        'contact_history' : permission_set_results.contact_history,
        'project_history' : permission_set_results.project_history,
        'task_history' : permission_set_results.task_history,
    }

    # context
    c = {
        'permission_set_form': permission_set_form(initial=initial),
        'save_errors': save_errors,
        'permission_set_id': permission_set_id,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def permission_set_information_list(request):
    permission_results =  return_user_permission_level(request, None, 'administration_create_permission_sets')

    if permission_results['administration_create_permission_sets'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    #Get data
    permission_set_results = permission_set.objects.all()

    # Load template
    t = loader.get_template('NearBeach/permission_set_information/permission_set_list.html')

    # context
    c = {
        'permission_set_results': permission_set_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def product_and_service_discontinued(request, product_id):
    product_instance = products_and_services.objects.get(product_id=product_id)

    if product_instance.is_deleted == "FALSE":
        product_instance.is_deleted = "TRUE"
    else:
        product_instance.is_deleted = "FALSE"

    product_instance.save()

    return HttpResponseRedirect(reverse(product_and_service_search))

@login_required(login_url='login')
def product_and_service_edit(request, product_id):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_sets')

    if permission_results['administration_create_permission_sets'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST" and permission_results['administration_create_permission_sets'] > 2:
        form = product_and_service_form(request.POST, instance=products_and_services.objects.get(product_id=product_id))
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse(product_and_service_search))
        else:
            print(form.errors)

    # Load template
    t = loader.get_template('NearBeach/product_and_service/product_and_service_edit.html')

    # context
    c = {
        'product_and_service_form': product_and_service_form(
            instance=products_and_services.objects.get(product_id=product_id)
        ),
        'product_id': product_id,
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def product_and_service_new(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_sets')

    if permission_results['administration_create_permission_sets'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST" and permission_results['administration_create_permission_sets'] > 3:
        form = product_and_service_form(request.POST,)
        if form.is_valid():
            submit_product = products_and_services(
                product_or_service=form.cleaned_data['product_or_service'],
                product_name=form.cleaned_data['product_name'],
                product_part_number=form.cleaned_data['product_part_number'],
                product_cost=form.cleaned_data['product_cost'],
                product_price=form.cleaned_data['product_price'],
                product_description=form.cleaned_data['product_description'],
                change_user=request.user,
            )
            submit_product.save()


            return HttpResponseRedirect(reverse(product_and_service_search))
        else:
            print(form.errors)

    # Load template
    t = loader.get_template('NearBeach/product_and_service/product_and_service_new.html')

    # context
    c = {
        'product_and_service_form': product_and_service_form(),
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))




@login_required(login_url='login')
def product_and_service_search(request):
    permission_results = return_user_permission_level(request, None, 'invoice_product')

    if permission_results['invoice_product'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    #Get Data
    product_results = products_and_services.objects.filter(
        product_or_service='Product',
        #Is deleted becomes 'DISCONTINUED' in the table. We can then recontinue it :)
    )
    service_results = products_and_services.objects.filter(
        product_or_service='Service',
        # Is deleted becomes 'DISCONTINUED' in the table. We can then recontinue it :)
    )

    # Load template
    t = loader.get_template('NearBeach/product_and_service/product_and_service_search.html')

    # context
    c = {
        'product_results': product_results,
        'service_results': service_results,
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))






@login_required(login_url='login')
def search_users(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_users')

    if permission_results['administration_create_users'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    filter_users = ''
    if request.method == "POST":
        form = search_form(request.POST)
        if form.is_valid():
            # EDIT LATER for helping search
            search_for = form.cleaned_data['search_for']
            user_results = User.objects.filter(
                Q(is_active=True),
                Q(username__contains=search_for) | Q(first_name__contains=search_for) | Q(last_name__contains=search_for) | Q(email__contains=search_for),
            )
        else:
            print(form.errors)

    else:
        user_results = User.objects.filter(
            is_active=True,
        )


    # Load template
    t = loader.get_template('NearBeach/search_users.html')

    # context
    c = {
        'user_results': user_results,
        'search_form': search_form(request.POST or None),
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def user_information(request, user_id):
    permission_results = return_user_permission_level(request, None, 'administration_create_users')

    if permission_results['administration_create_users'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    errors = ''
    save_state = ''
    if request.method == "POST" and permission_results['administration_create_users'] == 4:
        if user_id == "":
            form = user_information_form(request.POST)
        else:
            form = user_information_form(
                request.POST,
                instance=User.objects.get(id=user_id),
            )
        if form.is_valid():
            form.save()

            save_state = 'User has been saved'

            """
            For new users
            ~~~~~~~~~~~~~
            - If password fields are left blank, generate random password
            - If password fields do not match, send back errors
            - If password fields match, save password against the new user
            
            For old users
            ~~~~~~~~~~~~~
            - If password fields are blank, nothing to do
            - If password fields do not match, send back error
            - If password fields match, save password against user
            """
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if user_id == "":
                if not password1 == password1:
                    errors = 'PASSWORDS ARE NOT THE SAME'
                else:
                    if password1 == "":
                        #Passwords are blank - generate a new password for the user
                        password1 = User.objects.make_random_password()

                    #Save the password
                    user_instance = User.objects.get(username=form.cleaned_data['username'])
                    user_instance.set_password(password1)
                    user_instance.save()

                    #Go to the new profile of the user
                    return HttpResponseRedirect(reverse('user_information',args={user_instance.id}))

            else:
                if password1 == password2:
                    #Change passwords
                    if not password1 == "":
                        user_instance = User.objects.get(id=user_id)
                        user_instance.set_password(password1)
                        user_instance.save()
                else:
                    errors = 'PASSWORDS ARE NOT THE SAME'
        else:
            print(form.errors)
            errors = form.errors

    #forms
    if user_id == None:
        ui_form = user_information_form()
    else:
        ui_form = user_information_form(
            instance=User.objects.get(id=user_id)
        )

    # Load template
    t = loader.get_template('NearBeach/user_information.html')

    # context
    c = {
        'user_information_form': ui_form,
        'is_superuser': request.session['is_superuser'],
        'errors': errors,
        'user_id': user_id,
        'new_item_permission': permission_results['new_item'],
        'administration_permission': permission_results['administration'],
        'save_state': save_state,
    }

    return HttpResponse(t.render(c, request))