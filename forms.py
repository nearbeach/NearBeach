from django import forms

#Import from Models
from .models import organisations
from .models import list_of_titles
from .models import list_of_countries

#Import Django's users
from django.contrib.auth.models import User

#Import extra
import datetime

#Global Variables
#Setup drop down box options
YEAR_CHOICES = (
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

MONTH_CHOICES = (
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

DAY_CHOICES = (
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

HOUR_CHOICES = (
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

MINUTE_CHOICES = (
	('0','0'),
	('5','5'),
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

MERIDIEMS_CHOICES = (
	('AM','AM'),
	('PM','PM'),
)


class new_campus_form(forms.Form):
	#Get data for choice boxes
	countries_results = list_of_countries.objects.all()
	
	#Fields
	campus_nickname = forms.CharField(max_length = 255)
	campus_phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Please use a correct standard of phone number."))
	campus_fax = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Please use a correct standard of phone number."))
	campus_country_id = forms.ModelChoiceField(label = "Organisation", widget = forms.Select, queryset = countries_results)
	campus_address1 = forms.CharField(max_length = 255)
	campus_address2 = forms.CharField(max_length = 255)
	campus_address3 = forms.CharField(max_length = 255)
	campus_suburb = forms.CharField(max_length = 255) #BUG
	campus_state_id = forms.CharField(max_length = 255)


class new_customer_form(forms.Form):
	#Get data for choice boxes
	titles_results = list_of_titles.objects.all()
	
	customer_title = forms.ModelChoiceField(label = 'Title', widget = forms.Select, queryset = titles_results)
	customer_first_name = forms.CharField(max_length = 50)
	customer_last_name = forms.CharField(max_length = 50)
	customer_email = forms.EmailField(max_length = 200)


class new_organisation_form(forms.Form):
	organisation_name = forms.CharField(max_length = 255)
	organisation_website = forms.URLField(max_length = 255)
	organisation_email = forms.EmailField(max_length = 255)

class new_project_form(forms.Form):
	#Get data for choice boxes
	organisations_results = organisations.objects.all()
	
	
	project_name = forms.CharField(max_length = 255)
	project_description = forms.CharField(widget = forms.Textarea)
	organisations_id = forms.ModelChoiceField(label = "Organisation", widget = forms.Select, queryset = organisations_results)
	
	start_date_year = forms.ChoiceField(choices = YEAR_CHOICES)
	start_date_month = forms.ChoiceField(choices = MONTH_CHOICES)
	start_date_day = forms.ChoiceField(choices = DAY_CHOICES)
	start_date_hour = forms.ChoiceField(choices = HOUR_CHOICES)
	start_date_minute = forms.ChoiceField(choices = MINUTE_CHOICES)
	start_date_meridiems = forms.ChoiceField(choices = MERIDIEMS_CHOICES)
	
	finish_date_year = forms.ChoiceField(choices = YEAR_CHOICES)
	finish_date_month = forms.ChoiceField(choices = MONTH_CHOICES)
	finish_date_day = forms.ChoiceField(choices = DAY_CHOICES)
	finish_date_hour = forms.ChoiceField(choices = HOUR_CHOICES)
	finish_date_minute = forms.ChoiceField(choices = MINUTE_CHOICES)
	finish_date_meridiems = forms.ChoiceField(choices = MERIDIEMS_CHOICES)
	


class new_task_form(forms.Form):



	#Get data for choice boxes
	organisations_results = organisations.objects.all()
	
	task_short_description = forms.CharField(max_length = 255)
	task_long_description = forms.CharField(widget = forms.Textarea)
	organisations_id = forms.ModelChoiceField(label = "Organisation", widget = forms.Select, queryset = organisations_results)

	start_date_year = forms.ChoiceField(choices = YEAR_CHOICES)
	start_date_month = forms.ChoiceField(choices = MONTH_CHOICES)
	start_date_day = forms.ChoiceField(choices = DAY_CHOICES)
	start_date_hour = forms.ChoiceField(choices = HOUR_CHOICES)
	start_date_minute = forms.ChoiceField(choices = MINUTE_CHOICES)
	start_date_meridiems = forms.ChoiceField(choices = MERIDIEMS_CHOICES)
	
	finish_date_year = forms.ChoiceField(choices = YEAR_CHOICES)
	finish_date_month = forms.ChoiceField(choices = MONTH_CHOICES)
	finish_date_day = forms.ChoiceField(choices = DAY_CHOICES)
	finish_date_hour = forms.ChoiceField(choices = HOUR_CHOICES)
	finish_date_minute = forms.ChoiceField(choices = MINUTE_CHOICES)
	finish_date_meridiems = forms.ChoiceField(choices = MERIDIEMS_CHOICES)


	
class search_customers_form(forms.Form):
	#Just have a simple search field
	search_customers = forms.CharField(max_length = 255, required = False)

class search_organisations_form(forms.Form):
	#Just have a simple search field
	search_organisations = forms.CharField(max_length = 255, required = False)



