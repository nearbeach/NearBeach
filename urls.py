from django.conf.urls import include, url


#The following two imports are for the static files
from django.conf import settings
from django.conf.urls.static import static


#Password reset
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from . import views, views_lookup, views_quotes, views_project_information

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^active_projects/', views.active_projects, name='active_projects'),
	url(r'^assign_customer_project_task/(?P<customer_id>[0-9]+)/', views.assign_customer_project_task,
		name='assign_customer_project_task'),
	url(r'^associate/(?P<project_id>[0-9]+)/(?P<task_id>[0-9]+)/(?P<project_or_task>[P,T])', views.associate,
		name='associate'),
	url(r'^associated_projects/(?P<task_id>[0-9]+)/', views.associated_projects, name='associated_projects'),
	url(r'^associated_tasks/(?P<project_id>[0-9]+)/', views.associated_tasks, name='associated_tasks'),
	url(r'^campus_information/(?P<campus_information>[0-9]+)/', views.campus_information, name='campus_information'),
	url(r'^customers_campus_information/(?P<customer_campus_id>[0-9]+)/(?P<customer_or_org>["CUST","CAMP"]+)',
		views.customers_campus_information, name="customers_campus_information"),
	url(r'^customer_information/(?P<customer_id>[0-9]+)/', views.customer_information, name='customer_information'),
	url(r'^dashboard/$', views.dashboard,name='dashboard'),
	url(r'dashboard/active_projects', views.dashboard_active_projects,
		name='dashboard_active_projects'),
	url(r'dashboard/active_tasks', views.dashboard_active_tasks, name='dashboard_active_tasks'),
	url(r'dashboard/group_active_projects', views.dashboard_group_active_projects,name='dashboard_group_active_projects'),
	url(r'dashboard/group_active_tasks', views.dashboard_group_active_tasks,name='dashboard_group_active_tasks'),
	url(r'dashboard/group_opportunities', views.dashboard_group_opportunities, name='dashboard_group_opportunities'),
	url(r'dashboard/opportunities', views.dashboard_opportunities, name='dashboard_opportunities'),
	url(r'^delete_cost/(?P<cost_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])', views.delete_cost,
		name='delete_cost'),
	url(r'^delete_campus_contact/(?P<customers_campus_id>[0-9]+)/(?P<cust_or_camp>["CUST","CAMP"]+)',views.delete_campus_contact, name='delete_campus_contact'),
	url(r'^delete_opportunity_permission/(?P<opportunity_id>[0-9]+)/(?P<groups_id>[0-9]+)/(?P<assigned_user>[0-9]+)',
		views.delete_opportunity_permission, name='delete_opportunity_permission'),
	url(r'^login', views.login, name='login'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^new_campus/(?P<organisations_id>[0-9]+)/', views.new_campus, name='new_campus'),
	url(r'^new_customer/(?P<organisations_id>[0-9]+)/', views.new_customer, name='new_customer'),
	url(r'^new_opportunity/$', views.new_opportunity, name='new_opportunity'),
	url(r'^new_opportunity/(?P<organisation_id>[0-9]+)/$', views.new_opportunity, name='new_opportunity'),
	url(r'^new_opportunity/(?P<organisation_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views.new_opportunity,
		name='new_opportunity'),
	url(r'^new_organisation', views.new_organisation, name='new_organisation'),
	url(r'^new_project/$', views.new_project, name='new_project'),
	url(r'^new_project/(?P<organisations_id>[0-9]+)/$', views.new_project, name='new_project'),
	url(r'^new_project/(?P<organisations_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views.new_project, name='new_project'),
	url(r'^new_quote/(?P<primary_key>[0-9]+)/(?P<destination>["project","task","opportunity"]+)/',views.new_quote, name='new_quote'),

	url(r'^new_task/$', views.new_task, name='new_task'),
	url(r'^new_task/(?P<organisations_id>[0-9]+)/$', views.new_task, name='new_task'),
	url(r'^new_task/(?P<organisations_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views.new_task, name='new_task'),
	url(r'^new_task/(?P<organisations_id>[0-9]+)/(?P<customer_id>[0-9]+)/(?P<opportunity_id>[0-9]+)/', views.new_task, name='new_task'),
	url(r'^next_step/(?P<next_step_id>[0-9]+)/(?P<opportunity_id>[0-9]+)', views.next_step, name="next_step"),
	url(r'^opportunity_information/(?P<opportunity_id>[0-9]+)/', views.opportunity_information,
		name='opportunity_information'),
	url(r'^organisation_information/(?P<organisations_id>[0-9]+)/', views.organisation_information,
		name='organisation_information'),
	url(r'^password_reset/$', password_reset,
		{'post_reset_redirect': 'password_reset_done', 'template_name': 'NearBeach/password_reset.html'},
		name='password_reset'),
	url(r'^password_reset/done/$', password_reset_done, {'template_name': 'NearBeach/password_reset_done.html'},
		name='password_reset_done'),
	url(r'^permission_denied', views.permission_denied, name='permission_denied'),
	url(r'^private/(?P<document_key>[0-9A-Za-z_\-]+)/$', views.private_document, name='private'),
	url(r'^project_information/(?P<project_id>[0-9]+)/', views.project_information, name='project_information'),
	url(r'^quote_information/(?P<quote_id>[0-9]+)/$', views.quote_information, name='quote_information'),
	#url(r'^quote_information/(?P<quote_id>[0-9]+)/line_items/', views_quotes.line_items, name='quotes_line_items'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
		{'post_reset_redirect': 'password_reset_complete', 'template_name': 'NearBeach/reset.html'},
		name='password_reset_confirm'),
	url(r'^reset/done/$', password_reset_complete, {'template_name': 'NearBeach/reset_done.html'},
		name='password_reset_complete'),
	url(r'^search_customers', views.search_customers, name='search_customers'),
	url(r'^search_organisations', views.search_organisations, name='search_organisations'),
	url(r'^search_projects_tasks', views.search_projects_tasks, name='search_projects_tasks'),
	url(r'^task_information/(?P<task_id>[0-9]+)', views.task_information, name='task_information'),
	#Bug - if this line is before the other search functions, it will override other functions
	url(r'^search', views.search, name='search'),


	#Quotes Modules
	url(r'^quote_list_of_line_items/(?P<quote_id>[0-9]+)/$', views_quotes.list_of_line_items, name='quote_list_of_line_items'),
	url(r'^quote_new_line_item/(?P<quote_id>[0-9]+)/$', views_quotes.new_line_item, name='quote_new_line_item'),
	url(r'^quote_delete_line_item/(?P<line_item_id>[0-9]+)/$', views_quotes.delete_line_item, name='quote_delete_line_item'),


	#Project Information
	url(r'^information_project_costs/(?P<project_id>[0-9]+)/$', views_project_information.information_project_costs, name='information_project_costs'),
	url(r'^information_project_customers/(?P<project_id>[0-9]+)/$', views_project_information.information_project_customers, name='information_project_customers'),
	url(r'^information_project_history/(?P<project_id>[0-9]+)/$', views_project_information.information_project_history, name='information_project_history'),
	url(r'^information_project_assign_users/(?P<project_id>[0-9]+)/$', views_project_information.information_project_assigned_users, name='information_project_assigned_users'),


	#Look up
	url(r'^lookup_product/(?P<product_id>[0-9]+)/$', views_lookup.lookup_product, name='lookup_product')

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


