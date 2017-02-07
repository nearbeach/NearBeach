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


def new_organisation(request):
	if request.method == 'POST':
		form = new_organisation_form(request.POST)
		if form.is_valid():
			organisation_name = form.cleaned_data['organisation_name']
			organisation_email = form.cleaned_data['organisation_email']
			organisation_website = form.cleaned_data['organisation_website']
			
			p = organisations(organisation_name = organisation_name, organisation_email = organisation_email, organisation_website = organisation_website)
			save_results = p.save()
		return HttpResponseRedirect('active_projects')
	else:
		form = new_organisation_form()
	
	#load template
	t = loader.get_template('NearBeach/new_organisation.html')
	
	#context
	c = {
		'new_organisation_form': new_organisation_form(),
	}
	
	return HttpResponse(t.render(c, request))
	#render_to_response('NearBeach/new_organisation.html', {'new_organisation_form': form}, context_instance = RequestContext(request))
	

		
		
	

		

def new_project(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	

	#Obtain the groups the user is associated with
	current_user = User.objects.get(username = request.user.get_username())
	#groups_count = user_groups.objects.filter(username_id = current_user.id, is_deleted = 'FALSE').count()
	cursor = connection.cursor()

	cursor.execute("""
	SELECT DISTINCT
	  groups.group_id
	, groups.group_name

	FROM 
	  user_groups join groups
		on user_groups.group_id_id = groups.group_id

	WHERE 1=1
	AND user_groups.is_deleted = "FALSE"
	AND user_groups.username_id = %s
	""", [current_user.id])
	groups_results = namedtuplefetchall(cursor)
	
	
	#Obtain all the organisations	
	organisation_results = organisations.objects.all()
	
	#Load the template
	t = loader.get_template('NearBeach/new_project.html')
	
	#Construct the sets
	set_hours = ['01',	'02',	'03',	'04',	'05',	'06',	'07',	'08',	'09',	'10',	'11',	'12',]
	set_minutes = ['00',	'05',	'10',	'15',	'20',	'25',	'30',	'35',	'40',	'45',	'50',	'55',]
	set_meridiems = ['AM','PM',]
	
	set_days = ['01',	'02',	'03',	'04',	'05',	'06',	'07',	'08',	'09',	'10',	'11',	'12',	'13',	'14',	'15',	'16',	'17',	'18',	'19',	'20',	'21',	'22',	'23',	'24',	'25',	'26',	'27',	'28',	'29',	'30',	'31',]
	set_months = ['January',	'February',	'March',	'April',	'May',	'June',	'July',	'August',	'September',	'October',	'November',	'December',]
	set_years = ['2010',	'2011',	'2012',	'2013',	'2014',	'2015',	'2016',	'2017',	'2018',	'2019',	'2020',	'2021',	'2022',	'2023',	'2024',	'2025',	'2026',	'2027',	'2028',	'2029',	'2030',	'2031',	'2032',	'2033',	'2034',	'2035',	'2036',	'2037',	'2038',	'2039',	'2040',	'2041',	'2042',	'2043',	'2044',	'2045',]
	
	#context
	c = {
		'groups_results': groups_results,
		'groups_count': len(groups_results),	#use len for the named tuple
		'organisation_results': organisation_results,
		'organisation_counts': organisation_results.count(),
		'new_project_form': new_project_form(),
		
		'set_hours': set_hours,
		'set_minutes': set_minutes,
		'set_meridiems': set_meridiems,
		'set_days': set_days,
		'set_months': set_months,
		'set_years': set_years,			
	}
	
	return HttpResponse(t.render(c, request))


def new_project_submit(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	if request.method == 'POST':
			
		#Obtain the fields of data from the form
		id_project_name = request.POST.get("id_project_name", '')
		id_project_description = request.POST.get("id_project_description", '')
		id_organisations_id = request.POST.get("id_organisations_id", '')
		
		#Collect the dates
		"""
		id_start_date = datetime.datetime(request.POST.get("start_date_year",''),
											request.POST.get("start_date_month",''),
											request.POST.get("start_date_day",''),
											request.POST.get("start_date_hour",''),
											request.POST.get("start_date_minute",''),
											)
		id_end_date = datetime.datetime(request.POST.get("end_date_year",''),
											request.POST.get("end_date_month",''),
											request.POST.get("end_date_day",''),
											request.POST.get("end_date_hour",''),
											request.POST.get("end_date_minute",''),
											)
											"""
		
		data = project(project_name = id_project_name,
						project_description = id_project_description,
						organisation_id = id_organisations_id,
						#project_start_date = id_start_date,
						#project_end_date = id_end_date,
						#project_status = "New"
						)
		
		save_results = data.save()
			
	
	return
	
	"""
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
	"""

def new_task(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	return render(request, 'NearBeach/new_task.html', {})

def new_task_submit(request):
	"""
	If the user is not logged in, we want to send them to the login page.
	This function should be in ALL webpage requests except for login and
	the index page
	"""
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	
	##ADD CODE##
	return
	
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


