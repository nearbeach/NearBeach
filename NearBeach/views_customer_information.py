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

import simplejson
from .user_permissions import return_user_permission_level
from django.urls import reverse


@login_required(login_url='login',redirect_field_name="")
def information_customer_contact_history(request, customer_id):
    permission_results = return_user_permission_level(request, None,['customer','contact_history'])

    if permission_results['customer']  == 0:
        return HttpResponseRedirect(reverse('permission_denied'))

    if request.method == "POST":
        # Save everything!
        form = information_customer_contact_history_form(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            """
            If the user has written something in the contact section, we want to save it
            """
            contact_history_notes = form.cleaned_data['contact_history']

            if not contact_history_notes == '':
                # Lets save some contact history
                contact_type = form.cleaned_data['contact_type']
                contact_date = form.cleaned_data['contact_date']


                # document
                contact_attachment = request.FILES.get('contact_attachment')
                if contact_attachment:
                    documents_save = document(
                        document_description=contact_attachment,
                        document=contact_attachment,
                        change_user=request.user,
                    )
                    documents_save.save()

                    # Add to document permissions
                    document_permissions_save = document_permission(
                        document_key=documents_save,
                        customer_id=customer.objects.get(customer_id=customer_id),
                        change_user=request.user,
                    )
                    document_permissions_save.save()

                customer_instance = customer.objects.get(customer_id=customer_id)

                submit_history = contact_history(
                    #organisation_id=customer_instance.organisation_id,
                    customer_id=customer_instance,
                    contact_type=contact_type,
                    contact_date=contact_date,
                    contact_history=contact_history_notes,
                    user_id=current_user,
                    change_user=request.user,
                )
                #if not customer_instance.organisation_id == None:
                #    submit_history.organisation_id = customer_instance.organisation_id

                if contact_attachment:
                    submit_history.document_key = documents_save
                submit_history.save()



    #Data
    customer_contact_history = contact_history.objects.filter(
        customer_id=customer.objects.get(customer_id=customer_id)
    )

    contact_date = datetime.datetime.now()

    #Load template
    t = loader.get_template('NearBeach/customer_information/customer_contact_history.html')

    # context
    c = {
        'contact_history_form': information_customer_contact_history_form(),
        'customer_contact_history': customer_contact_history,
        'media_url': settings.MEDIA_URL,
        'PRIVATE_MEDIA_URL': settings.PRIVATE_MEDIA_URL,
        'contact_year': contact_date.year,
        'contact_month': contact_date.month,
        'contact_day': contact_date.day,
        'contact_hour': contact_date.hour,
        'contact_minute': int(contact_date.minute/5)*5,
        'contact_history_perm': permission_results['contact_history'],
        'customer_permissions': permission_results['customer'],
    }

    return HttpResponse(t.render(c, request))



@login_required(login_url='login',redirect_field_name="")
def information_customer_documents_upload(request, customer_id):
    if request.method == "POST":
        if request.FILES == None:
            return HttpResponseBadRequest('File needs to be uploaded')

        #Get the file data
        file = request.FILES['file']

        #Data objects required
        filename = str(file)
        file_size = file.size
        print("File name: " + filename + "\nFile Size: " + str(file_size))

        """
        File Uploads
        """
        customer_results = customer.objects.get(customer_id=customer_id)
        document_save = document(
            document_description=filename,
            document=file,
            change_user=request.user,
        )
        document_save.save()

        document_permissions_save = document_permission(
            document_key=document_save,
            organisation_id=customer_results.organisation_id,
            customer_id=customer_results,
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

