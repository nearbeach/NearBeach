from __future__ import unicode_literals
from django import forms


#Import from Models
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
#Import ModelForm
from django.forms import ModelForm, BaseModelFormSet
from django.forms.widgets import TextInput
#from forms_special_fields import *
from NearBeach.forms_special_fields import *

from tinymce import TinyMCE

#Used for login
from django.contrib.auth import authenticate, get_user_model, login, logout

#SQL
from django.db import connection


#Import extra
import datetime
from django.core.exceptions import ObjectDoesNotExist
#Global Variables
#User=get_user_model



#Setup drop down box options
DISCOUNT_CHOICE=(
	('Percentage','Percentage'),
	('Amount','Amount'),
)

NOTHING_CHOICE=(
    ('','-----'),
)


OBJECT_CHOICES=(
    ('Project','Project'),
    ('Task','Task'),
    ('Quote','Quote'),
    ('Opportunity','Opportunity'),
)

RATING_SCORE = (
    (1, '1 Star'),
    (2, '2 Star'),
    (3, '3 Star'),
    (4, '4 Star'),
    (5, '5 Star'),
)


RFC_IMPACT = (
    (3,'High'),
    (2,'Medium'),
    (1,'Low'),
)

RFC_PRIORITY = (
    (4,'Critical'),
    (3,'High'),
    (2,'Medium'),
    (1,'Low'),
)

RFC_RISK = (
    (5,'Very High'),
    (4,'High'),
    (3,'Moderate'),
    (2,'Low'),
    (1,'None'),
)

RFC_STATUS = (
    (1,'Draft'),
    (2,'Waiting for approval'),
    (3,'Approved'),
    (4,'Started'),
    (5,'Finished'),
    (6,'Rejected'),
)

RFC_TYPE = (
    (4,'Emergency'),
    (3,'High'),
    (2,'Medium'),
    (1,'Low'),
)


#Include closed option
INCLUDE_CLOSED={
    ('INCLUDE_CLOSED','Include Closed?'),
}

INCLUDE_DEACTIVATED={
    ('INCLUDE_DEACTIVATED','Include Deactivated?'),
}

#Global Variables
MAX_PICTURE_SIZE=1000 * 1024 #1Mb wow


class about_user_form(ModelForm):
    about_user_text = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Give a good description about yourself',
            }
        ),
        required=False,
    )
    class Meta:
        model=about_user
        fields = {
            'about_user_text'
        }


class add_permission_set_to_group_form(forms.Form):
    def __init__(self,*args,**kwargs):
        #Get the group id for this form
        group_id=kwargs.pop('group_id')
        super(add_permission_set_to_group_form,self).__init__(*args,**kwargs)

        #Get the dataset
        permission_set_results = permission_set.objects.filter(
            is_deleted="FALSE",
        ).exclude(
            permission_set_id__in=group_permission.objects.filter(
                is_deleted="FALSE",
                group_id=group_id,
            ).values('permission_set_id')
        )
        #Assign it to the field
        self.fields['add_permission_set'].queryset = permission_set_results

    add_permission_set = forms.ModelChoiceField(
        label = "Permission Set Name",
        widget=forms.Select(attrs={
            'class': 'chosen-select form-control',
            'onchange': 'permission_set_changed()',
        }),
        queryset=permission_set.objects.filter(is_deleted='FALSE')
    )


class add_user_to_group_form(forms.Form):
    def __init__(self,*args,**kwargs):
        group_id=kwargs.pop('group_id')

        super(add_user_to_group_form,self).__init__(*args,**kwargs)

        """
        We want to limit the permission_sets to only those currently applied to the group.
        """
        permission_set_results = permission_set.objects.filter(
            is_deleted="FALSE",
            permission_set_id__in=group_permission.objects.filter(
                is_deleted="FALSE",
                group_id=group_id,
            ).values('permission_set_id')
        )
        self.fields['permission_set'].queryset = permission_set_results

    permission_set=forms.ModelChoiceField(
        queryset=permission_set.objects.all(),
        widget=forms.Select(attrs={
            'class': 'chosen-select form-control',
            'onchange': 'add_user_changed()',
        })
    )
    add_user=forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_active=True,
        ),
        widget=forms.Select(attrs={
            'class': 'chosen-select form-control',
            'onchange': 'add_user_changed()',
        })
    )



class assign_group_add_form(forms.Form):
    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id')
        destination = kwargs.pop('destination', None)

        super(assign_group_add_form, self).__init__(*args, **kwargs)

        """
        The following query will determine the list of groups an object can be assigned to. It will also make sure
        to remove any groups that have already been added to the object.        
        """
        group_results = group.objects.all()

        if destination == "project":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    project_id=location_id,
                ).exclude(
                    group_id=None
                ).values('group_id')
            )
        elif destination == "task":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    task_id=location_id,
                ).exclude(
                    group_id=None
                ).values('group_id')
            )
        elif destination == "requirement":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    requirement_id=location_id,
                ).exclude(
                    group_id=None
                ).values('group_id')
            )
        elif destination == "quote":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    quote_id=location_id,
                ).exclude(
                    group_id=None
                ).values('group_id')
            )
        elif destination == "kanban_board":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    kanban_board_id=location_id,
                ).exclude(
                    group_id=None
                ).values('group_id')
            )
        elif destination == "opportunity":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    opportunity_id=location_id,
                ).exclude(
                    group_id=None
                ).values('group_id')
            )
        elif destination == "request_for_change":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    request_for_change_id=location_id,
                ).exclude(
                    group_id=None
                ).values('group_id')
            )

        self.fields['add_group'].queryset = group_results

    add_group = forms.ModelChoiceField(
        queryset=group.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'onchange': 'add_group_change()',
            'class': 'form-control',
        })
    )



class assign_user_add_form(forms.Form):
    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id')
        destination = kwargs.pop('destination', None)

        super(assign_user_add_form, self).__init__(*args, **kwargs)

        """
        The following query will determine the list of groups an object can be assigned to. It will also make sure
        to remove any groups that have already been added to the object.        
        """

        if destination == "project":
            user_results = User.objects.filter(
                id__in=user_group.objects.filter(
                    is_deleted="FALSE",
                    group_id__in=object_assignment.objects.filter(
                        is_deleted="FALSE",
                        project_id=location_id,
                    ).values('group_id')
                ).values('username')
            ).exclude(
                id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    project_id=location_id,
                ).exclude(
                    assigned_user=None,
                ).values('assigned_user')
            )
        elif destination == "task":
            user_results = User.objects.filter(
                id__in=user_group.objects.filter(
                    is_deleted="FALSE",
                    group_id__in=object_assignment.objects.filter(
                        is_deleted="FALSE",
                        task_id=location_id,
                    ).values('group_id')
                ).values('username')
            ).exclude(
                id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    task_id=location_id,
                ).exclude(
                    assigned_user=None,
                ).values('assigned_user')
            )
        elif destination == "requirement":
            user_results = User.objects.filter(
                id__in=user_group.objects.filter(
                    is_deleted="FALSE",
                    group_id__in=object_assignment.objects.filter(
                        is_deleted="FALSE",
                        requirement_id=location_id,
                    ).values('group_id')
                ).values('username')
            ).exclude(
                id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    requirement_id=location_id,
                ).exclude(
                    assigned_user=None,
                ).values('assigned_user')
            )
        elif destination == "quote":
            user_results = User.objects.filter(
                id__in=user_group.objects.filter(
                    is_deleted="FALSE",
                    group_id__in=object_assignment.objects.filter(
                        is_deleted="FALSE",
                        quote_id=location_id,
                    ).values('group_id')
                ).values('username')
            ).exclude(
                id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    quote_id=location_id,
                ).exclude(
                    assigned_user=None,
                ).values('assigned_user')
            )
        elif destination == "kanban_board":
            user_results = User.objects.filter(
                id__in=user_group.objects.filter(
                    is_deleted="FALSE",
                    group_id__in=object_assignment.objects.filter(
                        is_deleted="FALSE",
                        kanban_board_id=location_id,
                    ).values('group_id')
                ).values('username')
            ).exclude(
                id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    kanban_board_id=location_id,
                ).exclude(
                    assigned_user=None,
                ).values('assigned_user')
            )
        elif destination == "opportunity":
            user_results = User.objects.filter(
                id__in=user_group.objects.filter(
                    is_deleted="FALSE",
                    group_id__in=object_assignment.objects.filter(
                        is_deleted="FALSE",
                        opportunity_id=location_id,
                    ).values('group_id')
                ).values('username')
            ).exclude(
                id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    opportunity_id=location_id,
                ).exclude(
                    assigned_user=None,
                ).values('assigned_user')
            )
        else:
            print("SOMETHING FUCKED UP!!!")
            print("DESTINATION: " + destination)
        self.fields['add_user'].queryset = user_results


    add_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'onchange': 'add_user_change()',
            'class': 'form-control',
        })
    )



