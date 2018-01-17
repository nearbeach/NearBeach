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
from .namedtuplefetchall import *
from .user_permissions import return_user_permission_level

#import python modules
import datetime, json, simplejson, urllib, urllib2

#permission_set_form

@login_required(login_url='login')
def group_information(request):
    #Load template
    t = loader.get_template('NearBeach/group_information.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def group_information_add_permission_set(request, group_id):
    permission_permission = 0

    if request.session['is_superuser']:
        permission_permission = 4
    else:
        ph_permission = return_user_permission_level(request, None, 'administration_create_groups')
        pb_permission = return_user_permission_level(request, None, 'administration_create_permission_sets')

        #Permission takes the highest from both
        if ph_permission > permission_permission:
            permission_permission = ph_permission

        if pb_permission > permission_permission:
            permission_permission = pb_permission

    if permission_permission == 0:
        return HttpResponseRedirect(reverse('permission_denied'))


    if request.method == "POST" and permission_permission > 2:
        submit_group_permissions = group_permissions(
            permission_set = permission_set.objects.get(permission_set_id=request.GET['permission_set']),
            group_id = groups.objects.get(groups_id=group_id),
        )
        submit_group_permissions.save()

    permission_set_results = permission_set.objects.filter(
        is_deleted='FALSE',
    )

    #Load template
    t = loader.get_template('NearBeach/groups/groups_add_permission_set.html')

    # context
    c = {
        'permission_set_results': permission_set_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def group_information_create(request):
    group_permission = 0

    if request.session['is_superuser'] == True:
        group_permission = 4
    else:
        ph_results = return_user_permission_level(request, None, 'administration_create_groups')

        if ph_results > group_permission:
            group_permission = ph_results

    if group_permission < 3:
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
    user_permission = 0
    group_permission = 0

    if request.session['is_superuser'] == True:
        user_permission = 4
        group_permission = 4
    else:
        pp_results = return_user_permission_level(request, None,'administration_assign_users_to_groups')
        ph_results = return_user_permission_level(request, None, 'administration_create_groups')

        if pp_results > user_permission:
            user_permission = pp_results

        if ph_results > group_permission:
            group_permission = ph_results

    if group_permission == 0:
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
        'user_permission': user_permission,
        'group_permission': group_permission,
        'group_id': group_id,
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def group_information_edit_users(request, group_id):
    user_permission = 0

    if request.session['is_superuser'] == True:
        user_permission = 4
    else:
        pp_results = return_user_permission_level(request, None,'administration_assign_users_to_groups')

        if pp_results > user_permission:
            user_permission = pp_results

    if user_permission == 0:
        return HttpResponseRedirect(reverse('permission_denied'))


    if request.method == "POST" and user_permission > 2:
        #Get the new user
        submit_user_groups = user_groups(
            username = User.groups.get(id=request.GET('user_id')),
            permission_set=permission_set.objects.get(permission_set_id=request.GET('permission_set')),
            change_user = request.user
        )
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
        'user_permission': user_permission,
        'permission_set_results': permission_set_results,
        'group_id': group_id,
    }

    # context

    return HttpResponse(t.render(c, request))



@login_required(login_url='login')
def group_information_list(request):
    group_permissions = 0

    if request.session['is_superuser'] == True:
        group_permissions = 4
    else:
        pp_results = return_user_permission_level(request, None,'administration_create_groups')

        if pp_results > group_permissions:
            group_permissions = pp_results

    if group_permissions == 0:
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
def permission_set_information(request):
    permission_set_permission = 0

    if request.session['is_superuser'] == True:
        permission_set_permission = 4
    else:
        pp_results = return_user_permission_level(request, None,'administration_create_permission_sets')


        if pp_results > permission_set_permission:
            permission_set_permission = pp_results


    if permission_set_permission == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    #Load template
    t = loader.get_template('NearBeach/permission_set_information.html')

    # context
    c = {

    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def permission_set_information_create(request):
    permission_set_permission = 0

    if request.session['is_superuser'] == True:
        permission_set_permission = 4
    else:
        pp_results = return_user_permission_level(request, None, 'administration_create_permission_sets')

        if pp_results > permission_set_permission:
            permission_set_permission = pp_results

    if permission_set_permission < 3:
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
    permission_set_permission = 0

    if request.session['is_superuser'] == True:
        permission_set_permission = 4
    else:
        pp_results = return_user_permission_level(request, None, 'administration_create_permission_sets')

        if pp_results > permission_set_permission:
            permission_set_permission = pp_results

    if permission_set_permission < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    save_errors = None
    if request.method == "POST":
        form = permission_set_form(request.POST)
        if form.is_valid():
            # Try and save the form.
            update_permission_set = permission_set.objects.get(permission_set_id=permission_set_id)

            #Bug in python objects - can not update a name if it has the same name.
            #if not update_permission_set.permission_set_name == form.cleaned_data['permission_set_name']:
            #    update_permission_set.permission_set_name = form.cleaned_data['permission_set_name']

            update_permission_set.administration_assign_users_to_groups = form.cleaned_data['administration_assign_users_to_groups']
            update_permission_set.administration_create_groups = form.cleaned_data['administration_create_groups']
            update_permission_set.administration_create_permission_sets = form.cleaned_data['administration_create_permission_sets']
            update_permission_set.administration_create_users = form.cleaned_data['administration_create_users']
            update_permission_set.assign_campus_to_customer = form.cleaned_data['assign_campus_to_customer']
            update_permission_set.associate_project_and_tasks = form.cleaned_data['associate_project_and_tasks']
            update_permission_set.customer = form.cleaned_data['customer']
            update_permission_set.invoice = form.cleaned_data['invoice']
            update_permission_set.invoice_product = form.cleaned_data['invoice_product']
            update_permission_set.opportunity = form.cleaned_data['opportunity']
            update_permission_set.organisation = form.cleaned_data['organisation']
            update_permission_set.organisation_campus = form.cleaned_data['organisation_campus']
            update_permission_set.project = form.cleaned_data['project']
            update_permission_set.requirement = form.cleaned_data['requirement']
            update_permission_set.requirement_link = form.cleaned_data['requirement_link']
            update_permission_set.task = form.cleaned_data['task']
            update_permission_set.documents = form.cleaned_data['documents']
            update_permission_set.contact_history = form.cleaned_data['contact_history']
            update_permission_set.project_history = form.cleaned_data['project_history']
            update_permission_set.task_history = form.cleaned_data['task_history']
            update_permission_set.change_user=request.user

            update_permission_set.save()


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
        'permission_set_id': permission_set_id
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def permission_set_information_list(request):
    permission_set_permission = 0

    if request.session['is_superuser'] == True:
        permission_set_permission = 4
    else:
        pp_results = return_user_permission_level(request, None, 'administration_create_permission_sets')

        if pp_results > permission_set_permission:
            permission_set_permission = pp_results

    if permission_set_permission == 0:
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