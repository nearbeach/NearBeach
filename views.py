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


#For Importing RAW SQL
from django.db import connection

#For the forms
from django.db import models

#Import Django's users
from django.contrib.auth.models import User

#Import forms
from .forms import new_project_form
from .forms import new_organisation_form
from .forms import new_task_form
from .forms import new_customer_form
from .forms import search_customers_form
from .forms import search_organisations_form

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
	

def auth_view(request):
	#Obtain the values from the login form
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	
	#check the user's details
	user = auth.authenticate(username = username, password = password)
	
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect(reverse('active_projects'))
	else:
		return HttpResponseRedirect(reverse('invalid_login'))


def customer_information(request, customer_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	#load template
	t = loader.get_template('NearBeach/customer_information.html')
	
	#context
	c = {
		
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
		#return HttpResponseRedirect("/NearBeach/login")
		return HttpResponseRedirect(reverse('login'))
	else:
		return HttpResponseRedirect(reverse('active_projects'))
	
	#Default
	return HttpResponseRedirect(reverse('login'))


def invalid(request):
	return render(request, 'NearBeach/invalid.html', {})


def login(request):
	return render(request, 'NearBeach/login.html', {})
	

def logout(request):
	#log the user out and go to login page
	auth.logout(request)
	return HttpResponseRedirect(reverse('login'))


def new_customer(request):
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
			
			submit_form = customers(customer_title = customer_title, customer_first_name = customer_first_name, customer_last_name = customer_last_name, customer_email = customer_email)
			
			#BUG - no validation process to see if there exists a customer already :(
			submit_form.save()
			
			#Submit customer to an organisation
			#BUG MISSING FEATURE!!
			
			
			return HttpResponseRedirect(reverse(customer_information, args={submit_form.customer_id}))
		
		#If form is not valid, return to new_organisation_form.
		#Should I print something on the page?
		print("There was an error!")
		return HttpResponseRedirect(reverse('new_organisation'))
	else:
		form = new_customer_form()
	
	#load template
	t = loader.get_template('NearBeach/new_customer.html')
	
	#context
	c = {
		'new_customer_form': new_customer_form(),
	}
	
	return HttpResponse(t.render(c, request))


def new_organisation(request):
	if request.method == 'POST':
		form = new_organisation_form(request.POST)
		if form.is_valid():
			organisation_name = form.cleaned_data['organisation_name']
			organisation_email = form.cleaned_data['organisation_email']
			organisation_website = form.cleaned_data['organisation_website']
			
			submit_form = organisations(organisation_name = organisation_name, organisation_email = organisation_email, organisation_website = organisation_website)
			
			"""
			IMPORTANT!! BUG HERE!!!
			There is no validaion process what so ever! Please read bug 55
			"""
			submit_form.save()
			return HttpResponseRedirect(reverse(organisation_information, args={submit_form.organisations_id}))
		
		#If form is not valid, return to new_organisation_form.
		#Should I print something on the page?
		print("There was an error!")
		return HttpResponseRedirect(reverse('new_organisation'))
	else:
		form = new_organisation_form()
	
	#load template
	t = loader.get_template('NearBeach/new_organisation.html')
	
	#context
	c = {
		'new_organisation_form': new_organisation_form(),
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
			
			submit_project = project(project_name = project_name, project_description = project_description, organisations_id = organisations_id, project_start_date = project_start_date, project_end_date = project_end_date, project_status = 'New')
			
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
		current_user = User.objects.get()
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
		
		#Load the template
		t = loader.get_template('NearBeach/new_project.html')
		
		#context
		c = {
			'new_project_form': new_project_form(),
			'groups_results': groups_results,
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
		current_user = User.objects.get()
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


		#Loaed the template
		t = loader.get_template('NearBeach/new_task.html')
		
		c = {
			'new_task_form': new_task_form(),
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
	
	#Loaed the template
	t = loader.get_template('NearBeach/organisation_information.html')
	
	c = {
		'organisation_results': organisation_results,
	}
	
	return HttpResponse(t.render(c, request))
	

def project_history_submit(request, project_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
		
	#Obtain the value from the textarea
	project_history_text = request.POST.get("history_text", '')
	
	#Check to see if there is data - if blank just reload the page (we have gone too far)
	if project_history_text is not None:
		#First we need to get the project_id and customer_id database connections
		project_id_connection = project.objects.get(pk = project_id)
		
		#Get username_id from User
		current_user = User.objects.get(username = request.user.get_username())
		
		#Submitting the data.
		data = project_history(project_id = project_id_connection, user_id = current_user, project_history = project_history_text)
		data.save()
	
	#Return to that exact page again, user reverse to reverse engineer the 
	#exact URL
	return HttpResponseRedirect(reverse('project_information',args=(project_id,)))

	
def project_information(request, project_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
		
	#Query the database for project information
	project_information_results = project.objects.get(pk = project_id)
	project_history_results = project_history.objects.filter(project_id = project_id, is_deleted = 'FALSE')
	
	
	#Query the database for associated task information
	cursor = connection.cursor()
	cursor.execute("""
		SELECT 
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
		'project_information_results': project_information_results,
		'project_history_results': project_history_results,
		'associated_tasks_results': associated_tasks_results,
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
	
	#context
	c = {

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
	

	
def task_history_submit(request, task_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	#Obtain the value from the textarea
	task_history_text = request.POST.get("history_text", '')
	
	#Check to see if there is data - if blank just reload the page (we have gone too far)
	if task_history_text is not None:
		#First we need to get the task_id and customer id database connections
		tasks_id_connection = tasks.objects.get(pk = task_id)
		
		#Get username_id from User
		current_user = User.objects.get(username = request.user.get_username())
		
		#Submit the data
		data = tasks_history(tasks_id = tasks_id_connection, user_id = current_user, task_history = task_history_text)
		data.save()
	#Return to that exact page again, user reverse to reverse engineer the
	#exact URL
	return HttpResponseRedirect(reverse('task_information',args=(task_id,)))

 
def task_information(request, task_id):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
		
	#Gather needed information about the task
	task_information_results = tasks.objects.get(pk = task_id)
	task_history_results = tasks_history.objects.filter(tasks_id = task_id)
	
	#Load the template
	t = loader.get_template('NearBeach/task_information.html')
	
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
			AND project_tasks.task_id = '0'
		""")
	associated_project_results = namedtuplefetchall(cursor)
	
	#context
	c = {
		'task_information_results': task_information_results,
		'task_history_results': task_history_results,
		'associated_project_results': associated_project_results,
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


