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
	
	
	#New Items
	url(r'^new_project', views.new_project, name='new_project'),
	url(r'^new_project_submit', views.new_project_submit, name='new_project_submit'),
	url(r'^new_task', views.new_task, name='new_task'),
	url(r'^new_task_submit', views.new_task_submit, name='new_task_submit'),
	
	

	

]