class bug_client_form(ModelForm):
    # Get data for choice boxes
    bug_client_results = list_of_bug_client.objects.filter(is_deleted='FALSE')

    bug_client_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Bug Client Name',
            'class': 'form-control',
        })
    )
    list_of_bug_client=forms.ModelChoiceField(
        label='Bug Clients',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=bug_client_results,
        empty_label=None,
    )
    bug_client_url=forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Example: https://bugzilla.nearbeach.org',
            'class': 'form-control',
        })
    )
    class Meta:
        model = bug_client
        fields = {
            'bug_client_name',
            'list_of_bug_client',
            'bug_client_url',
        }


class bug_search_form(forms.Form):
    #Get the choice box
    bug_client_results = bug_client.objects.filter(is_deleted="FALSE")

    #Fields
    list_of_bug_client=forms.ModelChoiceField(
        label='Bug Clients',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=bug_client_results,
        empty_label=None,
    )
    search = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )






class campus_information_form(ModelForm):
    # Fields
    campus_nickname=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Nickname i.e Melbourne',
            'class': 'form-control',
        })
    )
    campus_phone=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Phone',
            'type': 'tel',
            'class': 'form-control',
        })
    )
    campus_fax=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Fax',
            'type': 'tel',
            'class': 'form-control',
        })
    )
    campus_address1=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 1',
            'class': 'form-control',
        })
    )
    campus_address2=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 2',
            'class': 'form-control',
        })
    )
    campus_address3=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 3',
            'class': 'form-control',
        })
    )
    campus_suburb=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Suburb',
            'class': 'form-control',
        })
    )


    class Meta:
        model=campus
        fields='__all__'
        exclude=[
            'campus_region_id',
            'campus_country_id',
            'organisation_id',
            'is_deleted',
            'change_user',
        ]


class campus_readonly_form(ModelForm):
    # Fields
    campus_nickname=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Nickname i.e Melbourne',
            'class': 'form-control',
            'readonly': True,
        })
    )
    campus_phone=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Phone',
            'type': 'tel',
            'class': 'form-control',
            'readonly': True,
        })
    )
    campus_fax=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Fax',
            'type': 'tel',
            'class': 'form-control',
            'readonly': True,
        })
    )
    campus_address1=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 1',
            'class': 'form-control',
            'readonly': True,
        })
    )
    campus_address2=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 2',
            'class': 'form-control',
            'readonly': True,
        })
    )
    campus_address3=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 3',
            'class': 'form-control',
            'readonly': True,
        })
    )
    campus_suburb=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Suburb',
            'class': 'form-control',
            'readonly': True,
        })
    )


    class Meta:
        model=campus
        fields='__all__'
        exclude=[
            'campus_region_id',
            'campus_country_id',
            'organisation_id',
            'is_deleted',
            'change_user',
        ]


class change_task_form(ModelForm):
    def __init__(self,*args,**kwargs):
        #Extract the variables
        rfc_id = kwargs.pop('rfc_id')

        super(change_task_form,self).__init__(*args,**kwargs)

        #Filter for users who are currently in the group.
        user_results = User.objects.filter(
            is_active=True,
            id__in=user_group.objects.filter(
                is_deleted="FALSE",
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    request_for_change=rfc_id,
                ).values('group_id')
            ).values('username')
        )

        self.fields['change_task_assigned_user'].queryset=user_results
        self.fields['change_task_qa_user'].queryset=user_results

    change_task_title = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    change_task_description=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control change_task_description',
            },
        ),
    )

    change_task_start_date=forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
    )
    change_task_end_date=forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
    )
    change_task_assigned_user=forms.ModelChoiceField(
        queryset=None, #Need to limit this
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )
    change_task_qa_user=forms.ModelChoiceField(
        queryset=None, #Need to limit this
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )
    change_task_required_by=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        initial='Stakeholder(s)',
    )
    class Meta:
        model = change_task
        fields = {
            'change_task_title',
            'change_task_description',
            'change_task_start_date',
            'change_task_end_date',
            'change_task_assigned_user',
            'change_task_qa_user',
            'change_task_required_by',
        }

class connect_form(forms.Form):
    customers=forms.ModelMultipleChoiceField(
        queryset = customer.objects.filter(
            is_deleted="FALSE",
        ).order_by(
            'customer_first_name',
            'customer_last_name',
        ),
        widget=ConnectCustomerSelect(),
        required=False,  # If they select nothing it will do nothing :)

    )

    organisations = forms.ModelMultipleChoiceField(
        queryset=organisation.objects.filter(
            is_deleted="FALSE",
        ).order_by(
            'organisation_name',
        ),
        widget=ConnectOrganisationSelect(),
        required=False,  # If they select nothing it will do nothing :)
    )


class contact_history_readonly_form(ModelForm):
    def __init__(self, *args, **kwargs):
        """
        The contact descriptioon will each need to be stored in a readonly tinyMCE widget. The issue here is that
        each widget will need it's own ID other wise it will apply the tinyMCE widget to only one.

        This widget can be used in both the project_readonly and project_information mode
        """
        contact_history_id = kwargs.pop('contact_history_id', None)
        super(contact_history_readonly_form, self).__init__(*args, **kwargs)

        #self.fields['quote_billing_address'].queryset = campus_results

        self.fields['contact_history'].widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'id': 'id_contact_history' + str(contact_history_id),
            },

        )

    #Definition of the tinyMCE widget
    contact_history = forms.CharField()
    submit_history = forms.CharField(
        widget=TextInput(attrs={
            'readonly': True,
            'class': 'form-control',
        })
    )

    class Meta:
        model=contact_history
        fields={
            'contact_history',
        }


class cost_information_form(forms.Form):
    cost_description = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width': '70%',
                'placeholder': 'Cost Description',
                'onkeyup': 'enable_disable_add_cost()',
                'class': 'form-control',
            }
        )
    )
    cost_amount = forms.DecimalField(
        max_digits=19,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width': '30%',
                'placeholder': '$0.00',
                'onkeyup': 'enable_disable_add_cost()',
                'class': 'form-control',
            }
        )
    )


class customer_campus_form(ModelForm):
    customer_phone=forms.CharField(
        max_length=11,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    customer_fax=forms.CharField(
        max_length=11,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )

    class Meta:
        model=customer_campus
        fields={
                    'customer_phone',
                    'customer_fax'
                }


class customer_information_form(ModelForm):
    #The Fields
    customer_last_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    customer_title=forms.ModelChoiceField(
        queryset=list_of_title.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    customer_email=forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        })
    )

    customer_first_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    update_profile_picture=forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'size': MAX_PICTURE_SIZE,
        })
    )

    class Meta:
        model=customer
        fields='__all__'
        exclude=[
            'is_deleted',
            'organisation_id',
            'change_user',
        ]

    def clean_update_profile_picture(self):
        profile_picture=self.cleaned_data['update_profile_picture']

        try:
            """
            We only want to limit pictures to being under 1000kb
            """
            picture_errors=""

            main, sub=profile_picture.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg','gif','png']):
                picture_errors += 'Please use a JPEG, GIF or PNG image'

            if len(profile_picture) > (MAX_PICTURE_SIZE):
                picture_errors += '\nPicture profile exceeds 1000kb'

            if not picture_errors == "":
                raise forms.ValidationError(picture_errors)

        except AttributeError:
            pass

        return profile_picture


