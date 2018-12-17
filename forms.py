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



YEAR_CHOICES=(
    ('2010','2010'),
    ('2011','2011'),
    ('2012','2012'),
    ('2013','2013'),
    ('2014','2014'),
    ('2015','2015'),
    ('2016','2016'),
    ('2017','2017'),
    ('2018','2018'),
    ('2019','2019'),
    ('2020','2020'),
    ('2021','2021'),
    ('2022','2022'),
    ('2023','2023'),
    ('2024','2024'),
    ('2025','2025'),
    ('2026','2026'),
    ('2027','2027'),
    ('2028','2028'),
    ('2029','2029'),
    ('2030','2030'),
    ('2031','2031'),
    ('2032','2032'),
    ('2033','2033'),
    ('2034','2034'),
    ('2035','2035'),
    ('2036','2036'),
    ('2037','2037'),
    ('2038','2038'),
    ('2039','2039'),
    ('2040','2040'),
)

MONTH_CHOICES=(
    ('1','January'),
    ('2','February'),
    ('3','March'),
    ('4','April'),
    ('5','May'),
    ('6','June'),
    ('7','July'),
    ('8','August'),
    ('9','September'),
    ('10','October'),
    ('11','November'),
    ('12','December'),
)

DAY_CHOICES=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('14','14'),
    ('15','15'),
    ('16','16'),
    ('17','17'),
    ('18','18'),
    ('19','19'),
    ('20','20'),
    ('21','21'),
    ('22','22'),
    ('23','23'),
    ('24','24'),
    ('25','25'),
    ('26','26'),
    ('27','27'),
    ('28','28'),
    ('29','29'),
    ('30','30'),
    ('31','31'),
)

HOUR_CHOICES=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
)

MINUTE_CHOICES=(
    ('00','00'),
    ('05','05'),
    ('10','10'),
    ('15','15'),
    ('20','20'),
    ('25','25'),
    ('30','30'),
    ('35','35'),
    ('40','40'),
    ('45','45'),
    ('50','50'),
    ('55','55'),
)

MERIDIEMS_CHOICES=(
    ('AM','AM'),
    ('PM','PM'),
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
    permission_set_name = forms.ModelChoiceField(
        label = "Permission Set Name",
        widget=forms.Select,
        queryset=permission_set.objects.filter(is_deleted='FALSE')
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
                ).exclude(group_id=None).values('group_id')
            )
        elif destination == "task":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    task_id=location_id,
                ).exclude(group_id=None).values('group_id')
            )
        elif destination == "requirement":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    requirement_id=location_id,
                ).exclude(group_id=None).values('group_id')
            )
        elif destination == "quote":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    quote_id=location_id,
                ).exclude(group_id=None).values('group_id')
            )
        elif destination == "kanban_board":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    kanban_board_id=location_id,
                ).exclude(group_id=None).values('group_id')
            )
        elif destination == "opportunity":
            group_results = group_results.exclude(
                group_id__in=object_assignment.objects.filter(
                    is_deleted="FALSE",
                    opportunity_id=location_id,
                ).exclude(group_id=None).values('group_id')
            )

        self.fields['add_group'].queryset = group_results

    add_group = forms.ModelChoiceField(
        queryset=group.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'width': '80%',
            'onchange': 'add_group_change()',
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
            'width': '80%',
            'onchange': 'add_user_change()',
        })
    )



class bug_client_form(ModelForm):
    # Get data for choice boxes
    bug_client_results = list_of_bug_client.objects.filter(is_deleted='FALSE')

    bug_client_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Bug Client Name',
        })
    )
    list_of_bug_client=forms.ModelChoiceField(
        label='Bug Clients',
        widget=forms.Select,
        queryset=bug_client_results,
        empty_label=None,
    )
    bug_client_url=forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Example: https://bugzilla.nearbeach.org',
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
        widget=forms.Select,
        queryset=bug_client_results,
        empty_label=None,
    )
    search = forms.CharField(max_length=255)



