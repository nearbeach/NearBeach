from __future__ import unicode_literals
from django import forms


#Import from Models
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
#Import ModelForm
from django.forms import ModelForm
from django.forms.widgets import TextInput
from forms_special_fields import *


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


class add_permission_set_to_group_form(forms.Form):
    permission_set_name = forms.ModelChoiceField(
        label = "Permission Set Name",
        widget=forms.Select,
        queryset=permission_set.objects.filter(is_deleted='FALSE')
    )



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
        model=customers_campus
        fields={
                    'customer_phone',
                    'customer_fax'
                }


class campus_information_form(ModelForm):
    #SQL
    #region_results=list_of_countries_regions.objects.all()

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
            'placeholder': 'Campus Phone (03) 9999 9999',
        })
    )
    campus_fax=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Fax (03) 9999 9999',
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
        model=organisations_campus
        fields='__all__'
        exclude=[
            'campus_region_id',
            'campus_country_id',
            'organisations_id',
            'is_deleted',
            'change_user',
        ]




class customer_information_form(ModelForm):


    #The Fields
    customer_first_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput()
    )

    update_profile_picture=forms.ImageField(required=False,)

    class Meta:
        model=customers
        fields='__all__'
        exclude=[
            'is_deleted',
            'organisations_id',
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



class document_tree_create_folder_form(forms.Form):
    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id')
        project_or_task = kwargs.pop('project_or_task',None)

        super(document_tree_create_folder_form, self).__init__(*args, **kwargs)

        if project_or_task == "P":
            project_instance = project.objects.get(project_id=location_id)
            folders_results = folders.objects.filter(
                is_deleted="FALSE",
                project_id=project_instance,
            )
        elif project_or_task == "T":
            task_instance = tasks.objects.get(tasks_id=location_id)
            folders_results = folders.objects.filter(
                is_deleted="FALSE",
                task_id=task_instance,
            )

        self.fields['nested_folder'].queryset = folders_results

    folder_description = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Folder Description',
            }
        )
    )
    nested_folder = forms.ModelChoiceField(
        required=False,
        queryset=folders.objects.all(),
    )


class document_tree_upload_form(forms.Form):
    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id')
        project_or_task = kwargs.pop('project_or_task',None)

        super(document_tree_upload_form, self).__init__(*args, **kwargs)

        if project_or_task == "P":
            project_instance = project.objects.get(project_id=location_id)
            folders_results = folders.objects.filter(
                is_deleted="FALSE",
                project_id=project_instance,
            )
        elif project_or_task == "T":
            task_instance = tasks.objects.get(tasks_id=location_id)
            folders_results = folders.objects.filter(
                is_deleted="FALSE",
                task_id=task_instance,
            )

        self.fields['nested_folder'].queryset = folders_results

    nested_folder = forms.ModelChoiceField(
        required=False,
        queryset=folders.objects.all(),
    )
    document = forms.FileField(
        required=True,
    )
    document_description = forms.CharField(
        required=True,
        max_length=50,
    )


class groups_form(ModelForm):
    group_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Group Name',
        })
    )
    class Meta:
        model=groups
        fields = {
            'group_name',
        }


class information_customer_contact_history_form(forms.Form):
    # Get data for choice boxes
    contact_type_results = list_of_contact_types.objects.filter(is_deleted='FALSE')

    contact_type = forms.ModelChoiceField(
        label='Contact Type',
        widget=forms.Select,
        queryset=contact_type_results,
        empty_label=None
    )


    start_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    start_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    start_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)


    contact_history=forms.CharField(
        widget=forms.Textarea(attrs={
            'width': '99%',
            'max-height': '300px'
        }),
        required=False
    )

    contact_attachment=forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange':'enable_submit()'
        })
    )





class information_organisation_contact_history_form(forms.Form):
    # Get data for choice boxes
    contact_type_results = list_of_contact_types.objects.filter(is_deleted='FALSE')

    # The Fields
    contact_type = forms.ModelChoiceField(
        label='Contact Type',
        widget=forms.Select,
        queryset=contact_type_results,
        empty_label=None
    )

    start_date_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange": 'check_start_date()'
        })
    )
    start_date_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange": 'check_start_date()'
        })
    )
    start_date_day = forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange": 'check_start_date()'
        })
    )

    start_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    start_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    start_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)

    contact_history = forms.CharField(
        widget=forms.Textarea(attrs={
            'width': '99%'
        })
        , required=False
    )
    contact_attachment = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange': 'enable_submit()'
        })
    )