class customer_readonly_form(ModelForm):
    #The Fields
    customer_last_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
        })
    )
    customer_title=forms.ModelChoiceField(
        queryset=list_of_title.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'disabled': True,
        })
    )
    customer_email=forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': True,
        })
    )

    customer_first_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
        })
    )
    """
    There is an issue with the customer read only contact histry. It does not pass through the required media files.
    This is a simple and effective work around for that issue.  :) This should be a blank field.
    """
    customer_media=forms.CharField(
        widget=TinyMCE(attrs={

        }),
        required=False,
    )
    class Meta:
        model=customer
        fields='__all__'
        exclude=[
            'is_deleted',
            'organisation_id',
            'change_user',
        ]

class diagnostic_test_document_upload_form(forms.Form):
    document = forms.FileField(
        required=True,
    )

class document_upload_form(ModelForm):
    document_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Document Description',
            'class': 'form-control',
        })
    )
    document_description = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Document Description',
            'class': 'form-control',
        })
    )
    class Meta:
        model = document
        fields = {
            'document',
            'document_description',
        }


class document_url_form(ModelForm):
    document_url_location=forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'https://documentlocation.com',
            'style': 'width: 100%;',
        }),
    )
    document_description=forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Document Description',
        })
    )
    class Meta:
        model = document
        fields = {
            'document_url_location',
            'document_description',
        }


class email_form(ModelForm):
    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id')
        destination = kwargs.pop('destination',None)

        super(email_form, self).__init__(*args, **kwargs)

        if destination == 'organisation':
            customer_results = customer.objects.filter(
                is_deleted="FALSE",
                organisation_id=location_id
            )
            self.fields['to_email'].required=False
        elif destination == "customer":
            customer_results = customer.objects.filter(
                is_deleted="FALSE",
                organisation_id__in=customer.objects.filter(customer_id=location_id).values('organisation_id')
            )

            #If customer has no organisation associated with it
            if not customer_results:
                customer_results = customer.objects.filter(customer_id=location_id)

            self.fields['to_email'].required = True
        elif destination == "project":
            """
            If there is no organisationn assigned to this project then we want to pull out ALL customers that are not
            associated with a organisation.
            """
            project_results = project.objects.get(project_id=location_id)
            if project_results.organisation_id:
                customer_results = customer.objects.filter(
                    is_deleted="FALSE",
                    organisation_id=project.objects.get(project_id=location_id).organisation_id.organisation_id
                )
            else:
                customer_results = customer.objects.filter(
                    customer_id=project_results.customer_id
                )
        elif destination == "task":
            task_results = task.objects.get(task_id=location_id)
            if task_results.organisation_id:
                customer_results = customer.objects.filter(
                    is_deleted="FALSE",
                    organisation_id=task.objects.get(task_id=location_id).organisation_id.organisation_id
                )
            else:
                customer_results = customer.objects.filter(
                    customer_id__in= task_customer.objects.filter(
                        is_deleted="FALSE",
                        task_id=location_id,
                    ).values('customer_id')
                )
        elif destination == "opportunity":
            """
            The following code needs to be fixed up as opportunities can be assigned to customers are organisations.
            
            The rule we want are;
            - Either email all customers of a CONNECTED organisation
            - OR email CONNECTED customers
            """
            opportunity_results=opportunity.objects.get(opportunity_id=location_id)
            customer_results = customer.objects.filter(
                is_deleted="FALSE",
                organisation_id__in=opportunity_connection.objects.filter(
                    is_deleted="FALSE",
                    organisation_id__isnull=False,
                    opportunity_id=location_id,
                ).values('organisation_id')
            )
        elif destination == "quote":
            """
            We need to determine who the quote is for to determine the customer list. For example a quote can be for;
            - Project
            - Task
            - Opportunity
            - Customer
            - Organistaion
            
            Once we know who it is for we then extract the relevant customer list.
            """
            quote_results = quote.objects.get(quote_id=location_id)

            if quote_results.project_id:
                customer_results = customer.objects.filter(
                    is_deleted="FALSE",
                    organisation_id=project.objects.get(project_id=quote_results.project_id.project_id).organisation_id.organisation_id
                )
            elif quote_results.task_id:
                """
                A task can be assigned to an organisation or not. If the task is assigned to an organisaton then it will
                obtain a list of customers from the organisation.
                
                If the task is not assigned to the organisation, then it will obtain a list of customers from the 
                task customers table
                """
                if quote_results.task_id.organisation_id:
                    customer_results = customer.objects.filter(
                        is_deleted="FALSE",
                        organisation_id=task.objects.get(task_id=quote_results.task_id.task_id).organisation_id.organisation_id
                    )
                else:
                    customer_results = customer.objects.filter(
                        is_deleted="FALSE",
                        customer_id__in=task_customer.objects.filter(
                            is_deleted="FALSE",
                            task_id=quote_results.task_id_id
                        )
                    )
            elif quote_results.opportunity_id:
                opportunity_results=opportunity.objects.get(
                        opportunity_id=quote_results.opportunity_id.opportunity_id
                )
                if opportunity_results.organisation_id:
                    customer_results = customer.objects.filter(
                        is_deleted="FALSE",
                        organisation_id=opportunity_results.organisation_id.organisation_id
                    )
                else:
                    customer_results = customer.objects.filter(
                        is_deleted="FALSE",
                        customer_id=opportunity_results.customer_id.customer_id
                    )
            elif quote_results.customer_id:
                customer_results=customer.objects.filter(
                    is_deleted="FALSE",
                    customer_id=quote_results.customer_id.customer_id
                )
            elif quote_results.organisation_id:
                customer_results = customer.objects.filter(
                    is_deleted="FALSE",
                    organisation_id=quote_results.organisation_id
                )
            else:
                print("SOMETHING FUCKED UP!!!")
        else:
            customer_results = ''

        self.fields['to_email'].queryset = customer_results
        self.fields['cc_email'].queryset = customer_results
        self.fields['bcc_email'].queryset = customer_results

    organisation_email = forms.EmailField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display: none;',
            'class': 'form-control',
        }),
    )
    to_email = forms.ModelMultipleChoiceField(
        queryset=customer.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
            'style': 'width: 90%',
        }),
    )
    cc_email = forms.ModelMultipleChoiceField(
        required=False,
        queryset=customer.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
            'style': 'width: 90%',
        }),
    )
    bcc_email = forms.ModelMultipleChoiceField(
        required=False,
        queryset=customer.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
            'style': 'width: 90%',
        }),
    )
    email_subject = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Subject',
            'class': 'form-control col-md-11',
        }),
    )
    email_content = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Email content',
                'class': 'form-control',
            }
        )
    )
    is_private = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
        })
    )
    email_quote = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
        })
    )
    quote_template_description=forms.ModelChoiceField(
        queryset=quote_template.objects.filter(is_deleted='FALSE'),
        empty_label=None,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )


    class Meta:
        model = customer
        fields = {

        }

class email_information_form(ModelForm):
    email_subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-11',
        })
    )
    email_content = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Email content',
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model=email_content
        fields = {
            'email_subject',
            'email_content',
        }

class group_form(ModelForm):
    def __init__(self, *args, **kwargs):
        """
        We need to pass the group_id through, as a group should not be it's own parent group.
        :param args: group_id
        :param kwargs:
        """
        group_id = kwargs.pop('group_id')

        super(group_form, self).__init__(*args, **kwargs)

        group_results = group.objects.filter(
            is_deleted="FALSE",
        ).exclude(group_id=group_id)

        self.fields['parent_group'].queryset = group_results

    group_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Group Name',
            'class': 'form-control',
        })
    )
    parent_group=forms.ModelChoiceField(
        queryset=group.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        required=False,
    )
    class Meta:
        model=group
        fields = {
            'group_name',
            'parent_group',
        }


