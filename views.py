from django.shortcuts import render
from django.http import HttpResponse

#login imports
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators import csrf
from django.template import RequestContext, loader
from django.shortcuts import render
from django.urls import reverse

# Importing all the classes from the models
from .models import customers
from .models import customers_campus
from .models import group_permissions
from .models import groups
from .models import list_of_countries_states
from .models import list_of_countries
from .models import list_of_titles
from .models import organisations_campus
from .models import organisations
from .models import project_customers
from .models import project_groups
from .models import project_history

from .models import project_stages
from .models import project_tasks
from .models import project
from .models import stages
from .models import tasks_actions
from .models import tasks_customers
from .models import tasks_groups
from .models import tasks_history
from .models import tasks
from .models import user_groups

#Import Settings file to obtain secret key
from django.conf import settings

#Used for login
#from django.contrib.auth import authenticate, get_user_model, login, logout


#For Importing RAW SQL
from django.db import connection
from django.db.models import Q

#For the forms
from django.db import models

#Import Django's users
from django.contrib.auth.models import User

#Import forms
from .forms import customer_information_form
from .forms import login_form
from .forms import new_project_form
from .forms import new_organisation_form
from .forms import new_task_form
from .forms import new_customer_form
from .forms import search_customers_form
from .forms import search_organisations_form
from .forms import new_campus_form
from .forms import task_information_form
from .forms import campus_information_form
from .forms import project_information_form
from .forms import search_tasks_form
from .forms import search_projects_form
from .forms import customer_campus_form
from .forms import search_form


#Import datetime
import datetime


# Create your views here.