class customer_campus_form(ModelForm):
    customer_phone=forms.CharField(
        max_length=11,
        required=False
    )
    customer_fax=forms.CharField(
        max_length=11,
        required=False
    )

    class Meta:
        model=customer_campus
        fields={
                    'customer_phone',
                    'customer_fax'
                }


class campus_information_form(ModelForm):
    #SQL
    #region_results=list_of_country_region.objects.all()

    # Fields
    campus_nickname=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Nickname i.e Melbourne',
        })
    )
    campus_phone=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Phone',
            'type': 'tel',
        })
    )
    campus_fax=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Fax',
            'type': 'tel',
        })
    )
    campus_address1=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 1',
        })
    )
    campus_address2=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 2',
        })
    )
    campus_address3=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 3',
        })
    )
    campus_suburb=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Suburb',
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


class cost_information_form(forms.Form):
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



class customer_information_form(ModelForm):


    #The Fields
    customer_first_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput()
    )

    update_profile_picture=forms.ImageField(required=False,)

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
            We only want to limit pictures to being under 400kb
            """
            picture_errors=""

            main, sub=profile_picture.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg','gif','png']):
                picture_errors += 'Please use a JPEG, GIF or PNG image'

            if len(profile_picture) > (MAX_PICTURE_SIZE): #400kb
                picture_errors += '\nPicture profile exceeds 400kb'

            if not picture_errors == "":
                raise forms.ValidationError(picture_errors)

        except AttributeError:
            pass

        return profile_picture


class diagnostic_test_document_upload_form(forms.Form):
    document = forms.FileField(
        required=True,
    )

class document_upload_form(ModelForm):
    document_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Document Description',
        })
    )
    document_description = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Document Description',
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
            opportunity_results=opportunity.objects.get(opportunity_id=location_id)
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
        }),
    )
    to_email = forms.ModelMultipleChoiceField(
        queryset=customer.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 90%',
        }),
    )
    cc_email = forms.ModelMultipleChoiceField(
        required=False,
        queryset=customer.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 90%',
        }),
    )
    bcc_email = forms.ModelMultipleChoiceField(
        required=False,
        queryset=customer.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 90%',
        }),
    )
    email_subject = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Subject',
        }),
    )
    email_content = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Email content'
            }
        )
    )
    is_private = forms.BooleanField(
        required=False,
    )
    email_quote = forms.BooleanField(
        required=False,
    )
    quote_template_description=forms.ModelChoiceField(
        queryset=quote_template.objects.filter(is_deleted='FALSE'),
        empty_label=None,
        required=False,
    )


    class Meta:
        model = customer
        fields = {

        }

class email_information_form(ModelForm):
    email_content = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Email content',
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
    group_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Group Name',
        })
    )
    class Meta:
        model=group
        fields = {
            'group_name',
        }


class information_customer_contact_history_form(forms.Form):
    # Get data for choice boxes
    contact_type_results = list_of_contact_type.objects.filter(is_deleted='FALSE')

    contact_type = forms.ModelChoiceField(
        label='Contact Type',
        widget=forms.Select,
        queryset=contact_type_results,
        empty_label=None
    )
    contact_attachment=forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange':'enable_submit()'
        })
    )

    contact_history=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Opportunity Description',
            }
        ),
        required=False,
    )
    contact_date=forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
        })
    )





class information_organisation_contact_history_form(forms.Form):
    # Get data for choice boxes
    contact_type_results = list_of_contact_type.objects.filter(is_deleted='FALSE')

    # The Fields
    contact_type = forms.ModelChoiceField(
        label='Contact Type',
        widget=forms.Select,
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
            }
        ),
        required=False,
    )
    contact_attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange': 'enable_submit()'
        })
    )
    contact_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
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
        }),
    )

    kanban_card_text = forms.CharField(
        required=True,
        max_length=255,
        widget=TextInput(attrs={
            'placeholder': 'Card Text',
        }),
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
        }),
    )
    kanban_board_column = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Please place each new column on a new line. Each name will be truncated to 255 characters',
        }),
        required=True,
    )
    kanban_board_level = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Please place each new level on a new line. Each name will be truncated to 255 characters',
        }),
        required=True,
    )
    select_groups = forms.ModelMultipleChoiceField(
        queryset=group_results,
        required=True,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
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
    class Meta:
        model = list_of_tax
        fields = {
            'tax_amount',
            'tax_description',
        }



class login_form(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'login',
            'width': '100%'
        })
    )
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password',
            'width': '100%'
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
        })
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Address'
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
        })
    )
    campus_phone=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Phone',
            'type': 'tel',
        })
    )
    campus_fax=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Fax',
            'type': 'tel',
        })
    )
    campus_address1=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 1',
        })
    )
    campus_address2=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 2',
        })
    )
    campus_address3=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Address 3',
        })
    )
    campus_suburb=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Suburb',
        })
    )
    country_and_region = forms.ModelChoiceField(
        required=False,
        queryset=list_of_country.objects.filter(is_deleted='FALSE'),
        empty_label="Please pick a Country/Region",
        widget=RegionSelect(attrs={
            'class': 'chosen-select',
            'tag': forms.HiddenInput(),
            'style': 'width: 100%',
        }),
    )


class new_customer_form(forms.Form):
    #Get data for choice boxes
    titles_results=list_of_title.objects.all()
    organisations_results=organisation.objects.filter(is_deleted='FALSE')

    #Fields
    customer_title=forms.ModelChoiceField(
        label='Title',
        widget=forms.Select(),
        queryset=titles_results
    )
    customer_first_name=forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
        }),
    )
    customer_last_name=forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
        'placeholder': 'Last Name',
    }),
    )
    customer_email=forms.EmailField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'customer@email.com',
            'type':'email',
        }),
    )
    organisation_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select,
        queryset=organisations_results,
        required=False,
    )


class new_folder_form(forms.Form):
    folder_description=forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Folder Description',
        })
    )


class new_line_item_form(ModelForm):
    #Get the data
    quantity = forms.IntegerField(
		widget=forms.TextInput(attrs={
			'value': '1',
			'width': '10px',
            'onkeyup': 'update_total()',
		})
	)
    product_price = forms.CharField(
        widget=forms.TextInput(attrs={
            'readonly': True,
            'style': 'background-color: aliceblue',
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
        })
    )
    discount_choice = forms.ChoiceField(
        choices=DISCOUNT_CHOICE,
        widget=forms.Select(attrs={
            'onchange': 'discount_type_change()',
        })
    )
    discount_percent = forms.CharField(
        required=False, #if empty, we are assuming it will be 0%
        widget=forms.TextInput(attrs={
            'min': '0',
            'max': '100',
            'step': '5',
            'onchange': 'update_total()',
        })
    )

    sales_price = forms.CharField(
        required=False, #if empty, we are assuming it will be 0
        widget=forms.TextInput(attrs={
            'step': '1',
            'readonly': 'true',
            'style': 'background-color: aliceblue',
        })
    )
    tax_amount = forms.CharField(
		widget=forms.TextInput(attrs={
			'readonly': 'true',
			'width': '50px',
			'value': '0',
			'step': '1',
            'style': 'background-color: aliceblue',
        })
	)
    tax = forms.ModelChoiceField(
        required=False,
        label="Organisations",
        queryset=list_of_tax.objects.filter(is_deleted='FALSE'),
        widget=forms.Select(attrs={
            "onChange": 'update_total()'
        }),
    )
    total = forms.CharField(
        required=False,
		widget=forms.TextInput(attrs={
			'readonly': True,
			'width': '100px',
			'value': '0',
            'style': 'background-color: aliceblue',
		})
	)
    product_note = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder':'Product Notes',
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
    organisaion_results=organisation.objects.filter(is_deleted='FALSE')
    groups_results=group.objects.filter(is_deleted="FALSE")
    user_results=auth.models.User.objects.all()

    # Fields
    opportunity_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Opportunity Name',
        })
    )
    opportunity_description=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Opportunity Description',
            }
        )
    )
    opportunity_expected_close_date=forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
        })
    )
    organisation_id=forms.ModelChoiceField(
        label="Organisations",
        queryset=organisaion_results,
        required=False,
        widget=forms.Select(attrs={
            "onChange":'update_customers()'
        }),
    )
    amount_type_id=forms.ModelChoiceField(
        label="Amount Type",
        widget=forms.Select,
        queryset=amount_type_results,
    )
    select_groups=forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 100%',
        }),
    )

    select_users=forms.ModelMultipleChoiceField(
        queryset=user_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 100%',
        }),
    )

    class Meta:
        model=opportunity
        fields='__all__'


        exclude={
            'opportunity_stage_id',
            'customer_id',
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
                'width': '99%',
        })
    )
    organisation_website=forms.URLField(
        max_length=255,
        widget=forms.URLInput(attrs={
            'style': 'width: 99%;',
            'placeholder': 'https://organisation_website.com',
        })
    )
    organisation_email=forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={
            'width': '99%',
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
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 100%',
        }),
        required=True,
        queryset=group_results,
    )

    project_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Project Name',
        })
    )
    project_description=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Project Description',
            }
        )
    )
    organisation_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select,
        queryset=organisations_results,
        required=False,
    )
    project_start_date=forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
        })
    )
    project_end_date=forms.DateTimeField(
        initial=datetime.datetime.now()+datetime.timedelta(days=31),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px'
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
        })
    )

    quote_valid_till_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    quote_valid_till_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    quote_valid_till_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    quote_valid_till_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    quote_valid_till_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    quote_valid_till_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)


    quote_stage_id = forms.ModelChoiceField(
        label="Quote Stage",
        widget=forms.Select,
        queryset=list_of_quote_stages,
    )

    quote_terms=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'style': 'width: 100%',
            },
            attrs={
                "placeholder": 'Quote Terms',
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
            }
        ),
        required=False,
    )

    select_groups = forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=True,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 100%',
        }),
    )

    class Meta:
        model=quote
        fields={
            'quote_title',
            'quote_stage_id',
            'quote_approval_status_id',
            'quote_terms',
            'customer_notes',
        }


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
            'placeholder': 'Requirement Title'
        }),
    )
    requirement_scope = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Requirement Scope'
            }
        ),
    )
    requirement_status=forms.ModelChoiceField(
        label="Quote Stage",
        widget=forms.Select,
        queryset=requirement_status_results,
    )

    requirement_permission = forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=True,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 100%',
        }),
    )


    class Meta:
        model=requirement
        fields={
            'requirement_title',
            'requirement_scope',
            'requirement_type',
            'requirement_status',
        }


class new_task_form(forms.Form):
    # Get data for choice boxes
    organisations_results=organisation.objects.filter(is_deleted='FALSE')
    group_results = group.objects.filter(is_deleted='FALSE')

    # Fields
    task_permission=forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(attrs={
            'placeholder': 'Select Groups to Assign to Project',
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 100%',
        }),
        required=True,
        queryset=group_results,
    )
    task_short_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Task Short Description',
        }),
    )
    task_long_description=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                "placeholder": 'Task Long Description',
            }
        ),
    )
    organisation_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select,
        queryset=organisations_results,
        required=False,
    )
    task_start_date=forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
        })
    )
    task_end_date=forms.DateTimeField(
        initial=datetime.datetime.now()+datetime.timedelta(days=31),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px'
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

    opportunity_description = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Opportunity Description',
            }
        )
    )

    opportunity_expected_close_date = forms.DateTimeField(
        initial=datetime.datetime.now(),
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
        })
    )

    next_step=forms.CharField(
        max_length=255,
        required=False,
    )


    select_groups=forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 100%',
        }),
    )

    select_users=forms.ModelMultipleChoiceField(
        queryset=user_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'style': 'width: 100%',
        }),
    )


    class Meta:
        model=opportunity
        fields='__all__'
        exclude={
            'customer_id',
            'organisation_id',
            'lead_source_id',
            'date_created',
            'date_modified',
            'user_id',
            'is_deleted',
            'change_user',
        }

class organisation_information_form(ModelForm):
    #Profile picture
    update_profile_picture=forms.ImageField(required=False, )

    #Customer Documents
    document_description=forms.CharField(
        max_length=255,
        required=False
    )
    document=forms.FileField(required=False)

    class Meta:
        model=organisation
        fields={
                'organisation_name',
                'organisation_website',
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
    product_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Product/Service Name'
        }),
    )
    product_part_number = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Product/Service Part Number'
        }),
    )
    product_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Product/Service Description'
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
            'width': '100%',
            'readonly': True,
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
    document=forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange':'enable_submit()'
        })
    )
    document_url_location=forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder':'https://example.com',
            'onChange':'enable_submit()'
        })
    )
    document_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'width':'100%',
            'onkeyup':'enable_submit()'
        })
    )

    folder_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'width':'100%',
            'onkeyup':'enable_submit()'
        })
    )

    project_description = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Please Enter your project description',
            }
        )
    )
    project_start_date=forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
        })
    )
    project_end_date=forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px'
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
                'width': '100%',
                'toolbar': False,
                'menubar': False,
                'readonly': 1,
            },
            attrs={
                'placeholder': 'Requirement Scope'
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
                customers=quote_instance.customer_id,
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
    )


    quote_title=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Quote Title',
        })
    )

    quote_valid_till_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    quote_valid_till_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    quote_valid_till_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    quote_valid_till_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    quote_valid_till_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    quote_valid_till_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)


    quote_stage_id = forms.ModelChoiceField(
        label="Quote Stage",
        widget=forms.Select,
        queryset=list_of_quote_stages,
    )


    quote_terms=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'style': 'width: 100%;'
            },
            attrs={
                "placeholder": 'Quote Terms',
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
        }


class quote_template_form(ModelForm):
    quote_template_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Quote Template Description',
        })
    )
    header=forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Please Enter Template Header',
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
        }),
    )


class requirement_information_form(ModelForm):
    requirement_scope = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                'width': '100%',
            },
            attrs={
                'placeholder': 'Requirement Scope'
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
    """
    This is used for both
    -- New requirement items
    -- Editing existing requirement items
    """
    requirement_item_title=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Requirement Item Title',
        })
    )
    requirement_item_scope=forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Requirement Item Scope',
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
        }),
    )

class search_organisation_form(forms.Form):
    #Just have a simple search field
    search_organisation=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Organisations',
        }),
    )


class search_project_form(forms.Form):
    search_projects=forms.CharField(
        max_length=255,
        required=False
    )
    include_closed=forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=INCLUDE_CLOSED
    )

class search_task_form(forms.Form):
    search_tasks=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Tasks',
        }),
    )
    include_closed=forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=INCLUDE_CLOSED
    )

class search_template_form(forms.Form):
    search_templates=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Templates',
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




class task_information_form(ModelForm):
    task_short_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            "class":'task_short_description'
        })
    )

    document=forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange':'enable_submit()'
        })
    )
    document_url_location=forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder':'https://example.com',
            'onChange':'enable_submit()'
        })
    )
    document_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'width':'100%',
            'onkeyup':'enable_submit()'
        })
    )

    folder_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width': '100%',
                'onkeyup': 'enable_submit()'
            }
        )
    )

    task_start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px',
        })
    )
    task_end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'style': 'width: 200px'
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



class timeline_form(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'onchange': 'render_gantt_chart()',
            'style': 'width: 120px;',
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'onchange': 'render_gantt_chart()',
            'style': 'width: 120px;',
        })
    )
    object_type = forms.ChoiceField(
        choices=OBJECT_CHOICES,
        widget=forms.Select(attrs={
            'onchange': 'render_gantt_chart()',
        })
    )


class to_do_form(ModelForm):
    to_do = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'To do next?',
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
        })
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
        }),
    )
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Address'
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
        })
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
            'style': 'width: 100%;'
        }),
    )

    class Meta:
        model=user_weblink
        fields = {
            'user_weblink_url',
            'user_weblink_source',
        }