class information_customer_contact_history_form(forms.Form):
    # Get data for choice boxes
    contact_type_results = list_of_contact_type.objects.filter(is_deleted='FALSE')

    contact_type = forms.ModelChoiceField(
        label='Contact Type',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=contact_type_results,
        empty_label=None
    )
    contact_attachment=forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange':'enable_submit()',
        })
    )

    contact_history=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Opportunity Description',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    contact_date=forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
            'class': 'form-control',
        })
    )





class information_organisation_contact_history_form(forms.Form):
    # Get data for choice boxes
    contact_type_results = list_of_contact_type.objects.filter(is_deleted='FALSE')

    # The Fields
    contact_type = forms.ModelChoiceField(
        label='Contact Type',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=contact_type_results,
        empty_label=None
    )
    contact_history = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Opportunity Description',
                'class': 'form-control',
            }
        ),
        required=False,
    )
    contact_attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange': 'enable_submit()',

        })
    )
    contact_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
            'class': 'form-control',
        })
    )

"""
class information_project_cost_form(forms.Form):
    cost_description = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width': '70%',
                'placeholder': 'Cost Description',
                'onkeyup': 'enable_disable_add_cost()',
            }
        )
    )
    cost_amount = forms.DecimalField(
        max_digits=19,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width': '30%',
                'placeholder': '$0.00',
                'onkeyup': 'enable_disable_add_cost()',
            }
        )
    )
"""


class information_project_history_form(ModelForm):
    project_history = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Project Description',
            }
        )
    )

    class Meta:
        model = project_history
        fields = {
            'project_history'
        }



"""
class information_task_cost_form(forms.Form):
    cost_description = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width': '70%',
                'placeholder': 'Cost Description',
                'onkeyup': 'enable_disable_add_cost()',
            }
        )
    )
    cost_amount = forms.DecimalField(
        max_digits=19,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width': '30%',
                'placeholder': '$0.00',
                'onkeyup': 'enable_disable_add_cost()',
            }
        )
    )
"""


class information_task_history_form(ModelForm):
    task_history=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Project Description',
            }
        )
    )
    class Meta:
        model=task_history
        fields={
            'task_history',
        }


class kanban_card_form(ModelForm):
    def __init__(self, *args, **kwargs):
        kanban_board_id = kwargs.pop('kanban_board_id')

        super(kanban_card_form, self).__init__(*args, **kwargs)

        self.fields['kanban_column'].queryset = kanban_column.objects.filter(kanban_board=kanban_board_id)
        self.fields['kanban_level'].queryset = kanban_level.objects.filter(kanban_board=kanban_board_id)

    kanban_card_comment = forms.CharField(
        required=False,
        widget=TextInput(attrs={
            'placeholder': 'Card Comments',
            'class': 'form-control',
        }),
    )

    kanban_card_text = forms.CharField(
        required=True,
        max_length=255,
        widget=TextInput(attrs={
            'placeholder': 'Card Text',
            'class': 'form-control',
            'onkeydown': 'new_card_text_changed()',
            'onchange': 'new_card_text_changed()',
        }),
    )
    kanban_column=forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=0,
    )
    kanban_level = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=0,
    )

    class Meta:
        model = kanban_card
        fields = {
            'kanban_card_text',
            'kanban_column',
            'kanban_level',
        }


class kanban_board_form(forms.Form):
    #Required python Modules
    group_results = group.objects.filter(is_deleted="FALSE")

    #Fields
    kanban_board_name = forms.CharField(
        max_length=255,
        widget=TextInput(attrs={
            'placeholder': 'Board Name',
            'class': 'form-control',
        }),
    )
    kanban_board_column = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Please place each new column on a new line. Each name will be truncated to 255 characters',
            'class': 'form-control',
        }),
        required=True,
    )
    kanban_board_level = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Please place each new level on a new line. Each name will be truncated to 255 characters',
            'class': 'form-control',
        }),
        required=True,
    )
    select_groups = forms.ModelMultipleChoiceField(
        queryset=group_results,
        required=True,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
            'style': 'width: 100%',
        }),
    )


class kanban_edit_xy_name_form(forms.Form):
    kanban_xy_name=forms.CharField(
        max_length=50,
        widget=TextInput(attrs={
            'placeholder': 'Column/Level Name',
        }),
    )


class kanban_properties_form(ModelForm):
    kanban_board_name=forms.CharField(
        max_length=255,
        widget=TextInput(attrs={
            'placeholder': 'Board Name',
        }),
        required=True,
    )
    class Meta:
        model = kanban_board
        fields = {
            'kanban_board_name',
        }




class kanban_new_link_form(ModelForm):
    def __init__(self, *args, **kwargs):
        kanban_board_id = kwargs.pop('kanban_board_id')

        super(kanban_new_link_form, self).__init__(*args, **kwargs)

        self.fields['kanban_column'].queryset = kanban_column.objects.filter(kanban_board=kanban_board_id)
        self.fields['kanban_level'].queryset = kanban_level.objects.filter(kanban_board=kanban_board_id)

        self.fields['kanban_column'].empty_label = None
        self.fields['kanban_level'].empty_label = None

    kanban_column=forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    kanban_level=forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = kanban_card
        fields = {
            'kanban_column',
            'kanban_level',
        }


class kudos_form(ModelForm):
    kudos_rating=forms.ChoiceField(
        widget=forms.RadioSelect(attrs={
            'style': 'list-style: none;'
        }),
        choices=RATING_SCORE,
    )
    improvement_note=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Improvement Note',
            },
        ),
        required=False,
    )
    liked_note=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Liked Note',
            }
        ),
        required=False,
    )
    project_description = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Project Description',
            },
        ),
        required=False,
    )

    class Meta:
        model = kudos
        fields = {
            'kudos_rating',
            'extra_kudos',
            'improvement_note',
            'liked_note',
        }



class kudos_read_only_form(ModelForm):
    improvement_note=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Improvement Note',
            },
        ),
        required=False,
    )
    liked_note=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Liked Note',
            }
        ),
        required=False,
    )
    project_description = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Project Description',
            },
        ),
        required=False,
    )

    class Meta:
        model = kudos
        fields = {
            'improvement_note',
            'liked_note',
        }


class list_of_tax_form(ModelForm):
    tax_amount=forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    tax_description=forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    class Meta:
        model = list_of_tax
        fields = {
            'tax_amount',
            'tax_description',
        }



class login_form(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
            'required': True,
            'autofocus': True,
        })
    )
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'required': True,
        })
    )


    def clean(self):
        #Get login data
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")

        #Checking authentication
        if username and password:
            user=authenticate(username=username, password=password)
            """
            The following bunch of if, else if statements will return errors if the following
            cases are met
            -- Login is not valid
            -- Login is currently not active
            -- If the user does not have group associated with them
            
            Exception
            ~~~~~~~~~
            If there are NO rows in permission_set then the system will need to be setup and ignore the 
            last rule.
            """
            if ((not user) or (not user.check_password(password))):
                raise forms.ValidationError("The login details are incorrect")
            elif (not user.is_active):
                raise forms.ValidationError("Please contact your system administrator. Your account has been disabled")


            try:
                #If this exists, continue
                if not permission_set.objects.filter(permission_set_id=1).count() == 0: #Sometimes this piece of code will throw an error
                    #Continue
                    if (user_group.objects.filter(username_id=user.id, is_deleted='FALSE').count() == 0): #If the system has not been setup ignore this rule.
                        raise forms.ValidationError("Please contact your system administrator. Your account has no group access")
                else:
                    print("Currently the user has been setup with: " + str(user_group.objects.filter(username_id=user.id, is_deleted='FALSE').count()) + " user group")

            except ObjectDoesNotExist:
                print("First time setup " + str(datetime.datetime.now()))

        return super(login_form, self).clean()


class my_profile_form(ModelForm):
    password1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'password',
            'placeholder': 'Password',
            'onkeyup': 'enable_submit()',
            'autocomplete': 'off',
            'class': 'form-control',
        })
    )
    password2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'password',
            'placeholder': 'Repeate Password',
            'onkeyup': 'enable_submit()',
            'autocomplete': 'off',
            'class': 'form-control',
        })
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'form-control',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Address',
            'class': 'form-control',
        })
    )
    class Meta:
        model=User
        fields={
            'first_name',
            'last_name',
            'email',
        }