class information_project_costs_form(forms.Form):
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



class information_project_history_form(forms.Form):
    project_history=forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Please update any history here and then click on the submit button'
        })
        , required=False
    )






class information_task_costs_form(forms.Form):
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



class information_task_history_form(forms.Form):
    task_history=forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Please update any history here and then click on the submit button'
        })
        , required=False
    )


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


class kanban_board_form(ModelForm):
    kanban_board_name = forms.CharField(
        max_length=255,
        widget=TextInput(attrs={
            'placeholder': 'Board Name',
        }),
    )
    class Meta:
        model = kanban_board
        fields = {
            'kanban_board_name',
        }


class list_of_taxes_form(ModelForm):
    class Meta:
        model = list_of_taxes
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
            -- If the user does not have groups associated with them
            
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
                    if (user_groups.objects.filter(username_id=user.id, is_deleted='FALSE').count() == 0): #If the system has not been setup ignore this rule.
                        raise forms.ValidationError("Please contact your system administrator. Your account has no group access")
                else:
                    print("Currently the user has been setup with: " + str(user_groups.objects.filter(username_id=user.id, is_deleted='FALSE').count()) + " user groups")

            except ObjectDoesNotExist:
                print("First time setup " + str(datetime.datetime.now()))

        return super(login_form, self).clean()


class new_campus_form(forms.Form):
    #Get data for choice boxes
    #countries_results=list_of_countries.objects.all()
    #regions_results=list_of_countries_regions.objects.all()

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
            'placeholder': 'Campus Phone (03) 9999 9999',
        })
    )
    campus_fax=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Campus Fax (03) 9999 9999',
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
        queryset=list_of_countries.objects.filter(is_deleted='FALSE'),
        empty_label="Please pick a Country/Region",
        widget=RegionSelect(attrs={
            'class': 'chosen-select',
            'tag': forms.HiddenInput(),
        }),
    )


class new_customer_form(forms.Form):
    #Get data for choice boxes
    titles_results=list_of_titles.objects.all()
    organisations_results=organisations.objects.filter(is_deleted='FALSE')

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
    }),
    )
    organisations_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select,
        queryset=organisations_results,
        required=False,
    )


class new_line_item_form(ModelForm):
    #Get the data
    products_and_services = forms.ModelChoiceField(
        required=False,
        queryset=products_and_services.objects.filter(is_deleted='FALSE'),
        empty_label="Please pick a product/service",
        widget=ProductOrServiceSelect(),
    )
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
    product_description = forms.CharField(
        required=False,
		max_length=255,
		widget=forms.TextInput(attrs={
			'readonly': True,
            'placeholder': 'Product/Service Description',
            'style': 'background-color: aliceblue',
            'style': 'display: none;',
		})
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
        queryset=list_of_taxes.objects.filter(is_deleted='FALSE'),
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
        model = quotes_products_and_services
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
    organisaion_results=organisations.objects.filter(is_deleted='FALSE')
    groups_results=groups.objects.filter(is_deleted="FALSE")
    user_results=auth.models.User.objects.all()

    # Fields
    opportunity_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Opportunity Name',
        })
    )
    opportunity_description=forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Opportunity Description',
        })
    )
    organisations_id=forms.ModelChoiceField(
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
    finish_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    finish_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    finish_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)

    next_step_description=forms.CharField(
        max_length=255,
        required=False
    )

    select_groups=forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'width': '500px',
        }),
    )

    select_users=forms.ModelMultipleChoiceField(
        queryset=user_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'width': '500px',
        }),
    )

    class Meta:
        model=opportunity
        fields='__all__'


        exclude={
            'opportunity_expected_close_date',
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
        widget=forms.TextInput(attrs={
            'width': '99%',
            'placeholder': 'https://organisations_website.com',
        })
    )
    organisation_email=forms.EmailField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'width': '99%',
            'placeholder': 'organisations@email.com',
        })
    )


class new_project_form(forms.Form):
    #Get data for choice boxes
    organisations_results=organisations.objects.filter(is_deleted='FALSE')

    # Fields
    project_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Project Name',
        })
    )
    project_description=forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Project Description',
        })
    )
    organisations_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select,
        queryset=organisations_results,
        required=False,
    )
    start_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    start_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    start_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)

    finish_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    finish_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    finish_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)


class new_quote_form(ModelForm):
    #Get data for form
    list_of_quote_stages=list_of_quote_stages.objects.filter(
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
        widget=forms.Textarea(attrs={
            "placeholder": 'Quote Terms',
        }),
    )
    customer_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": 'Customer Notes',
        }),
        required=False,
    )


    class Meta:
        model=quotes
        fields={
            'quote_title',
            'quote_stage_id',
            'quote_terms',
            'customer_notes',
        }


