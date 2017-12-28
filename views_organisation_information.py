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
from django.http import HttpResponse
from django.template import  loader
from NearBeach.forms import *
from .models import *
from .namedtuplefetchall import *

@login_required(login_url='login')
def information_organisation_contact_history(request, organisation_id):
    # Get the data from the form if the information has been submitted
    if request.method == "POST":
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
                task_start_date = time_combined(
                    int(form.cleaned_data['start_date_year']),
                    int(form.cleaned_data['start_date_month']),
                    int(form.cleaned_data['start_date_day']),
                    0,
                    0,
                    'AM'
                )

                # documents
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


                submit_history = contact_history(
                    organisations_id=organisations.objects.get(organisations_id=organisation_id),
                    contact_type=contact_type,
                    contact_date=task_start_date,
                    contact_history=contact_history_notes,
                    user_id=current_user,
                    change_user=request.user,
                    #document_key=documents_save,
                )
                if contact_attachment:
                    submit_history.document_key=documents_save
                submit_history.save()
    #Get data
    contact_history_results = contact_history.objects.filter(organisations_id=organisation_id)

    #Load template
    t = loader.get_template('NearBeach/organisation_information/organisation_contact_history.html')

    # context
    c = {
        'contact_history_form': information_organisation_contact_history_form(),
        'contact_history_results': contact_history_results,
    }

    return HttpResponse(t.render(c, request))


@login_required(login_url='login')
def information_organisation_documents(request, organisation_id):
    #Load template
    t = loader.get_template('NearBeach/organisation_information/organisation_documents.html')

    # context
    c = {
    }

    return HttpResponse(t.render(c, request))


"""
The time converter - we need a function that breaks time up into different segments, and also
combines it back. This is the time converter
"""
def time_combined(year,month,day,hour,minute,meridiem):
    """
    Time is tricky. So I am following the simple rules;
    12:** AM will have the hour changed to 0
    1:** AM will not have the hour changed
    12:** PM will not have the hour changed
    1:** PM will have the hour changed by adding 12

    From these simple points, I have constructed the following
    if statements to take control of the correct hour.
    """
    if meridiem == "AM":
        if hour == 12:
            hour = 0
    else:
        if hour < 12:
            hour = hour + 12



    # Create the final start/end date fields
    return datetime.datetime(
        year,
        month,
        day,
        hour,
        minute
    )