def active_projects(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	
	#Get username_id from User
	current_user = User.objects.get(username = request.user.get_username())
	
	
	
	#Setup connection to the database and query it
	cursor = connection.cursor()
	
	cursor.execute("""
	SELECT 
	  project.project_id AS "project_id"
	, '' AS "task_id"
	, project.project_name AS "description"
	, project.project_end_date AS "end_date"

	from 
	  project left join project_tasks
		on project.project_id = project_tasks.project_id
		and project_tasks.is_deleted = 'FALSE'
	, project_groups
	, user_groups

	where 1 = 1
	and project.project_status IN ('New','Open')
	and project.project_status IN ('New','Open')
	and project.project_id = project_groups.project_id_id
	and project_groups.groups_id_id = user_groups.group_id_id
	and user_groups.username_id = %s

	UNION

	select 
	  project_tasks.project_id AS `Project ID`
	, tasks.tasks_id AS `Task ID`
	, tasks.task_short_description AS `Description`
	, tasks.task_end_date AS `End Date` 

	from 
	  tasks left join project_tasks
		on tasks.tasks_id = project_tasks.task_id 
		and project_tasks.is_deleted = "FALSE"
	, tasks_groups
	, user_groups

	where 1 = 1
	and tasks.task_status in ('New','Open')
	and tasks.tasks_id = tasks_groups.tasks_id_id
	and tasks_groups.groups_id_id = user_groups.group_id_id
	and user_groups.username_id = %s
	
	UNION
	
	select 
	 project_tasks.project_id AS `Project ID`
	, tasks.tasks_id AS `Task ID`
	, tasks.task_short_description AS `Description`
	, tasks.task_end_date AS `End Date` 
	
	from 
	  tasks left join project_tasks
		on tasks.tasks_id = project_tasks.task_id 
		and project_tasks.is_deleted = "FALSE"


	where 1 = 1
	and tasks.task_status in ('New','Open')
	and tasks.task_assigned_to_id = %s
	""", [current_user.id, current_user.id, current_user.id])
	active_projects_results = namedtuplefetchall(cursor)
	
	#Load the template
	t = loader.get_template('NearBeach/active_projects.html')
	
	#context
	c = {
		'active_projects_results': active_projects_results,
	}
	
	return HttpResponse(t.render(c, request))
	
	
def associate(request, project_id, task_id, project_or_task):
	#Submit the data
	submit_result = project_tasks(
								project_id_id = project_id, 
								task_id_id = task_id)
	submit_result.save()
	
	
	#Once we assign them together, we go back to the original
	if project_or_task == "P":
		return HttpResponseRedirect(reverse('project_information', args = {project_id} ))
	else:
		return HttpResponseRedirect(reverse('task_information', args = {task_id}))
		


def associated_projects(request, task_id):
	"""
	We want the ability for the user to assign any project to the current
	task that their group owns. The user will have the ability to
	check to see if they want only new or open, or if they would like
	to see closed tasks too.
	"""
	search_projects = search_projects_form()
	
	#POST
	if request.method == "POST":
		#TO DO! EXTRACT POST AND FILTER RESULTS!!!
		projects_results = project.objects.filter()
	else:
		projects_results = project.objects.filter()
	
	#Load the template
	t = loader.get_template('NearBeach/associated_projects.html')
	
	#context
	c = {
		'projects_results': projects_results,
		'search_projects': search_projects,
		'task_id': task_id,
	}
	
	return HttpResponse(t.render(c, request))

def associated_tasks(request, project_id):
	"""
	We want the ability for the user to assign any task to the current
	project that their group owns. The user will have the ability to
	check to see if they want only new or open, or if they would like
	to see closed tasks too.
	"""
	search_tasks = search_tasks_form()
	
	#POST
	if request.method == "POST":
		#TO DO! EXTRACT POST AND FILTER RESULTS!!!
		tasks_results = tasks.objects.filter()
	else:
		tasks_results = tasks.objects.filter()
	
	#Load the template
	t = loader.get_template('NearBeach/associated_tasks.html')
	
	#context
	c = {
		'tasks_results': tasks_results,
		'search_tasks': search_tasks,
		'project_id': project_id,
	}
	
	return HttpResponse(t.render(c, request))


def campus_information(request, campus_information):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	
	#Obtain data (before POST if statement as it is used insude)
	campus_results = organisations_campus.objects.get(pk = campus_information)	
	
	#If instance is in POST
	if request.method == "POST":
		if 'add_customer_submit' in request.POST:
			#Obtain the ID of the customer
			customer_results = int(request.POST.get("add_customer_select"))
			
			#Get the SQL Instances
			customer_instance = customers.objects.get(customer_id = customer_results)
			campus_instances = organisations_campus.objects.get(id = campus_information)
			
			#Save the new campus
			submit_campus = customers_campus(customer_id = customer_instance,	campus_id = campus_instances,	customer_phone = '', customer_fax = '')
			submit_campus.save()
			
			#Go to the form.
			return HttpResponseRedirect(reverse('customers_campus_information', args={submit_campus.id,'CAMP'}))
			
		else:
			#Other save button must have been pressed	
			form = campus_information_form(request.POST)
			if form.is_valid():
				
				#Save all the data
				campus_results.organisations_id = form.cleaned_data['organisations_id']
				campus_results.campus_nickname = form.cleaned_data['campus_nickname']
				campus_results.campus_phone = form.cleaned_data['campus_phone']
				campus_results.campus_fax = form.cleaned_data['campus_fax']
				campus_results.campus_address1 = form.cleaned_data['campus_address1']
				campus_results.campus_address2 = form.cleaned_data['campus_address2']
				campus_results.campus_address3 = form.cleaned_data['campus_address3']
				campus_results.campus_suburb = form.cleaned_data['campus_suburb']
				campus_results.campus_state_id = form.cleaned_data['campus_state_id']
				campus_results.campus_country_id = form.cleaned_data['campus_country_id']
				
				campus_results.save()
		

	#Get Data
	customer_campus_results = customers_campus.objects.filter(campus_id = campus_information)
	add_customers_results = customers.objects.filter(organisations_id = campus_results.organisations_id)
	
	
	#Load the template
	t = loader.get_template('NearBeach/campus_information.html')
	
	#context
	c = {
		'campus_results': campus_results,
		'campus_information_form': campus_information_form(instance=campus_results),
		'customer_campus_results': customer_campus_results,
		'add_customers_results': add_customers_results,	
	}
	
	return HttpResponse(t.render(c, request))	


def customers_campus_information(request, customer_campus_id, customer_or_org):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))

		
	#IF method is post
	if request.method == "POST":
		form = customer_campus_form(request.POST)
		if form.is_valid():
			#Save the data
			save_data = customers_campus.objects.get(id = customer_campus_id)
			
			save_data.customer_phone = form.cleaned_data['customer_phone']
			save_data.customer_fax = form.cleaned_data['customer_fax']
			
			save_data.save()
					
			"""
			Now direct the user back to where they were from. The default
			will be the customer information
			"""
			if customer_or_org == "CAMP":
				return HttpResponseRedirect(reverse('campus_information', args = { save_data.campus_id.id } ))
			else:
				return HttpResponseRedirect(reverse('customer_information', args = { save_data.customer_id.customer_id } ))


	
	#Get Data
	customer_campus_results = customers_campus.objects.get(id = customer_campus_id)
	
	#Setup the initial results
	initial = {
		'customer_phone': customer_campus_results.customer_phone,
		'customer_fax': customer_campus_results.customer_fax,
	}
	
	
	#Load template
	t = loader.get_template('NearBeach/customer_campus.html')
	
	#context
	c = {
		'customer_campus_form': customer_campus_form(initial=initial),
		'customer_campus_results': customer_campus_results,
		'customer_campus_id': customer_campus_id,
		'customer_or_org': customer_or_org,
	}
	
	return HttpResponse(t.render(c, request))