class new_requirement_form(ModelForm):
    requirement_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Requirement Title'
        }),
    )
    requirement_scope = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Requirement Scope'
        }),
    )
    class Meta:
        model=requirements
        fields={
            'requirement_title',
            'requirement_scope',
            'requirement_type',
        }



class new_task_form(forms.Form):
    #Get data for choice boxes
    organisations_results=organisations.objects.filter(is_deleted='FALSE')

    # Fields
    task_short_description=forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Task Short Description',
        }),
    )
    task_long_description=forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": 'Task Long Description',
        }),
    )
    organisations_id=forms.ModelChoiceField(
        label="Organisation",
        widget=forms.Select,
        queryset=organisations_results
    )
    start_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    start_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    start_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)

    finish_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    finish_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    finish_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)


class opportunity_information_form(ModelForm):
    #Get data for form
    groups_results=groups.objects.filter(is_deleted="FALSE")
    user_results=auth.models.User.objects.all()


    next_step=forms.CharField(
        max_length=255,
        required=False,
    )

    finish_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )

    finish_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    finish_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    finish_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)

    select_groups=forms.ModelMultipleChoiceField(
        queryset=groups_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'width': '500px',
        }),
    )

    select_users=forms.ModelMultipleChoiceField(
        queryset=user_results,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'placeholder': "Choose the users(s)",
            'class': 'chosen-select',
            'multiple tabindex': '4',
            'width': '500px',
        }),
    )


    class Meta:
        model=opportunity
        fields='__all__'
        exclude={
            'customer_id',
            'organisations_id',
            'opportunity_expected_close_date',
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
        model=organisations
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
            'placeholder': 'Product Name'
        }),
    )
    product_part_number = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Product Part Number'
        }),
    )
    product_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Product Description'
        }),
    )
    class Meta:
        model=products_and_services
        fields='__all__'
        exclude = {
            'is_deleted',
            'change_user',
        }


class project_information_form(ModelForm):
    """
    Project information will need to abide by the stricked laws of the new
    project datetime edits!!
    """

    start_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    start_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    start_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)

    finish_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    finish_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    finish_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)


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




    class Meta:
        model=project
        fields={
            'project_name',
            'project_description',
        }


class quote_information_form(ModelForm):
    #Get data for form
    list_of_quote_stages=list_of_quote_stages.objects.filter(
        is_deleted='FALSE',
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
        widget=forms.Textarea(attrs={
            "placeholder": 'Quote Terms',
        }),
    )
    customer_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": 'Customer Notes',
        }),
        required=False,
    )

    class Meta:
        model=quotes
        fields={
            'quote_title',
            'quote_stage_id',
            'quote_terms',
            'customer_notes',
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
    class Meta:
        model=requirements
        exclude=[
            'change_user',
            'is_deleted',
        ]



class requirement_items_form(forms.ModelForm):
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




class search_customers_form(forms.Form):
    #Just have a simple search field
    search_customers=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Customers',
        }),
    )

class search_organisations_form(forms.Form):
    #Just have a simple search field
    search_organisations=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Organisations',
        }),
    )


class search_projects_form(forms.Form):
    search_projects=forms.CharField(
        max_length=255,
        required=False
    )
    include_closed=forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=INCLUDE_CLOSED
    )

class search_tasks_form(forms.Form):
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

class search_users_form(forms.Form):
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

    start_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_start_date()'
        })
    )
    start_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    start_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    start_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)

    finish_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange":'check_end_date()'
        })
    )
    finish_date_hour=forms.ChoiceField(choices=HOUR_CHOICES)
    finish_date_minute=forms.ChoiceField(choices=MINUTE_CHOICES)
    finish_date_meridiems=forms.ChoiceField(choices=MERIDIEMS_CHOICES)
    task_history_text=forms.CharField(
        widget=forms.Textarea,
        required=False
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

    class Meta:
        model=tasks
        fields={
            'task_short_description',
            'task_long_description',
        }



class user_information_form(ModelForm):
    password1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'password',
            'placeholder': 'Password',
            'onkeyup': 'enable_submit()',
        })
    )
    password2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'password',
            'placeholder': 'Repeate Password',
            'onkeyup': 'enable_submit()',
        })
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
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
            'username',
            'first_name',
            'last_name',
            'is_active',
            'is_superuser',
            'email',
        }