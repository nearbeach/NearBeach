from django.conf.urls import include, url

#The following two imports are for the static files
from django.conf import settings
from django.conf.urls.static import static


#Password reset
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from . import views

urlpatterns = [
    #Basic URLS
    url(r'^$', views.index, name='index'),
    url(r'^active_projects/', views.active_projects, name='active_projects'),
    
    #Obtaining project and task information
	url(r'^project_information/(?P<project_id>[0-9]+)/', views.project_information, name='project_information'),
	url(r'^task_information/(?P<task_id>[0-9]+)', views.task_information, name='task_information'),


	#Login URLS
	url(r'^login', views.login, name='login'),
	url(r'^logout', views.logout, name='logout'),
	
	
	#New Items
	url(r'^new_project', views.new_project, name='new_project'),
	url(r'^new_task', views.new_task, name='new_task'),
	url(r'^new_organisation', views.new_organisation, name='new_organisation'),
	url(r'^new_customer/(?P<organisations_id>[0-9]+)/', views.new_customer, name='new_customer'),
	
	#Organisation
	url(r'^organisation_information/(?P<organisations_id>[0-9]+)/', views.organisation_information, name='organisation_information'),
	url(r'^search_organisations', views.search_organisations, name='search_organisations'),
	url(r'^new_campus/(?P<organisations_id>[0-9]+)/', views.new_campus, name='new_campus'),
	url(r'^customer_information/(?P<customer_id>[0-9]+)/', views.customer_information, name='customer_information'),
	url(r'^campus_information/(?P<campus_information>[0-9]+)/', views.campus_information, name='campus_information'),
	url(r'^customers_campus_information/(?P<customer_campus_id>[0-9]+)/(?P<customer_or_org>["CUST","CAMP"]+)', views.customers_campus_information, name="customers_campus_information"),
	url(r'^assign_customer_project_task/(?P<customer_id>[0-9]+)/', views.assign_customer_project_task, name='assign_customer_project_task'),


	#Search Items
	url(r'^search_customers', views.search_customers, name='search_customers'),
	url(r'^search_organisations', views.search_organisations, name='search_organisations'),
	url(r'^search_projects_tasks', views.search_projects_tasks, name='search_projects_tasks'),

	
	#Associated tasks/projects
	url(r'^associated_tasks/(?P<project_id>[0-9]+)/', views.associated_tasks, name='associated_tasks'),
	url(r'^associated_projects/(?P<task_id>[0-9]+)/', views.associated_projects, name='associated_projects'),
	url(r'^associate/(?P<project_id>[0-9]+)/(?P<task_id>[0-9]+)/(?P<project_or_task>[P,T])', views.associate, name='associate'),



	#Forgotten Passwords
	url(r'^password_reset/$', password_reset, {'post_reset_redirect': 'password_reset_done', 'template_name': 'NearBeach/password_reset.html'}, name='password_reset'),
	url(r'^password_reset/done/$', password_reset_done, { 'template_name': 'NearBeach/password_reset_done.html' }, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, { 'post_reset_redirect': 'password_reset_complete', 'template_name': 'NearBeach/reset.html' }, name='password_reset_confirm'),
	url(r'^reset/done/$', password_reset_complete, { 'template_name': 'NearBeach/reset_done.html' }, name='password_reset_complete'),
	
	
	#Search
	url(r'^search', views.search, name='search'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