def customer_information(request, customer_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
		
	if request.method == "POST":
		#If we are adding a new campus
		if 'add_campus_submit' in request.POST:
			#Obtain the id of the campus_id
			campus_id_results = request.POST.get("add_campus_select")
			
			#Get the SQL Instances
			customer_instance = customers.objects.get(customer_id = customer_id)
			campus_instances = organisations_campus.objects.get(id = campus_id_results)
			
			#Save the new campus
			submit_campus = customers_campus(customer_id = customer_instance,	campus_id = campus_instances,	customer_phone = '', customer_fax = '')
			submit_campus.save()
			
			#Go to the form.
			return HttpResponseRedirect(reverse('customers_campus_information', args={submit_campus.id,'CUST'}))
	
	#Get the instance
	customer_results = customers.objects.get(pk = customer_id)
	add_campus_results = organisations_campus.objects.filter(organisations_id = customer_results.organisations_id)


	#The campus the customer is associated to
	campus_results = customers_campus.objects.filter(customer_id = customer_id)
	
	#load template
	t = loader.get_template('NearBeach/customer_information.html')
	
	#context
	c = {
		'customer_information_form': customer_information_form(instance=customer_results),
		'campus_results': campus_results,
		'add_campus_results': add_campus_results,
		'customer_id': customer_id,
	}
	
	return HttpResponse(t.render(c, request))	


def index(request):
	"""
	The index page determines if a particular user has logged in. It will
	follow the following steps
	
	Method
	~~~~~~
	1.) If there is a user logged in, if not, send them to login
	2.) Find out if this user should be in the system, if not send them to
		invalid view
	3.) If survived this far the user will be sent to "Active Projects"
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	else:
		return HttpResponseRedirect(reverse('active_projects'))
	
	#Default
	return HttpResponseRedirect(reverse('login'))




def login(request):
	"""
	For some reason I can not use the varable "login_form" here as it is already being used.
	Instead I will use the work form.
	
	The form is declared at the start and filled with either the POST data OR nothing. If this
	process is called in POST, then the form will be checked and if it passes the checks, the
	user will be logged in.
	
	If the form is not in POST (aka GET) OR fails the checks, then it will create the form with
	the relevant errors.
	"""
	form = login_form(request.POST or None)
	
	
	#POST
	if request.method == 'POST':	
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
			
			#Just double checking. :)
			if request.user.is_authenticated:
					return HttpResponseRedirect(reverse('active_projects'))
		else:
			print(form.errors)
	
	#load template
	t = loader.get_template('NearBeach/login.html')
	

		
	#context
	c = {
		'login_form': form,
	}

	return HttpResponse(t.render(c, request))	



def logout(request):
	#log the user out and go to login page
	auth.logout(request)
	return HttpResponseRedirect(reverse('login'))


def new_campus(request, organisations_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	if request.method == 'POST':
		form = new_campus_form(request.POST)
		if form.is_valid():
			campus_nickname = form.cleaned_data['campus_nickname']
			campus_phone = form.cleaned_data['campus_phone']
			campus_fax = form.cleaned_data['campus_fax']
			campus_address1 = form.cleaned_data['campus_address1']
			campus_address2 = form.cleaned_data['campus_address2']
			campus_address3 = form.cleaned_data['campus_address3']
			campus_suburb = form.cleaned_data['campus_suburb']
			campus_state_id = form.cleaned_data['campus_state_id']
			campus_country_id = form.cleaned_data['campus_country_id']
			
			organisation = organisations.objects.get(organisations_id = organisations_id)

			#BUG - some simple validation should go here?
			
			#Submitting the data
			submit_form = organisations_campus(organisations_id = organisation, campus_nickname = campus_nickname, campus_phone = campus_phone, campus_fax = campus_fax, campus_address1 = campus_address1, campus_address2 = campus_address2, campus_address3 = campus_address3, campus_suburb = campus_suburb, campus_state_id = campus_state_id, campus_country_id = campus_country_id)
			submit_form.save()
			
			return HttpResponseRedirect(reverse(organisation_information, args={organisations_id}))
		else:
			print form.errors
			return HttpResponseRedirect(reverse(new_campus, args={organisations_id}))
	else:
		#load template
		t = loader.get_template('NearBeach/new_campus.html')

		#context
		c = {
			'organisations_id': organisations_id,
			'new_campus_form': new_campus_form(),
		}
	
	return HttpResponse(t.render(c, request))	


def new_customer(request, organisations_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	if request.method == 'POST':
		form = new_customer_form(request.POST)
		if form.is_valid():
			customer_title = form.cleaned_data['customer_title']
			customer_first_name = form.cleaned_data['customer_first_name']
			customer_last_name = form.cleaned_data['customer_last_name']
			customer_email = form.cleaned_data['customer_email']
			
			organisations_id = form.cleaned_data['organisations_id']
			
			submit_form = customers(customer_title = customer_title, customer_first_name = customer_first_name, customer_last_name = customer_last_name, customer_email = customer_email, organisations_id = organisations_id)
			
			#BUG - no validation process to see if there exists a customer already :(
			submit_form.save()
			
			return HttpResponseRedirect(reverse(customer_information, args={submit_form.customer_id}))
	else:
		form = new_customer_form()
	
	
	
	#load template
	t = loader.get_template('NearBeach/new_customer.html')

	initial = {
		'organisations_id': organisations_id,
	}

	
	#context
	c = {
		'new_customer_form': new_customer_form(initial=initial),
		'organisations_id': organisations_id,
	}
	
	return HttpResponse(t.render(c, request))


def new_organisation(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
		
		
	"""
	To stop duplicates in the system, the code will quickly check to see if
	there is already a company that has either one of the following;
	-- same name
	-- same website
	-- same contact email.
	
	If one of these conditions are met then the user will be returned to the
	form and shown the possible duplicates. If the user accepts this, then
	the organisation is created.	
	"""
	form = new_organisation_form(request.POST or None)
	duplicate_results = None
	if request.method == 'POST':
		if form.is_valid():
			organisation_name = form.cleaned_data['organisation_name']
			organisation_email = form.cleaned_data['organisation_email']
			organisation_website = form.cleaned_data['organisation_website']
			
			duplicate_results = organisations.objects.filter(Q(organisation_name=organisation_name) | Q(organisation_email=organisation_email) | Q(organisation_website=organisation_website))
			
			
			"""
			If the user has clicked that they accept the duplicate OR if there
			are NO duplicates, just make the organisation :)
			"""
			if ((duplicate_results.count() == 0) or (request.POST.get("save_duplicate"))):
				#Save the form data
				submit_form = organisations(organisation_name = organisation_name, organisation_email = organisation_email, organisation_website = organisation_website)
				submit_form.save()
				return HttpResponseRedirect(reverse(organisation_information, args={submit_form.organisations_id}))

	"""
	Now that we have determined if the organisations should be saved or not
	we are left with the only options;
	1.) There was no organisation to save
	2.) there was a duplicate organisation and we are asking the user about it
	"""
	#load template
	t = loader.get_template('NearBeach/new_organisation.html')
	
	#Define the duplication count
	duplication_count = 0;
	if not duplicate_results == None:
		duplication_count = duplicate_results.count()
		
	
	#context
	c = {
		'new_organisation_form': form,
		'duplicate_results': duplicate_results,
		'duplication_count': duplication_count,
	}
	
	return HttpResponse(t.render(c, request))

	

def new_project(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	if request.method == "POST":
		form = new_project_form(request.POST)
		if form.is_valid():
			project_name = form.cleaned_data['project_name']
			project_description = form.cleaned_data['project_description']
			organisations_id = form.cleaned_data['organisations_id']
			
			#Calendar values
			start_date_year = int(form.cleaned_data['start_date_year'])
			start_date_month = int(form.cleaned_data['start_date_month'])
			start_date_day = int(form.cleaned_data['start_date_day'])
			start_date_hour = int(form.cleaned_data['start_date_hour'])
			start_date_minute = int(form.cleaned_data['start_date_minute'])
			start_date_meridiems = form.cleaned_data['start_date_meridiems']
			
			finish_date_year = int(form.cleaned_data['finish_date_year'])
			finish_date_month = int(form.cleaned_data['finish_date_month'])
			finish_date_day = int(form.cleaned_data['finish_date_day'])
			finish_date_hour = int(form.cleaned_data['finish_date_hour'])
			finish_date_minute = int(form.cleaned_data['finish_date_minute'])
			finish_date_meridiems = form.cleaned_data['finish_date_meridiems']
			
			"""
			Time is tricky. So I am following the simple rules;
			12:** AM will have the hour changed to 0
			1:** AM will not have the hour changed
			12:** PM will not have the hour changed
			1:** PM will have the hour changed by adding 12
			
			From these simple points, I have constructed the following 
			if statements to take control of the correct hour.
			"""
			if start_date_meridiems == "AM":
				if start_date_hour == 12:
					start_date_hour = 0
			else:
				if start_date_hour > 12:
					start_date_hour = start_date_hour + 12
			
			if finish_date_meridiems == "AM":
				if finish_date_hour == 12:
					finish_date_hour = 0
			else:
				if finish_date_hour > 12:
					finish_date_hour = finish_date_hour + 12
			
			
			#Create the final start/end date fields
			project_start_date = datetime.datetime(start_date_year, start_date_month, start_date_day, start_date_hour, start_date_minute)
			project_end_date = datetime.datetime(finish_date_year, finish_date_month, finish_date_day, finish_date_hour, finish_date_minute)
			
			submit_project = project(
									project_name = project_name, 
									project_description = project_description, 
									organisations_id = organisations_id, 
									project_start_date = project_start_date, 
									project_end_date = project_end_date, 
									project_status = 'New')
			
			#Submit the data
			submit_project.save()
	
			"""
			Once the new project has been created, we will obtain a 
			primary key. Using this new primary key we will allocate
			groups to the new project.
			"""
			assigned_to_groups = request.POST.get('assigned_to_groups')
			
			for row in assigned_to_groups:
				submit_group = project_groups(project_id_id = submit_project.pk, groups_id_id = row)
				submit_group.save()
			
			return HttpResponseRedirect(reverse(project_information, args={submit_project.pk}))
	
	else:
		#Obtain the groups the user is associated with
		current_user = request.user
		cursor = connection.cursor()

		cursor.execute(
		"""
		SELECT DISTINCT
		  groups.group_id
		, groups.group_name

		FROM 
		  user_groups join groups
			on user_groups.group_id_id = groups.group_id

		WHERE 1=1
		AND user_groups.is_deleted = "FALSE"
		AND user_groups.username_id = %s
		"""
		, [current_user.id])
		groups_results = namedtuplefetchall(cursor)
		
		organisations_results = organisations.objects.filter(is_deleted='FALSE')
		
		#Setup dates for initalising
		today = datetime.datetime.now()
		next_week = today + datetime.timedelta(days=31)
		
		"""
		We need to do some basic formulations with the hour and and minutes.
		For the hour we need to find all those who are in the PM and
		change both the hour and meridiem accordingly.
		For the minute, we have to create it in 5 minute blocks.
		"""
		hour = today.hour
		minute = int(5*round(today.minute/5.0))
		meridiems = 'AM'
		
		if hour > 12:
			hour = hour - 12
			meridiems = 'PM'
		elif hour == 0:
			hour = 12
		
			
		
		#Load the template
		t = loader.get_template('NearBeach/new_project.html')
		
		#context
		c = {
			'new_project_form': new_project_form(initial={'start_date_year':today.year, 'start_date_month':today.month,'start_date_day':today.day,'start_date_hour':hour,'start_date_minute':minute,'start_date_meridiems':meridiems,
														'finish_date_year':next_week.year, 'finish_date_month':next_week.month,'finish_date_day':next_week.day,'finish_date_hour':hour,'finish_date_minute':minute,'finish_date_meridiems':meridiems,}),
			'groups_results': groups_results,
			'organisations_count': organisations_results.count(),
		}
		
	return HttpResponse(t.render(c, request))


def new_task(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	#Define if the page is loading in POST
	if request.method == "POST":
		form = new_task_form(request.POST)
		if form.is_valid():
			task_short_description = form.cleaned_data['task_short_description']
			task_long_description = form.cleaned_data['task_long_description']
			organisations_id = form.cleaned_data['organisations_id']
			
			#Calendar values
			start_date_year = int(form.cleaned_data['start_date_year'])
			start_date_month = int(form.cleaned_data['start_date_month'])
			start_date_day = int(form.cleaned_data['start_date_day'])
			start_date_hour = int(form.cleaned_data['start_date_hour'])
			start_date_minute = int(form.cleaned_data['start_date_minute'])
			start_date_meridiems = form.cleaned_data['start_date_meridiems']
			
			finish_date_year = int(form.cleaned_data['finish_date_year'])
			finish_date_month = int(form.cleaned_data['finish_date_month'])
			finish_date_day = int(form.cleaned_data['finish_date_day'])
			finish_date_hour = int(form.cleaned_data['finish_date_hour'])
			finish_date_minute = int(form.cleaned_data['finish_date_minute'])
			finish_date_meridiems = form.cleaned_data['finish_date_meridiems']
			
			"""
			Time is tricky. So I am following the simple rules;
			12:** AM will have the hour changed to 0
			1:** AM will not have the hour changed
			12:** PM will not have the hour changed
			1:** PM will have the hour changed by adding 12
			
			From these simple points, I have constructed the following 
			if statements to take control of the correct hour.
			"""
			if start_date_meridiems == "AM":
				if start_date_hour == 12:
					start_date_hour = 0
			else:
				if start_date_hour > 12:
					start_date_hour = start_date_hour + 12
			
			if finish_date_meridiems == "AM":
				if finish_date_hour == 12:
					finish_date_hour = 0
			else:
				if finish_date_hour > 12:
					finish_date_hour = finish_date_hour + 12
			
			
			#Create the final start/end date fields
			task_start_date = datetime.datetime(start_date_year, start_date_month, start_date_day, start_date_hour, start_date_minute)
			task_end_date = datetime.datetime(finish_date_year, finish_date_month, finish_date_day, finish_date_hour, finish_date_minute)
			
			
			submit_task = tasks(task_short_description = task_short_description, task_long_description = task_long_description, organisations_id = organisations_id, task_start_date = task_start_date, task_end_date = task_end_date, task_status = 'New')
			
			#Submit the data
			submit_task.save()
	
			"""
			Once the new project has been created, we will obtain a 
			primary key. Using this new primary key we will allocate
			groups to the new project.
			"""
			assigned_to_groups = request.POST.get('assigned_to_groups')
			
			for row in assigned_to_groups:
				submit_group = tasks_groups(tasks_id_id = submit_task.pk, groups_id_id = row)
				submit_group.save()
			
			return HttpResponseRedirect(reverse(task_information, args={submit_task.pk}))
		return HttpResponseRedirect(reverse('new_task'))
	
	else:
		#Obtain the groups the user is associated with
		current_user = User.objects.get(id = request.user.id)
		cursor = connection.cursor()

		cursor.execute(
		"""
		SELECT DISTINCT
		  groups.group_id
		, groups.group_name

		FROM 
		  user_groups join groups
			on user_groups.group_id_id = groups.group_id

		WHERE 1=1
		AND user_groups.is_deleted = "FALSE"
		AND user_groups.username_id = %s
		"""
		, [current_user.id])
		groups_results = namedtuplefetchall(cursor)

		#Setup dates for initalising
		today = datetime.datetime.now()
		next_week = today + datetime.timedelta(days=31)
		
		
		
		"""
		We need to do some basic formulations with the hour and and minutes.
		For the hour we need to find all those who are in the PM and
		change both the hour and meridiem accordingly.
		For the minute, we have to create it in 5 minute blocks.
		"""
		hour = today.hour
		minute = int(5*round(today.minute/5.0))
		meridiems = 'AM'
		
		if hour > 12:
			hour = hour - 12
			meridiems = 'PM'
		elif hour == 0:
			hour = 12


		#Loaed the template
		t = loader.get_template('NearBeach/new_task.html')
		
		c = {
			'new_task_form': new_task_form(initial={'start_date_year':today.year, 'start_date_month':today.month,'start_date_day':today.day,'start_date_hour':hour,'start_date_minute':minute,'start_date_meridiems':meridiems,
														'finish_date_year':next_week.year, 'finish_date_month':next_week.month,'finish_date_day':next_week.day,'finish_date_hour':hour,'finish_date_minute':minute,'finish_date_meridiems':meridiems,}),
			'groups_results': groups_results,
		}
	
	return HttpResponse(t.render(c, request))


def organisation_information(request, organisations_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	
	#Query the database for organisation information
	organisation_results = organisations.objects.get(pk = organisations_id)
	campus_results = organisations_campus.objects.filter(organisations_id = organisations_id)
	customers_results = customers.objects.filter(organisations_id = organisation_results)
	
	
	#Loaed the template
	t = loader.get_template('NearBeach/organisation_information.html')
	
	c = {
		'organisation_results': organisation_results,
		'campus_results': campus_results,
		'customers_results': customers_results,
	}
	
	return HttpResponse(t.render(c, request))
	

def project_information(request, project_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	"""
	There are two buttons on the project information page. Both will come
	here. Both will save the data, however only one of them will resolve
	this project.
	"""
	#Get the data from the form if the information has been submitted
	if request.method == "POST":
		form = project_information_form(request.POST)
		if form.is_valid():
			#Define the data we will edit
			project_results = project.objects.get(project_id = project_id)
			
			project_results.project_name = form.cleaned_data['project_name']
			project_results.project_description = form.cleaned_data['project_description']

			
			#Calendar values
			start_date_year = int(form.cleaned_data['start_date_year'])
			start_date_month = int(form.cleaned_data['start_date_month'])
			start_date_day = int(form.cleaned_data['start_date_day'])
			start_date_hour = int(form.cleaned_data['start_date_hour'])
			start_date_minute = int(form.cleaned_data['start_date_minute'])
			start_date_meridiems = form.cleaned_data['start_date_meridiems']
			
			finish_date_year = int(form.cleaned_data['finish_date_year'])
			finish_date_month = int(form.cleaned_data['finish_date_month'])
			finish_date_day = int(form.cleaned_data['finish_date_day'])
			finish_date_hour = int(form.cleaned_data['finish_date_hour'])
			finish_date_minute = int(form.cleaned_data['finish_date_minute'])
			finish_date_meridiems = form.cleaned_data['finish_date_meridiems']
			
			"""
			Time is tricky. So I am following the simple rules;
			12:** AM will have the hour changed to 0
			1:** AM will not have the hour changed
			12:** PM will not have the hour changed
			1:** PM will have the hour changed by adding 12
			
			From these simple points, I have constructed the following 
			if statements to take control of the correct hour.
			"""
			if start_date_meridiems == "AM":
				if start_date_hour == 12:
					start_date_hour = 0
			else:
				start_date_hour = start_date_hour + 12
			
			if finish_date_meridiems == "AM":
				if finish_date_hour == 12:
					finish_date_hour = 0
			else:
				finish_date_hour = finish_date_hour + 12
			
			
			#Create the final start/end date fields
			project_results.project_start_date = datetime.datetime(start_date_year, start_date_month, start_date_day, start_date_hour, start_date_minute)
			project_results.project_end_date = datetime.datetime(finish_date_year, finish_date_month, finish_date_day, finish_date_hour, finish_date_minute)
			
			#Check to make sure the resolve button was hit
			if 'Resolve' in request.POST:
				#Well, we have to now resolve the data
				project_results.project_status = 'Resolved'
			
			project_results.save()
			
			#Now save the new project history.
			project_history_text_results = form.cleaned_data['project_history_text']
			
			if not project_history_text_results == '':
				current_user = User.objects.get(username = request.user.get_username())
				
				### TEMP SOLUTION ###
				project_id_connection = project.objects.get(pk = project_id)
				### END TEMP SOLUTION ###
				
				data = project_history(
									project_id = project_id_connection, 
									user_id = current_user, 
									project_history = project_history_text_results, 
									user_infomation = current_user.id
									)
				data.save()
			

	else:
		#If the method is not POST then we have to define project_results
		project_results = project.objects.get(project_id = project_id)


	#Obtain the required data
	project_history_results = project_history.objects.filter(project_id = project_id, is_deleted = 'FALSE')
	
	"""
	The 24 hours to 12 hours formula.
	00:00 means that it is 12:00 AM - change required for hour
	01:00 means that it is 01:00 AM - no change required
	12:00 means that it is 12:00 PM - change required for meridiem
	13:00 means that it is 01:00 PM - change required for hour and meridiem
	"""
	start_hour = project_results.project_start_date.hour
	start_meridiem = u'AM'
	if start_hour == 0:
		start_hour = 12
	elif start_hour == 12:
		start_meridiem = u'PM'
	elif start_hour > 12:
		start_hour = start_hour - 12
		start_meridiem = u'PM'
	
	end_hour = project_results.project_end_date.hour
	end_meridiem = u'AM'
	if end_hour == 0:
		end_hour = 12
	elif end_hour == 12:
		end_meridiem = u'PM'
	elif end_hour > 12:
		end_hour = end_hour - 12
		end_meridiem = u'PM'

	
	#Setup the initial data for the form
	initial = {
		'project_name': project_results.project_name,
		'project_description': project_results.project_description,
		'start_date_year': project_results.project_start_date.year,
		'start_date_month': project_results.project_start_date.month,
		'start_date_day': project_results.project_start_date.day,
		'start_date_hour': start_hour,
		'start_date_minute': project_results.project_start_date.minute,
		'start_date_meridiems': start_meridiem,
		'finish_date_year': project_results.project_end_date.year,
		'finish_date_month': project_results.project_end_date.month,
		'finish_date_day': project_results.project_end_date.day,
		'finish_date_hour': end_hour,
		'finish_date_minute': project_results.project_end_date.minute,
		'finish_date_meridiems': end_meridiem,
	}

	#Query the database for associated task information
	cursor = connection.cursor()
	cursor.execute("""
		SELECT DISTINCT
		  tasks.tasks_id
		, tasks.task_short_description
		, tasks.task_end_date
		FROM tasks
			JOIN project_tasks
			ON tasks.tasks_id = project_tasks.task_id
			AND project_tasks.is_deleted = 'FALSE'
			AND project_id = %s
		""", [project_id])
	associated_tasks_results = namedtuplefetchall(cursor)

	
	#Load the template
	t = loader.get_template('NearBeach/project_information.html')
	
	#context
	c = {
		'project_information_form': project_information_form(initial=initial),
		'project_results': project_results,
		'associated_tasks_results': associated_tasks_results,
		'project_history_results': project_history_results,
	}
	
	return HttpResponse(t.render(c, request))


def resolve_project(request, project_id):
	project_update = project.objects.get(project_id = project_id)
	project_update.project_status = 'Resolved'
	project_update.save()
	return HttpResponseRedirect(reverse('active_projects'))


def resolve_task(request, task_id):
	task_update = task.object.get(task_id = task_id)
	task_update.task_status = 'Resolved'
	task_update.save()
	return HttpResponseRedirect(reverse('active_projects'))	


def search(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	#Load the template
	t = loader.get_template('NearBeach/search.html')
	
	"""
	We will use the POST varable to help filter the results from the 
	database. The results will then appear below
	"""
	search_results = ''
	
	#Define if the page is loading in POST
	if request.method == "POST":
		form = search_form(request.POST)
		if form.is_valid():
			search_results = form.cleaned_data['search_for']

			
	"""
	This is where the magic happens. I will remove all spaces and replace
	them with a wild card. This will be used to search the concatenated
	first and last name fields
	"""	
	search_like = '%'
	
	for split_row in search_results.split(' '):
		search_like+=split_row
		search_like+='%'
	
	#Query the database for organisations
	cursor = connection.cursor()
	cursor.execute("""
		SELECT DISTINCT
		*
		FROM project
		WHERE 1=1
		AND (
			project.project_id like %s
			or project.project_name like %s
			or project.project_description like %s
			)
		""", [search_like, search_like, search_like])
	project_results = namedtuplefetchall(cursor)
	
	#Get list of tasks
	cursor.execute("""
		SELECT DISTINCT
		*
		FROM tasks
		WHERE 1=1
		AND (
			tasks.tasks_id like %s
			or tasks.task_short_description like %s
			or tasks.task_long_description like %s
		)
	""", [search_like, search_like, search_like])
	task_results = namedtuplefetchall(cursor)


	#context
	c = {
		'search_form': search_form(initial={ 'search_for': search_results }),
		'project_results': project_results,
		'task_results': task_results,
	}
	
	return HttpResponse(t.render(c, request))
	


def search_customers(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	
	#Load the template
	t = loader.get_template('NearBeach/search_customers.html')
	
	"""
	We will use the POST varable to help filter the results from the 
	database. The results will then appear below
	"""
	search_customers_results = ''
	
	#Define if the page is loading in POST
	if request.method == "POST":
		form = search_customers_form(request.POST)
		if form.is_valid():
			search_customers_results = form.cleaned_data['search_customers']
	
	"""
	This is where the magic happens. I will remove all spaces and replace
	them with a wild card. This will be used to search the concatenated
	first and last name fields
	"""	
	search_customers_like = '%'
	
	for split_row in search_customers_results.split(' '):
		search_customers_like+=split_row
		search_customers_like+='%'
	
	#Query the database for organisations
	cursor = connection.cursor()
	cursor.execute("""
		SELECT DISTINCT
		  customers.customer_id
		, customers.customer_first_name
		, customers.customer_last_name
		, organisations.organisation_name

		FROM customers JOIN organisations
			ON customers.organisations_id_id = organisations.organisations_id
		WHERE 1=1
		AND UPPER(customers.customer_first_name || ' ' || customers.customer_last_name) LIKE %s
		""", [search_customers_like])
	customers_results = namedtuplefetchall(cursor)
	
	#context
	c = {
		'search_customers_form': search_customers_form(initial={ 'search_customers': search_customers_results }),
		'customers_results': customers_results,		
	}
	
	return HttpResponse(t.render(c, request))

def search_organisations(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	#Load the template
	t = loader.get_template('NearBeach/search_organisations.html')
	
	
	"""
	We will use the following varable to help filterer our database
	results. ***WrTIE BETTER TOO TIRED TO DESCRIBE THIS!!!***
	"""
	search_organisations_results = ''
	
	#Define if the page is loading in POST
	if request.method == "POST":
		form = search_organisations_form(request.POST)
		if form.is_valid():
			search_organisations_results = form.cleaned_data['search_organisations']
	
	"""
	This is where the magic happens. I will remove all spaces and replace
	them with a wild card. This will be used to search the concatenated
	first and last name fields
	"""	
	search_organisations_like = '%'
	
	for split_row in search_organisations_results.split(' '):
		search_organisations_like+=split_row
		search_organisations_like+='%'
	
	#Now search the organisations
	#organisations_results = organisations.objects.filter(organisation_name__contains = search_organisations_like)
	
	#Query the database for organisations
	cursor = connection.cursor()
	cursor.execute("""
		SELECT DISTINCT
		  organisations.organisations_id
		, organisations.organisation_name
		, organisations.organisation_website
		, organisations.organisation_email
		FROM organisations
		WHERE 1=1
		AND organisations.organisation_name LIKE %s
		""", [search_organisations_like])
	organisations_results = namedtuplefetchall(cursor)
	
	
	#context
	c = {
		'search_organisations_form': search_organisations_form(initial={'search_organisations': search_organisations_results}),
		'organisations_results': organisations_results,
	}
	
	return HttpResponse(t.render(c, request))
	
def search_projects_tasks(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	#Load the template
	t = loader.get_template('NearBeach/search_projects_and_tasks.html')
	
	#context
	c = {

	}
	
	return HttpResponse(t.render(c, request))
	

def task_information(request, task_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	"""
	There are two buttons on the task information page. Both will come
	here. Both will save the data, however only one of them will resolve
	the task.
	"""
	#Define the data we will edit
	task_results = tasks.objects.get(tasks_id = task_id)
	
	#Get the data from the form
	if request.method == "POST":
		form = task_information_form(request.POST)
		if form.is_valid():
			#Extract all the information from the form and save
			task_results.task_short_description = form.cleaned_data['task_short_description']
			task_results.task_long_description = form.cleaned_data['task_long_description']

			
			#Calendar values
			start_date_year = int(form.cleaned_data['start_date_year'])
			start_date_month = int(form.cleaned_data['start_date_month'])
			start_date_day = int(form.cleaned_data['start_date_day'])
			start_date_hour = int(form.cleaned_data['start_date_hour'])
			start_date_minute = int(form.cleaned_data['start_date_minute'])
			start_date_meridiems = form.cleaned_data['start_date_meridiems']
			
			finish_date_year = int(form.cleaned_data['finish_date_year'])
			finish_date_month = int(form.cleaned_data['finish_date_month'])
			finish_date_day = int(form.cleaned_data['finish_date_day'])
			finish_date_hour = int(form.cleaned_data['finish_date_hour'])
			finish_date_minute = int(form.cleaned_data['finish_date_minute'])
			finish_date_meridiems = form.cleaned_data['finish_date_meridiems']
			
			"""
			Time is tricky. So I am following the simple rules;
			12:** AM will have the hour changed to 0
			1:** AM will not have the hour changed
			12:** PM will not have the hour changed
			1:** PM will have the hour changed by adding 12
			
			From these simple points, I have constructed the following 
			if statements to take control of the correct hour.
			"""
			if start_date_meridiems == "AM":
				if start_date_hour == 12:
					start_date_hour = 0
			else:
				start_date_hour = start_date_hour + 12
			
			if finish_date_meridiems == "AM":
				if finish_date_hour == 12:
					finish_date_hour = 0
			else:
				finish_date_hour = finish_date_hour + 12
			
			
			#Create the final start/end date fields
			task_results.task_start_date = datetime.datetime(start_date_year, start_date_month, start_date_day, start_date_hour, start_date_minute)
			task_results.task_end_date = datetime.datetime(finish_date_year, finish_date_month, finish_date_day, finish_date_hour, finish_date_minute)
			
			#Check to make sure the resolve button was hit
			if 'Resolve' in request.POST:
				#Well, we have to now resolve the data
				task_results.task_status = 'Resolved'
			
			task_results.save()
			
			#Now save the new project history.
			task_history_text_results = form.cleaned_data['task_history_text']
			
			if not task_history_text_results == '':
				current_user = User.objects.get(username = request.user.get_username())
				
				task_id_connection = tasks.objects.get(tasks_id = task_id)
				
				data = tasks_history(
									tasks_id = task_id_connection, 
									user_id = current_user, 
									task_history = task_history_text_results, 
									user_infomation = current_user.id
									)
				data.save()

	
	#Obtain required data
	task_history_results = tasks_history.objects.filter(tasks_id = task_id) #Will need to remove all IS_DELETED=TRUE
	
	"""
	The 24 hours to 12 hours formula.
	00:00 means that it is 12:00 AM - change required for hour
	01:00 means that it is 01:00 AM - no change required
	12:00 means that it is 12:00 PM - change required for meridiem
	13:00 means that it is 01:00 PM - change required for hour and meridiem
	"""
	start_hour = task_results.task_start_date.hour
	start_meridiem = u'AM'
	if start_hour == 0:
		start_hour = 12
	elif start_hour == 12:
		start_meridiem = u'PM'
	elif start_hour > 12:
		start_hour = start_hour - 12
		start_meridiem = u'PM'
	
	end_hour = task_results.task_end_date.hour
	end_meridiem = u'AM'
	if end_hour == 0:
		end_hour = 12
	elif end_hour == 12:
		end_meridiem = u'PM'
	elif end_hour > 12:
		end_hour = end_hour - 12
		end_meridiem = u'PM'
		
	#Setup the initial
	initial = {
		'task_short_description': task_results.task_short_description,
		'task_long_description': task_results.task_long_description,
		'start_date_year': task_results.task_start_date.year,
		'start_date_month': task_results.task_start_date.month,
		'start_date_day': task_results.task_start_date.day,
		'start_date_hour': start_hour,
		'start_date_minute': task_results.task_start_date.minute,
		'start_date_meridiems': start_meridiem,
		'finish_date_year': task_results.task_end_date.year,
		'finish_date_month': task_results.task_end_date.month,
		'finish_date_day': task_results.task_end_date.day,
		'finish_date_hour': end_hour,
		'finish_date_minute': task_results.task_end_date.minute,
		'finish_date_meridiems': end_meridiem,		
	}
	
	
	#Query the database for associated project information
	cursor = connection.cursor()
	cursor.execute("""
		SELECT 
		  project.project_id
		, project.project_name
		, project.project_end_date
		FROM project
			JOIN project_tasks
			ON project.project_id = project_tasks.project_id
			AND project_tasks.is_deleted = 'FALSE'
			AND project_tasks.task_id = %s
		""", [task_id])
	associated_project_results = namedtuplefetchall(cursor)
	
	
	#Load the template
	t = loader.get_template('NearBeach/task_information.html')

	#context
	c = {
		'task_results': task_results,
		'task_information_form': task_information_form(initial=initial),
		'associated_project_results': associated_project_results,
		'task_history_results': task_history_results,
	}

	return HttpResponse(t.render(c, request))
	


# Extra functionality
"""
The following function helps change the cursor's results into useable
SQL that the html templates can read.
"""
from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