class new_campus_form(forms.Form):
    #Get data for choice boxes
    #countries_results=list_of_country.objects.all()
    #regions_results=list_of_country_region.objects.all()

    #Fields
    campus_nickname=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Nickname i.e Melbourne',
            'class': 'form-control',
        })
    )
    campus_phone=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Phone',
            'type': 'tel',
            'class': 'form-control',
        })
    )
    campus_fax=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Fax',
            'type': 'tel',
            'class': 'form-control',
        })
    )
    campus_address1=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 1',
            'class': 'form-control',
        })
    )
    campus_address2=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 2',
            'class': 'form-control',
        })
    )
    campus_address3=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 3',
            'class': 'form-control',
        })
    )
    campus_suburb=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Suburb',
            'class': 'form-control',
        })
    )
    country_and_region = forms.ModelChoiceField(
        required=False,
        queryset=list_of_country.objects.filter(is_deleted='FALSE'),
        empty_label="Please pick a Country/Region",
        widget=RegionSelect(attrs={
            'class': 'chosen-select form-control',
            'tag': forms.HiddenInput(),
            'style': 'width: 100%',
        }),
    )


class new_change_task_form(ModelForm):
    def __init__(self,*args,**kwargs):
        #Extract the variables
        rfc_id = kwargs.pop('rfc_id')

        super(new_change_task_form,self).__init__(*args,**kwargs)

        #Filter for users who are currently in the group.
        user_results = User.objects.filter(
            is_active=True,
            id__in=user_group.objects.filter(
                is_deleted="FALSE",
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    request_for_change=rfc_id,
                ).values('group_id')
            ).values('username')
        )

        self.fields['change_task_assigned_user'].queryset=user_results
        self.fields['change_task_qa_user'].queryset=user_results

    change_task_title = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    change_task_description=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control change_task_description',
            },
        ),
    )

    change_task_start_date=forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
    )
    change_task_end_date=forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
    )
    change_task_assigned_user=forms.ModelChoiceField(
        queryset=None, #Need to limit this
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )
    change_task_qa_user=forms.ModelChoiceField(
        queryset=None, #Need to limit this
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )
    change_task_required_by=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        initial='Stakeholder(s)',
    )
    class Meta:
        model = change_task
        fields = {
            'change_task_title',
            'change_task_description',
            'change_task_start_date',
            'change_task_end_date',
            'change_task_assigned_user',
            'change_task_qa_user',
            'change_task_required_by',
        }



class new_customer_form(forms.Form):
    #Get data for choice boxes
    titles_results=list_of_title.objects.all()
    organisations_results=organisation.objects.filter(is_deleted='FALSE')

    #Fields
    customer_title=forms.ModelChoiceField(
        label='Title',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=titles_results
    )
    customer_first_name=forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'form-control',
        }),
    )
    customer_last_name=forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'form-control',
    }),
    )
    customer_email=forms.EmailField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'customer@email.com',
            'type':'email',
            'class': 'form-control',
        }),
    )
    organisation_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=organisations_results,
        required=False,
    )


class new_folder_form(forms.Form):
    folder_description=forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Folder Description',
            'class': 'form-control',
        })
    )


class new_group_form(ModelForm):
    group_name=forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Group Name',
        }),
    )
    parent_group=forms.ModelChoiceField(
        queryset=group.objects.filter(is_deleted="FALSE"),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        required=False,
    )

    class Meta:
        model = group
        fields = {
            'group_name',
            'parent_group',
        }


class new_line_item_form(ModelForm):
    #Get the data
    product_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    quantity = forms.IntegerField(
		widget=forms.NumberInput(attrs={
			'value': '1',
            'onkeyup': 'update_total()',
            'class': 'form-control',
		})
	)
    product_price = forms.CharField(
        widget=forms.TextInput(attrs={
            'readonly': True,
            'style': 'background-color: aliceblue',
            'class': 'form-control',
        })
    )
    product_and_service = forms.ModelChoiceField(
        required=True,
        queryset=product_and_service.objects.filter(is_deleted='FALSE'),
        empty_label="Please pick a product/service",
        widget=ProductOrServiceSelect(),
    )
    discount_amount = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'background-color: aliceblue',
            'step': '1',
            'onkeyup': 'update_total()',
            'readonly': True,
            'class': 'form-control',
        })
    )
    discount_choice = forms.ChoiceField(
        choices=DISCOUNT_CHOICE,
        widget=forms.Select(attrs={
            'onchange': 'discount_type_change()',
            'class': 'form-control',
        })
    )
    discount_percent = forms.CharField(
        required=False, #if empty, we are assuming it will be 0%
        widget=forms.TextInput(attrs={
            'min': '0',
            'max': '100',
            'step': '5',
            'onchange': 'update_total()',
            'class': 'form-control',
        })
    )

    sales_price = forms.CharField(
        required=False, #if empty, we are assuming it will be 0
        widget=forms.TextInput(attrs={
            'step': '1',
            'readonly': 'true',
            'style': 'background-color: aliceblue',
            'class': 'form-control',
        })
    )
    tax_amount = forms.CharField(
		widget=forms.TextInput(attrs={
			'readonly': 'true',
			'width': '50px',
			'value': '0',
			'step': '1',
            'style': 'background-color: aliceblue',
            'class': 'form-control',
        })
	)
    tax = forms.ModelChoiceField(
        required=False,
        label="Organisations",
        queryset=list_of_tax.objects.filter(is_deleted='FALSE'),
        widget=forms.Select(attrs={
            "onChange": 'update_total()',
            'class': 'form-control',
        }),
    )
    total = forms.CharField(
        required=False,
		widget=forms.TextInput(attrs={
			'readonly': True,
			'width': '100px',
			'value': '0',
            'style': 'background-color: aliceblue',
            'class': 'form-control',
		})
	)
    product_note = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder':'Product Notes',
            'class': 'form-control',
        })
    )


    class Meta:
        model = quote_product_and_service
        fields = '__all__'

        exclude = {
            'quotes_products_and_services_id',
            'quote',
            'customer_id',
            'date_created',
            'date_modified',
            'user_id',
            'is_deleted',
            'change_user',
            'product_cost',
            'discount_percent'
        }



class new_opportunity_form(ModelForm):
    #Get data for choice boxes
    opportunity_stage_results=list_of_opportunity_stage.objects.filter(is_deleted='FALSE')
    amount_type_results=list_of_amount_type.objects.filter(is_deleted='FALSE')
    groups_results=group.objects.filter(is_deleted="FALSE")
    user_results=auth.models.User.objects.all()

    # Fields
    currency_id=forms.ModelChoiceField(
        queryset=list_of_currency.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    lead_source_id=forms.ModelChoiceField(
        queryset=list_of_lead_source.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    opportunity_success_probability=forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    opportunity_amount=forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    amount_type_id=forms.ModelChoiceField(
        queryset=list_of_amount_type.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    opportunity_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Opportunity Name',
            'class': 'form-control',
        })
    )
    opportunity_description=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Opportunity Description',
                'class': 'form-control',
            }
        )
    )
    opportunity_expected_close_date=forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )
    amount_type_id=forms.ModelChoiceField(
        label="Amount Type",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=amount_type_results,
    )
    select_groups=forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
        }),
    )

    select_users=forms.ModelMultipleChoiceField(
        queryset=user_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
        }),
    )

    class Meta:
        model=opportunity
        fields='__all__'


        exclude={
            'opportunity_stage_id',
            'date_created',
            'date_modified',
            'user_id',
            'is_deleted',
            'change_user',
        }

class new_organisation_form(forms.Form):
    organisation_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
                'placeholder': 'Organisation\'s Name',
                'class': 'form-control',
        })
    )
    organisation_website=forms.URLField(
        initial="https://",
        max_length=255,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://organisation_website.com',
            'onblur': 'check_url()',
        })
    )
    organisation_email=forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'organisation@email.com',
            'type': 'email',
        })
    )


