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

#Global Variables
User=get_user_model



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
    region_results=list_of_countries_regions.objects.all()

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
    # Get data for choice boxes
    contact_type_results=list_of_contact_types.objects.filter(is_deleted='FALSE')

    #The Fields
    customer_first_name=forms.CharField(
        max_length=255,
        widget=forms.TextInput()
    )

    contact_type=forms.ModelChoiceField(
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

    update_profile_picture=forms.ImageField(required=False,)

    #Customer Documents
    document_description=forms.CharField(
        max_length=255,
        required=False
    )
    document=forms.FileField(required=False)

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


class information_project_history_form(forms.Form):
    project_history=forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Please update any history here and then click on the submit button'
        })
        , required=False
    )


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
            """
            if ((not user) or (not user.check_password(password))):
                raise forms.ValidationError("The login details are incorrect")
            elif (not user.is_active):
                raise forms.ValidationError("Please contact your system administrator. Your account has been disabled")
            elif (user_groups.objects.filter(username_id=user.id, is_deleted='FALSE').count() == 0):
                raise forms.ValidationError("Please contact your system administrator. Your account has no group access")
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
        queryset=organisations_results
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
    product_cost = forms.CharField(
		widget=forms.TextInput(attrs={
			'readonly': True,
			'width': '50px',
			'value': '0',
		})
	)
    product_price = forms.CharField(
        widget=forms.TextInput(attrs={
            'onkeyup': 'update_total()',
        })
    )
    product_description = forms.CharField(
        required=False,
		max_length=255,
		widget=forms.TextInput(attrs={
			'readonly': True,
            'placeholder': 'Service Description',
		})
	)
    discount_amount = forms.CharField(
        widget=forms.TextInput(attrs={
            'style': 'display: none;',
            'step': '1',
            'onkeyup': 'update_total()',
        })
    )
    discount_choice = forms.ChoiceField(
        choices=DISCOUNT_CHOICE,
        widget=forms.Select(attrs={
            'onchange': 'change_discount_choice()',
        })
    )
    discount_percentage = forms.CharField(
        required=False, #if empty, we are assuming it will be 0%
        widget=forms.TextInput(attrs={
            'min': '0',
            'max': '100',
            'step': '5',
            'onchange': 'update_total()',
        })
    )
    discount_amount = forms.CharField(
        required=False, #if empty, we are assuming it will be 0
        widget=forms.TextInput(attrs={
            'step': '1',
            'onkeyup': 'update_total()',
        })
    )
    sales_price = forms.CharField(
        required=False, #if empty, we are assuming it will be 0
        widget=forms.TextInput(attrs={
            'step': '1',
            'readonly': 'true',
        })
    )
    tax_amount = forms.CharField(
		widget=forms.TextInput(attrs={
			'readonly': 'true',
			'width': '50px',
			'value': '0',
			'step': '1',
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
    )


    class Meta:
        model=quotes
        fields={
            'quote_title',
            'quote_stage_id',
            'quote_terms',
            'customer_notes',
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
    # Get data for choice boxes
    contact_type_results=list_of_contact_types.objects.filter(is_deleted='FALSE')

    # The Fields
    contact_type=forms.ModelChoiceField(
        label='Contact Type',
        widget=forms.Select,
        queryset=contact_type_results,
        empty_label=None
    )

    start_date_year=forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            "onChange": 'check_start_date()'
        })
    )
    start_date_month=forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            "onChange": 'check_start_date()'
        })
    )
    start_date_day=forms.ChoiceField(
        choices=DAY_CHOICES,
        widget=forms.Select(attrs={
            "onChange": 'check_start_date()'
        })
    )

    contact_history=forms.CharField(
        widget=forms.Textarea(attrs={
            'width': '99%'
        })
        , required=False
    )
    contact_attachment=forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'onChange': 'enable_submit()'
        })
    )

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

    # Costs feature
    cost_description=forms.CharField(
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
    cost_amount=forms.DecimalField(
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


    #Costs feature
    cost_description=forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width':'70%',
                'placeholder': 'Cost Description',
                'onkeyup': 'enable_disable_add_cost()',
            }
        )
    )
    cost_amount=forms.DecimalField(
        max_digits=19,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(
            attrs={
                'width':'30%',
                'placeholder':'$0.00',
                'onkeyup': 'enable_disable_add_cost()',
            }
        )
    )

    class Meta:
        model=tasks
        fields={
                'task_short_description',
                'task_long_description',
        }


