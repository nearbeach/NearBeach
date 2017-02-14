from django.conf.urls import url

from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    #Basic URLS
    url(r'^$', views.index, name='index'),
    url(r'^active_projects/', views.active_projects, name='active_projects'),
    
    #Obtaining project and task information
	url(r'^project_information/(?P<project_id>[0-9]+)/', views.project_information, name='project_information'),
	url(r'^project_information/(?P<project_id>[0-9]+)/(?P<task_id>[0-9]+)', views.project_information, name='project_information'),
	url(r'^task_information/(?P<task_id>[0-9]+)', views.task_information, name='task_information'),
	
	#Submitting project and task history
	url(r'^project_history_submit/(?P<project_id>[0-9]+)/', views.project_history_submit, name='project_history_submit'),
	url(r'^task_history_submit/(?P<task_id>[0-9]+)/', views.task_history_submit, name='task_history_submit'),
	
	#Login URLS
	url(r'^login', views.login, name='login'),
	url(r'^auth_view', views.auth_view, name='authentication'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^invalid', views.invalid, name='invalid_login'),
	url(r'^logout', views.logout, name='logout'),
	
	
	#New Items
	url(r'^new_project', views.new_project, name='new_project'),
	url(r'^new_task', views.new_task, name='new_task'),
	url(r'^new_organisation', views.new_organisation, name='new_organisation'),
	url(r'^new_customer', views.new_customer, name='new_customer'),
	
	#Organisation
	url(r'^organisation_information/(?P<organisations_id>[0-9]+)/', views.organisation_information, name='organisation_information'),
	url(r'^search_organisations', views.search_organisations, name='search_organisations'),
	url(r'^customer_information/(?P<customer_id>[0-9]+)/', views.customer_information, name='customer_information'),
	
	#Search Items
	url(r'^search_customers', views.search_customers, name='search_customers'),
	url(r'^search_organisations', views.search_organisations, name='search_organisations'),
	url(r'^search_projects_tasks', views.search_projects_tasks, name='search_projects_tasks'),
	

]