class new_project_form(forms.Form):
    #Get data for choice boxes
    organisations_results=organisation.objects.filter(is_deleted='FALSE')
    group_results=group.objects.filter(is_deleted='FALSE')

    # Fields
    project_permission=forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'placeholder': 'Select Groups to Assign to Project',
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',

        }),
        required=True,
        queryset=group_results,
    )

    project_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Project Name',
            'class': 'form-control',
        })
    )
    project_description=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Project Description',
                'class': 'form-control',
            }
        )
    )
    organisation_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=organisations_results,
        required=False,
    )
    project_start_date=forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )
    project_end_date=forms.DateTimeField(
        initial=datetime.datetime.now()+datetime.timedelta(days=31),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = project
        fields = {
            'project_name',
            'project_description',
            'organisation_id',
            'project_start_date',
            'project_end_date',
        }


class new_quote_form(ModelForm):
    #Get data for forms
    groups_results = group.objects.filter(is_deleted="FALSE")
    user_results = auth.models.User.objects.all()

    #Get data for form
    list_of_quote_stages=list_of_quote_stage.objects.filter(
        is_deleted='FALSE',
        is_invoice='FALSE',
    )


    quote_title=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Quote Title',
            'class': 'form-control',
        })
    )

    quote_valid_till = forms.DateTimeField(
        initial=datetime.datetime.now()+datetime.timedelta(days=31),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )

    quote_stage_id = forms.ModelChoiceField(
        label="Quote Stage",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=list_of_quote_stages,
    )

    quote_terms=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'style': 'width: 100%',
            },
            attrs={
                "placeholder": 'Quote Terms',
                'class': 'form-control',
            }
        ),
    )
    customer_notes = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'style': 'width: 100%',
            },
            attrs={
                "placeholder": 'Customer Notes',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    select_groups = forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=True,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
            'style': 'width: 100%',
        }),
    )


    class Meta:
        model=quote
        fields={
            'quote_title',
            'quote_stage_id',
            'quote_terms',
            'customer_notes',
            'quote_valid_till',
        }


class new_request_for_change_form(ModelForm):
    """
    The request for change text has been truncated to rfc_ as the field names were too long.
    """
    rfc_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    rfc_summary = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_type = forms.ChoiceField(
        choices=RFC_TYPE,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=1,
    )
    rfc_implementation_start_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    rfc_implementation_end_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    rfc_implementation_release_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    rfc_version_number = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Version/Release Number',
        }),
        required=False,
    )
    rfc_lead = forms.ModelChoiceField(
        queryset=User.objects.filter( #This should only be group leaders
            is_active=True,
        ),
        widget=forms.Select(attrs={
            'class': 'chosen-select form-control',
        }),
        required=True,
    )
    rfc_priority = forms.ChoiceField(
        choices=RFC_PRIORITY,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=1,
    )
    rfc_risk = forms.ChoiceField(
        choices=RFC_RISK,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=1,
    )
    rfc_impact = forms.ChoiceField(
        choices=RFC_IMPACT,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=1,
    )
    rfc_risk_and_impact_analysis = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_implementation_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_backout_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_test_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )

    rfc_permission=forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'placeholder': 'Select Groups to Assign to Request for Change',
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',

        }),
        required=True,
        queryset=group.objects.filter(is_deleted="FALSE"),
    )
    class Meta:
        model=request_for_change
        exclude=[
            'change_user',
            'is_deleted',
            'rfc_status',
        ]


class new_requirement_item_form(ModelForm):
    # Get data used in query sets
    requirement_item_status_results = list_of_requirement_item_status.objects.filter(
        is_deleted='FALSE',
    )

    requirement_item_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Requirement Item Title',
            'class': 'form-control',
        })
    )
    requirement_item_scope = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'class': 'form-control',
            }
        ),
    )
    requirement_item_status = forms.ModelChoiceField(
        label="Quote Stage",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=requirement_item_status_results,
    )
    requirement_item_type = forms.ModelChoiceField(
        queryset=list_of_requirement_item_type.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    class Meta:
        model = requirement_item
        exclude = [
            'requirement_id'
            'change_user',
            'is_deleted',
        ]


class new_requirement_form(ModelForm):
    #Get Objects for Model Selects
    requirement_status_results = list_of_requirement_status.objects.filter(
        is_deleted='FALSE',
        requirement_status_is_closed='FALSE',
    )
    groups_results=group.objects.filter(is_deleted="FALSE")

    #Fields
    requirement_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Requirement Title',
            'class': 'form-control',
        }),
    )
    requirement_scope = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'class': 'form-control',
            }
        ),
    )
    requirement_status=forms.ModelChoiceField(
        label="Quote Stage",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=requirement_status_results,
    )

    requirement_permission = forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=True,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
            'style': 'width: 100%',
        }),
    )
    requirement_type =forms.ModelChoiceField(
        queryset=list_of_requirement_type.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )


    class Meta:
        model=requirement
        fields={
            'requirement_title',
            'requirement_scope',
            'requirement_type',
            'requirement_status',
        }


class new_tag_form(forms.Form):
    tag_name=forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-10',
            'placeholder': 'Submit Tag',
            'list': 'tag_list',
        }),
    )



class new_task_form(forms.Form):
    # Get data for choice boxes
    organisations_results=organisation.objects.filter(is_deleted='FALSE')
    group_results = group.objects.filter(is_deleted='FALSE')

    # Fields
    task_permission=forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'placeholder': 'Select Groups to Assign to Project',
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
        }),
        required=True,
        queryset=group_results,
    )
    task_short_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Task Short Description',
            'class': 'form-control',
        }),
    )
    task_long_description=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                "placeholder": 'Task Long Description',
                'class': 'form-control',
            }
        ),
    )
    organisation_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=organisations_results,
        required=False,
    )
    task_start_date=forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )
    task_end_date=forms.DateTimeField(
        initial=datetime.datetime.now()+datetime.timedelta(days=31),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )

class opportunity_group_permission_form(forms.Form):
    def __init__(self,*args,**kwargs):
        #Extract the variables
        group_results = kwargs.pop('group_results')

        super(opportunity_group_permission_form,self).__init__(*args,**kwargs)


        self.fields['group'].queryset=group_results

    group = forms.ModelChoiceField(
        required=True,
        queryset=group.objects.filter(is_deleted="BLANK") #This will make the queryset a blank set
    )



class opportunity_information_form(ModelForm):
    #Get data for form
    groups_results=group.objects.filter(is_deleted="FALSE")
    user_results=auth.models.User.objects.all()

    opportunity_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    opportunity_description = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Opportunity Description',
                'class': 'form-control',
            }
        )
    )

    opportunity_expected_close_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )

    next_step=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )


    select_groups=forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
        }),
    )

    select_users=forms.ModelMultipleChoiceField(
        queryset=user_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select form-control',
            'multiple tabindex': '0',
            'style': 'width: 100%',
        }),
    )

    currency_id = forms.ModelChoiceField(
        queryset=list_of_currency.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    opportunity_amount=forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )

    amount_type_id=forms.ModelChoiceField(
        queryset=list_of_amount_type.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

    opportunity_stage_id=forms.ModelChoiceField(
        queryset=list_of_quote_stage.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )

    opportunity_success_probability = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )


    class Meta:
        model=opportunity
        fields='__all__'
        exclude={
            'lead_source_id',
            'date_created',
            'date_modified',
            'user_id',
            'is_deleted',
            'change_user',
        }

