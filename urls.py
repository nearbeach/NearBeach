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
	url(r'^login', views.login, name='Login'),
	url(r'^auth_view', views.auth_view, name='Authentication'),
	url(r'^logout', views.logout, name='Logout'),
	url(r'^invalid', views.invalid, name='Invalid Login'),
	
	

	

]
