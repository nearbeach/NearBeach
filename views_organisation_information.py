"""
VIEWS - project information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the PROJECT INFORMATION MODULES. This is to help keep the VIEWS
file clean from AJAX (spray and wipe).
"""

from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import  loader
from NearBeach.forms import *
from .models import *
from .misc_functions import *
from .user_permissions import return_user_permission_level
from django.urls import reverse

import simplejson

@login_required(login_url='login')
def information_organisation_contact_history(request, organisation_id):
    organisation_permissions = 0
    contact_history_permission = 0

    if request.session['is_superuser'] == True:
        organisation_permissions = 4
        contact_history_permission = 4
    else:
        pp_results = return_user_permission_level(request, None,'organisation')
        ph_results = return_user_permission_level(request, None, 'contact_history')

        if pp_results > organisation_permissions:
            organisation_permissions = pp_results

        if ph_results == 1:
            contact_history_permission = 1

    if organisation_permissions == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    # Get the data from the form if the information has been submitted
    if request.method == "POST" and organisation_permissions > 1:
        form = information_organisation_contact_history_form(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            """
            If the user has written something in the contact section, we want to save it
            """
            contact_history_notes = form.cleaned_data['contact_history']

            if not contact_history_notes == '':
                # Lets save some contact history
                # organisation_id = form.cleaned_data['organisations_id'] #Not going to work :( #organisations_results.organisations_id
                contact_type = form.cleaned_data['contact_type']

                # Create the final start/end date fields
                contact_date = convert_to_utc(
                    int(form.cleaned_data['start_date_year']),
                    int(form.cleaned_data['start_date_month']),
                    int(form.cleaned_data['start_date_day']),
                    int(form.cleaned_data['start_date_hour']),
                    int(form.cleaned_data['start_date_minute']),
                    form.cleaned_data['start_date_meridiems']
                )

                # documents
                if request.FILES == None:
                    print("No files uploaded in contacts")

                contact_attachment = request.FILES.get('contact_attachment')
                
                if contact_attachment:
                    documents_save = documents(
                        document_description=contact_attachment,
                        document=contact_attachment,
                        change_user=request.user,
                    )
                    documents_save.save()

                    #Add to document permissions
                    document_permissions_save = document_permissions(
                        document_key=documents_save,
                        organisations_id=organisations.objects.get(organisations_id=organisation_id),
                        change_user=request.user,
                    )
                    document_permissions_save.save()
                else:
                    print("There was no document?")


                submit_history = contact_history(
                    organisations_id=organisations.objects.get(organisations_id=organisation_id),
                    contact_type=contact_type,
                    contact_date=contact_date,
                    contact_history=contact_history_notes,
                    user_id=current_user,
                    change_user=request.user,
                    #document_key=documents_save,
                )
                if contact_attachment:
                    submit_history.document_key=documents_save
                submit_history.save()
    #Get data
    contact_history_results = contact_history.objects.filter(
        organisations_id=organisations.objects.get(organisations_id=organisation_id)
    )

    contact_date = datetime.datetime.now()

    #Load template
    t = loader.get_template('NearBeach/organisation_information/organisation_contact_history.html')

    # context
    c = {
        'contact_history_form': information_organisation_contact_history_form(),
        'contact_history_results': contact_history_results,
        'organisation_permissions': organisation_permissions,
        'contact_history': contact_history,
        'contact_year': contact_date.year,
        'contact_month': contact_date.month,
        'contact_day': contact_date.day,
        'contact_hour': contact_date.hour,
        'contact_minute': int(contact_date.minute / 5) * 5,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_organisation_documents_list(request, organisation_id):
    organisation_permissions = 0
    document_perm = 0

    if request.session['is_superuser'] == True:
        organisation_permissions = 4
        document_perm = 4
    else:
        pp_results = return_user_permission_level(request, None,'organisation')
        ph_results = return_user_permission_level(request, None, 'documents')

        if pp_results > organisation_permissions:
            organisation_permissions = pp_results

        if ph_results == 1:
            document_perm = 1

    if organisation_permissions == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    #Get data
    customer_document_results = document_permissions.objects.filter(
        organisations_id=organisation_id,
        customer_id__isnull=False,
        is_deleted="FALSE",
    )
    organisation_document_results = document_permissions.objects.filter(
        organisations_id=organisation_id,
        customer_id__isnull=True,
        is_deleted="FALSE",
    )

    #Load template
    t = loader.get_template('NearBeach/organisation_information/organisation_documents_list.html')

    # context
    c = {
        'organisation_id': organisation_id,
        'customer_document_results': customer_document_results,
        'organisation_document_results': organisation_document_results,
        'organisation_permissions': organisation_permissions,
        'document_permissions': document_permissions,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_organisation_documents_upload(request, organisation_id):
    if request.method == "POST":
        if request.FILES == None:
            return HttpResponseBadRequest('File needs to be uploaded')

        #Get the file data
        file = request.FILES['file']

        #Data objects required
        filename = str(file)
        file_size = file._size
        print("File name: " + filename + "\nFile Size: " + str(file_size))

        """
        File Uploads
        """
        organisation_instance = organisations.objects.get(organisations_id=organisation_id)
        document_save = documents(
            document_description=filename,
            document=file,
            change_user=request.user,
        )
        document_save.save()

        document_permissions_save = document_permissions(
            document_key=document_save,
            organisations_id=organisation_instance,
            change_user=request.user,
        )
        document_permissions_save.save()

        result = []
        result.append({
            "name" : filename,
            "size" : file_size,
            "url" : '',
            "thumbnail_url" : '',
            "delete_url" : '/',
            "delete_type" : "POST",
        })
        response_data = simplejson.dumps(result)
        return HttpResponse(response_data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Only POST accepted')