class organisation_information_form(ModelForm):
    #Profile picture
    organisation_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    organisation_website=forms.URLField(
        max_length=255,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
        })
    )
    organisation_email=forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        })
    )
    update_profile_picture=forms.ImageField(required=False)

    document=forms.FileField(required=False)

    class Meta:
        model=organisation
        fields={
            'organisation_name',
            'organisation_website',
            'organisation_email',
            }

    def clean_update_profile_picture(self):
        profile_picture=self.cleaned_data['update_profile_picture']

        try:
            """
            We only want to limit pictures to being under 400kb
            """
            picture_errors=""

            main, sub=profile_picture.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'gif', 'png']):
                picture_errors += 'Please use a JPEG, GIF or PNG image'

            if len(profile_picture) > (MAX_PICTURE_SIZE):  # 400kb
                picture_errors += '\nPicture profile exceeds 400kb'

            if not picture_errors == "":
                raise forms.ValidationError(picture_errors)

        except AttributeError:
            pass

        return profile_picture


class organisation_readonly_form(ModelForm):
    #Profile picture
    organisation_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
        })
    )
    organisation_website=forms.URLField(
        max_length=255,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'readonly': True,
        })
    )
    """
    The following field clears up an issue with contact history. Contact history needs the .media field for the tinymce
    to work. A work around is to put an empty field here and just call the .media field.
    """
    bug_fixing_field = forms.CharField(
        widget=TinyMCE(attrs={})
    )

    class Meta:
        model=organisation
        fields={
                'organisation_name',
                'organisation_website',
            }


class opportunity_user_permission_form(forms.Form):
    def __init__(self,*args,**kwargs):
        #Extract the variables
        user_results = kwargs.pop('user_results')

        super(opportunity_user_permission_form,self).__init__(*args,**kwargs)


        self.fields['user'].queryset = user_results

    user = forms.ModelChoiceField(
        required=True,
        #queryset=group.objects.filter(is_deleted="BLANK") #This will make the queryset a blank set
        queryset=User.objects.filter(username=None)
    )




class permission_set_form(ModelForm):
    permission_set_name = forms.CharField(
        max_length=255,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Permission Set Name',
            'class': 'form-control',
        })
    )
    administration_assign_user_to_group=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    administration_create_group=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    administration_create_permission_set=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    administration_create_user=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    assign_campus_to_customer=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    associate_project_and_task=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    bug=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    bug_client=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    customer=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    email=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    invoice=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    invoice_product=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    kanban=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    kanban_card=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    opportunity=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    organisation=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    organisation_campus=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    project=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    quote=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    request_for_change=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    requirement=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    requirement_link=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    tag=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    task=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    tax=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    template=forms.ChoiceField(
        choices=PERMISSION_LEVEL,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    contact_history=forms.ChoiceField(
        choices=PERMISSION_BOOLEAN,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    document=forms.ChoiceField(
        choices=PERMISSION_BOOLEAN,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    kanban_comment=forms.ChoiceField(
        choices=PERMISSION_BOOLEAN,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    project_history=forms.ChoiceField(
        choices=PERMISSION_BOOLEAN,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    task_history=forms.ChoiceField(
        choices=PERMISSION_BOOLEAN,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    #Used for both edit and create
    class Meta:
        model=permission_set
        exclude={
            'date_created',
            'date_modified',
            'change_user',
            'is_deleted',
        }


class product_and_service_form(ModelForm):
    product_or_service=forms.ChoiceField(
        choices=PRODUCT_OR_SERVICE,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    product_cost=forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    product_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    product_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Product/Service Name',
            'class': 'form-control',
        }),
    )
    product_part_number = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Product/Service Part Number',
            'class': 'form-control',
        }),
    )
    product_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Product/Service Description',
            'class': 'form-control',
        }),
    )
    class Meta:
        model=product_and_service
        fields='__all__'
        exclude = {
            'is_deleted',
            'change_user',
        }


class project_history_readonly_form(ModelForm):
    def __init__(self, *args, **kwargs):
        """
        The project descriptioon will each need to be stored in a readonly tinyMCE widget. The issue here is that
        each widget will need it's own ID other wise it will apply the tinyMCE widget to only one.

        This widget can be used in both the project_readonly and project_information mode
        """
        project_history_id = kwargs.pop('project_history_id', None)
        super(project_history_readonly_form, self).__init__(*args, **kwargs)

        #self.fields['quote_billing_address'].queryset = campus_results

        self.fields['project_history'].widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'id': 'id_project_history_' + str(project_history_id),
            },

        )

        #Definition of the tinyMCE widget
    project_history = forms.CharField()
    submit_history = forms.CharField(
        widget=TextInput(attrs={
            'readonly': True,
            'class': 'form-control',
        })
    )

    class Meta:
        model=project_history
        fields={
            'project_history',
        }


class project_information_form(ModelForm):
    """
    Project information will need to abide by the stricked laws of the new
    project datetime edits!!
    """
    project_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    document=forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange':'enable_submit()',
            'class': 'form-control',
        })
    )
    document_url_location=forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder':'https://example.com',
            'onChange':'enable_submit()',
            'class': 'form-control',
        })
    )
    document_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'width':'100%',
            'onkeyup':'enable_submit()',
            'class': 'form-control',
        })
    )

    folder_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'width':'100%',
            'onkeyup':'enable_submit()',
            'class': 'form-control',
        })
    )

    project_description = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Please Enter your project description',
                'class': 'form-control',
            }
        )
    )
    project_start_date=forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )
    project_end_date=forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model=project
        fields={
            'project_name',
            'project_description',
            'project_start_date',
            'project_end_date',
        }

class project_readonly_form(ModelForm):
    project_description = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'class': 'form-control',
            }
        ),
    )

    class Meta:
        model=project
        fields = {
            'project_description'
        }



class quote_information_form(ModelForm):
    def __init__(self,*args,**kwargs):
        """
        Method
        ~~~~~~
        1.) Extract the quote id
        2.) Look at quote inforomation
        3.) If quote has an organisation - take the organisation's campus
        4.) If the quote does not have an organisation - take the customer's campus
        5.) Return the campus results into quote_billing_campus
        """
        quote_instance=kwargs.pop('quote_instance',None)
        super(quote_information_form,self).__init__(*args,**kwargs)

        if quote_instance.organisation_id:
            campus_results = campus.objects.filter(
                is_deleted="FALSE",
                organisation_id=quote_instance.organisation_id,
            )
        elif quote_instance.customer_id:
            campus_results = campus.objects.filter(
                is_deleted="FALSE",
                customer_id=quote_instance.customer_id,
            )
        else:
            #Blank object set
            campus_results = campus.objects.filter(pk=0)

        self.fields['quote_billing_address'].queryset = campus_results
    #Get data for form
    list_of_quote_stages=list_of_quote_stage.objects.filter(
        is_deleted='FALSE',
    )

    quote_billing_address = forms.ModelChoiceField(
        required=False,
        queryset=campus.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )


    quote_title=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Quote Title',
            'class': 'form-control',
        })
    )

    quote_valid_till = forms.DateTimeField(
        initial=datetime.datetime.now() + datetime.timedelta(days=31),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        })
    )

    quote_stage_id = forms.ModelChoiceField(
        label="Quote Stage",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=list_of_quote_stages,
    )


    quote_terms=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'style': 'width: 100%;'
            },
            attrs={
                "placeholder": 'Quote Terms',
                'class': 'form-control',
            },

        ),
    )
    customer_notes = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
              'style': 'width: 100%',
            },
            attrs={
                "placeholder": 'Customer Notes',
                'class': 'form-control',
            }
        ),
        required=False,
    )

    class Meta:
        model=quote
        fields={
            'quote_title',
            'quote_stage_id',
            'quote_terms',
            'customer_notes',
            'quote_valid_till',
        }


class quote_readonly_form(forms.Form):
    quote_terms = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'class': 'form-control',
            }
        ),
    )
    customer_notes = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'class': 'form-control',
            }
        ),
    )


class quote_template_form(ModelForm):
    quote_template_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Quote Template Description',
            'class': 'form-control',
        })
    )
    template_css=forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
        })
    )
    payment_terms=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    notes=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    page_layout=forms.ChoiceField(
        choices=PAGE_LAYOUT,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    margin_left=forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    margin_right=forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    margin_top=forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    margin_bottom=forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    margin_header=forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    margin_footer=forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    header=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Please Enter Template Header',
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model=quote_template
        exclude={
            'date_created',
            'date_modified',
            'change_user',
            'is_deleted',
            'product_line',
            'service_line',
        }



class search_form(forms.Form):
    #Just have a simple search field
    search_for=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search',
            'class': 'form-control',
        }),
    )


class request_for_change_form(ModelForm):
    """
    The request for change text has been truncated to rfc_ as the field names were too long.
    """
    rfc_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    rfc_summary = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_type = forms.ChoiceField(
        choices=RFC_TYPE,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=1,
    )
    rfc_implementation_start_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    rfc_implementation_end_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    rfc_implementation_release_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    rfc_version_number = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Version/Release Number',
        }),
        required=False,
    )
    rfc_lead = forms.ModelChoiceField(
        queryset=User.objects.filter( #This should only be group leaders
            is_active=True,
        ),
        widget=forms.Select(attrs={
            'class': 'chosen-select form-control',
        }),
        required=True,
    )
    rfc_priority = forms.ChoiceField(
        choices=RFC_PRIORITY,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=1,
    )
    rfc_risk = forms.ChoiceField(
        choices=RFC_RISK,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=1,
    )
    rfc_impact = forms.ChoiceField(
        choices=RFC_IMPACT,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        initial=1,
    )
    rfc_risk_and_impact_analysis = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_implementation_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_backout_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_test_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    class Meta:
        model=request_for_change
        exclude=[
            'change_user',
            'is_deleted',
            'rfc_status',
        ]


class request_for_change_note_form(ModelForm):
    rfc_note=forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'height: 80px;'
        }),
        required=False,
    )
    class Meta:
        model=request_for_change_note
        fields=[
            'rfc_note',
        ]


class request_for_change_readonly_form(ModelForm):
    """
    The request for change text has been truncated to rfc_ as the field names were too long.
    """
    rfc_summary = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )

    rfc_risk_and_impact_analysis = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_implementation_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_backout_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    rfc_test_plan = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    class Meta:
        model=request_for_change
        fields=[
            'rfc_summary',
            'rfc_risk_and_impact_analysis',
            'rfc_implementation_plan',
            'rfc_backout_plan',
            'rfc_test_plan',
        ]

class requirement_information_form(ModelForm):
    requirement_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    requirement_type = forms.ModelChoiceField(
        queryset=list_of_requirement_type.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    requirement_status = forms.ModelChoiceField(
        queryset=list_of_requirement_status.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    requirement_scope = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'class': 'form-control',
            }
        ),
    )

    class Meta:
        model=requirement
        exclude=[
            'change_user',
            'is_deleted',
        ]



class requirement_item_form(forms.ModelForm):
    requirement_item_status_results = list_of_requirement_item_status.objects.filter(
        is_deleted='FALSE',
    )

    requirement_item_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Requirement Item Title',
            'class': 'form-control',
        })
    )
    requirement_item_scope = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'class': 'form-control',
            }
        ),
    )
    requirement_item_status = forms.ModelChoiceField(
        label="Quote Stage",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        queryset=requirement_item_status_results,
    )
    requirement_item_type = forms.ModelChoiceField(
        queryset=list_of_requirement_item_type.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    #Fixing a bug
    requirement_id=forms.IntegerField(required=False)
    change_user=forms.IntegerField(required=False)

    class Meta:
        model=requirement_item
        exclude = [
            'requirement_id'
            'change_user',
            'is_deleted',
        ]


class requirement_readonly_form(ModelForm):
    requirement_scope = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'toolbar': False,
                'menubar': False,
            },
            attrs={
                'placeholder': 'Requirement Scope'
            }
        ),
    )

    class Meta:
        model=requirement
        fields=[
            'requirement_scope',
        ]

class search_customer_form(forms.Form):
    #Just have a simple search field
    search_customer=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Customers',
            'class': 'form-control w-75',
        }),
    )

class search_organisation_form(forms.Form):
    #Just have a simple search field
    search_organisation=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Organisations',
            'class': 'form-control w-75',
        }),
    )


class search_template_form(forms.Form):
    search_templates=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Templates',
            'class': 'form-control w-75',
        }),
    )

class search_user_form(forms.Form):
    search_users=forms.CharField(
        max_length=255,
        required=False,
    )
    include_deactivated=forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=INCLUDE_DEACTIVATED
    )



class task_history_readonly_form(ModelForm):
    def __init__(self, *args, **kwargs):
        """
        The project descriptioon will each need to be stored in a readonly tinyMCE widget. The issue here is that
        each widget will need it's own ID other wise it will apply the tinyMCE widget to only one.

        This widget can be used in both the project_readonly and project_information mode
        """
        task_history_id = kwargs.pop('task_history_id', None)
        super(task_history_readonly_form, self).__init__(*args, **kwargs)

        #self.fields['quote_billing_address'].queryset = campus_results

        self.fields['task_history'].widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'id': 'id_task_history_' + str(task_history_id),
            },

        )

    #Definition of the tinyMCE widget
    task_history = forms.CharField()
    submit_history = forms.CharField(
        widget=TextInput(attrs={
            'readonly': True,
            'class': 'form-control',
        })
    )

    class Meta:
        model=task_history
        fields={
            'task_history',
        }


class task_information_form(ModelForm):
    task_short_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            "class":'form-control',
        })
    )

    document=forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange':'enable_submit()',
            "class": 'form-control',
        })
    )
    document_url_location=forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder':'https://example.com',
            'onChange':'enable_submit()',
            "class": 'form-control',
        })
    )
    document_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'width':'100%',
            'onkeyup':'enable_submit()',
            "class": 'form-control',
        })
    )

    folder_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
                'width': '100%',
                'onkeyup': 'enable_submit()',
                "class": 'form-control',
        })
    )

    task_start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            "class": 'form-control',
        })
    )
    task_end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            "class": 'form-control',
        })
    )

    class Meta:
        model=task
        fields={
            'task_short_description',
            'task_long_description',
            #'task_start_date',
            #'task_end_date',
        }


class task_readonly_form(ModelForm):
    task_long_description = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Requirement Scope',
                'class': 'form-control',
            }
        ),
    )

    class Meta:
        model=task
        fields = {
            'task_long_description'
        }


class timeline_form(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'onchange': 'render_gantt_chart()',
            'class': 'form-control',
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'onchange': 'render_gantt_chart()',
            'class': 'form-control',
        })
    )
    object_type = forms.ChoiceField(
        choices=OBJECT_CHOICES,
        widget=forms.Select(attrs={
            'onchange': 'render_gantt_chart()',
            'class': 'form-control',
        })
    )


class to_do_form(ModelForm):
    to_do = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'To do next?',
            'class': 'form-control',
        })
    )
    class Meta:
        model=to_do
        fields={
            'to_do'
        }



class user_information_form(ModelForm):
    password1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'password',
            'placeholder': 'Password',
            'onkeyup': 'enable_submit()',
            'autocomplete': 'off',
            'class': 'form-control',
        })
    )
    password2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'password',
            'placeholder': 'Repeate Password',
            'onkeyup': 'enable_submit()',
            'autocomplete': 'off',
            'class': 'form-control',
        })
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }),
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'form-control',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Address',
            'class': 'form-control',
        })
    )
    class Meta:
        model=User
        fields={
            'username',
            'first_name',
            'last_name',
            'is_active',
            'is_superuser',
            'email',
        }


class user_want_form(ModelForm):
    want_choice_text=forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Please input a want or do not want',
            'class': 'form-control',
        })
    )
    want_choice=forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        choices=WANT_CHOICE,
    )
    want_skill=forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        choices=SKILL_CHOICE,
    )
    class Meta:
        model=user_want
        fields = {
            'want_choice',
            'want_choice_text',
            'want_skill',
        }


class user_weblink_form(ModelForm):
    user_weblink_url=forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'https://nearbeach.org',
            'class': 'form-control',
        }),
    )
    user_weblink_source=forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        choices=WEBSITE_SOURCE,
    )

    class Meta:
        model=user_weblink
        fields = {
            'user_weblink_url',
            'user_weblink_source',
        }