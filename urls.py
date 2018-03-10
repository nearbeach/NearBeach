from django.conf.urls import include, url


#The following two imports are for the static files
from django.conf import settings
from django.conf.urls.static import static


#Password reset
from django.contrib.auth.views import \
	password_reset, \
	password_reset_done, \
	password_reset_confirm, \
	password_reset_complete

from . import views, \
	views_lookup, \
	views_quotes, \
	views_project_information, \
	views_task_information, \
	views_organisation_information, \
	views_customer_information, \
	views_document_tree, \
	views_requirements, \
	views_administration

urlpatterns = [
	url(r'^$', views.index, name='index'),
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
	#url(r'^new_opportunity/(?P<organisation_id>[0-9]+)/$', views.new_opportunity, name='new_opportunity'),
	#url(r'^new_opportunity/(?P<organisation_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views.new_opportunity,
url(r'^new_opportunity/(?P<location_id>[0-9]+)/(?P<destination>["customer","organisation"]+)/$', views.new_opportunity,name='new_opportunity'),
	url(r'^new_organisation', views.new_organisation, name='new_organisation'),
	url(r'^new_project/$', views.new_project, name='new_project'),
	url(r'^new_project/(?P<location_id>[0-9]+)/(?P<destination>["customer","organisation","opportunity"]+)/',views.new_project,name='new_project'),
	url(r'^new_quote/(?P<primary_key>[0-9]+)/(?P<destination>["project","task","opportunity","customer","organisation"]+)/',views.new_quote, name='new_quote'),

	url(r'^new_task/$', views.new_task, name='new_task'),
url(r'^new_task/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer","opportunity"]+)/$', views.new_task, name='new_task'),

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
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
		{'post_reset_redirect': 'password_reset_complete', 'template_name': 'NearBeach/reset.html'},
		name='password_reset_confirm'),
	url(r'^reset/done/$', password_reset_complete, {'template_name': 'NearBeach/reset_done.html'},
		name='password_reset_complete'),
	url(r'^search_customers', views.search_customers, name='search_customers'),
	url(r'^search_organisations', views.search_organisations, name='search_organisations'),
	url(r'^search_projects_tasks', views.search_projects_tasks, name='search_projects_tasks'),
	url(r'^search_users', views_administration.search_users, name='search_users'),
	url(r'^task_information/(?P<task_id>[0-9]+)', views.task_information, name='task_information'),
	#Bug - if this line is before the other search functions, it will override other functions
	url(r'^search', views.search, name='search'),


	#Quotes Modules
	url(r'^quote_list_of_line_items/(?P<quote_id>[0-9]+)/$', views_quotes.list_of_line_items, name='quote_list_of_line_items'),
	url(r'^quote_new_line_item/(?P<quote_id>[0-9]+)/$', views_quotes.new_line_item, name='quote_new_line_item'),
	url(r'^quote_delete_line_item/(?P<line_item_id>[0-9]+)/$', views_quotes.delete_line_item, name='quote_delete_line_item'),
	url(r'^quote_responsible_customer/(?P<quote_id>[0-9]+)/$', views_quotes.responsible_customer, name='quote_responsible_customer'),
	url(r'^quote_delete_responsible_customer/(?P<quote_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views_quotes.delete_responsible_customer, name='quote_delete_responsible_customer'),
	url(r'^quote_responsible_customer/(?P<quote_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views_quotes.responsible_customer, name='quote_responsible_customer'),


	#Project Information
	url(r'^information_project_costs/(?P<project_id>[0-9]+)/$', views_project_information.information_project_costs, name='information_project_costs'),
	url(r'^information_project_customers/(?P<project_id>[0-9]+)/$', views_project_information.information_project_customers, name='information_project_customers'),
	url(r'^information_project_history/(?P<project_id>[0-9]+)/$', views_project_information.information_project_history, name='information_project_history'),
	url(r'^information_project_assign_users/(?P<project_id>[0-9]+)/$', views_project_information.information_project_assigned_users, name='information_project_assigned_users'),
	url(r'^information_project_delete_assigned_users/(?P<project_id>[0-9]+)/(?P<location_id>[0-9]+)', views_project_information.information_project_delete_assigned_users, name='information_project_delete_assigned_users'),


	#Task Information
	url(r'^information_task_costs/(?P<task_id>[0-9]+)/$', views_task_information.information_task_costs,
		name='information_task_costs'),
	url(r'^information_task_customers/(?P<task_id>[0-9]+)/$', views_task_information.information_task_customers,
		name='information_task_customers'),
	url(r'^information_task_history/(?P<task_id>[0-9]+)/$', views_task_information.information_task_history,
		name='information_task_history'),
	url(r'^information_task_assign_users/(?P<task_id>[0-9]+)/$', views_task_information.information_task_assigned_users,
		name='information_task_assigned_users'),



	url(r'^information_task_delete_assigned_users/(?P<task_id>[0-9]+)/(?P<user_id>[0-9]+)/$', views_task_information.information_task_delete_assigned_users,
		name='information_task_delete_assigned_users'),

	# organisation Information
	url(r'^information_organisation_contact_history/(?P<organisation_id>[0-9]+)/$',
		views_organisation_information.information_organisation_contact_history,
		name='information_organisation_contact_history'),
	url(r'^information_organisation_documents_list/(?P<organisation_id>[0-9]+)/$',
		views_organisation_information.information_organisation_documents_list,
		name='information_organisation_documents_list'),
	url(r'^information_organisation_documents_uploads/(?P<organisation_id>[0-9]+)/$',
		views_organisation_information.information_organisation_documents_upload,
		name='information_organisation_documents_uploads'),

	# customer Information
	url(r'^information_customer_contact_history/(?P<customer_id>[0-9]+)/$',
		views_customer_information.information_customer_contact_history,
		name='information_customer_contact_history'),
	url(r'^information_customer_documents_upload/(?P<customer_id>[0-9]+)/$',
		views_customer_information.information_customer_documents_upload,
		name='information_customer_documents_upload'),
	url(r'^information_customer_documents_list/(?P<customer_id>[0-9]+)/$',
		views_customer_information.information_customer_documents_list,
		name='information_customer_documents_list'),

	url(r'^information_customer_documents_list/(?P<customer_id>[0-9]+)/(?P<organisations_id>[0-9]+)/$',
		views_customer_information.information_customer_documents_list,
		name='information_customer_documents_list'),

	#Look up
	url(r'^lookup_product/(?P<product_id>[0-9]+)/$', views_lookup.lookup_product, name='lookup_product'),

	#Resolve
	url(r'^resolve_project/(?P<project_id>[0-9]+)/', views.resolve_project,	name='resolve_project'),
	url(r'^resolve_task/(?P<task_id>[0-9]+)/', views.resolve_task,	name='resolve_task'),

	#Document functions
	url(r'^delete_document/(?P<document_key>[0-9A-Za-z_\-]+)/$', views.delete_document, name='delete_document'),
	url(r'^rename_document/(?P<document_key>[0-9A-Za-z_\-]+)/$', views.rename_document, name='rename_document'),

	#Document Tree
	url(r'^document_tree_list/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/$', views_document_tree.document_tree_list,name='document_tree_list'),
	url(r'^document_tree_list/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/(?P<folder_id>[0-9]+)/', views_document_tree.document_tree_list,name='document_tree_list'),

	url(r'^document_tree_upload/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/', views_document_tree.document_tree_upload, name='document_tree_upload'),
	url(r'^document_tree_upload_documents/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/', views_document_tree.document_tree_upload_documents, name='document_tree_upload_documents'),

	url(r'^document_tree_create_folder/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/', views_document_tree.document_tree_create_folder, name='document_tree_create_folder'),

	#requirements
	url(r'^new_requirement/', views_requirements.new_requirement,
		name="new_requirement"),
	url(r'^requirement_information/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_information,
		name="requirement_information"),
	url(r'^requirement_item_edit/(?P<requirement_item_id>[0-9]+)/', views_requirements.requirement_item_edit,
		name="requirement_item_edit"),
	url(r'^requirement_items_list/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_items_list,
		name="requirement_items_list"),
	url(r'^requirement_items_new/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_items_new,
		name="requirement_items_new"),
	url(r'^requirement_items_new_link/(?P<requirement_item_id>[0-9]+)/$', views_requirements.requirement_items_new_link,
		name="requirement_items_new_link"),
url(r'^requirement_items_new_link/(?P<requirement_item_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)',
	views_requirements.requirement_items_new_link, name="requirement_items_new_link"),
	url(r'^requirement_links_list/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_links_list,
		name="requirement_links_list"),
	url(r'^requirement_new_link/(?P<requirement_id>[0-9]+)/$', views_requirements.requirement_new_link,
		name="requirement_new_link"),

url(r'^requirement_new_link/(?P<requirement_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)'
	, views_requirements.requirement_new_link,
		name="requirement_new_link"),

url(r'^user_permissions', views_lookup.lookup_user_permissions, name='user_permissions'),

	#Permission sets
	url(r'^permission_set_information/',views_administration.permission_set_information, name='permission_set_information'),
	url(r'^permission_set_information_edit/(?P<permission_set_id>[0-9]+)/$', views_administration.permission_set_information_edit,
		name='permission_set_information_edit'),
	url(r'^permission_set_information_list/',views_administration.permission_set_information_list, name='permission_set_information_list'),
	url(r'^permission_set_information_create/', views_administration.permission_set_information_create,
		name='permission_set_information_create'),


url(r'^group_information/', views_administration.group_information, name='group_information'),
	url(r'^group_information_create/', views_administration.group_information_create, name='group_information_create'),
url(r'^group_information_edit/(?P<group_id>[0-9]+)/', views_administration.group_information_edit, name='group_information_edit'),
url(r'^group_information_edit_users/(?P<group_id>[0-9]+)/', views_administration.group_information_edit_users, name='group_information_edit_users'),
url(r'^group_information_list/', views_administration.group_information_list, name='group_information_list'),
url(r'^group_information_add_permission_set/(?P<group_id>[0-9]+)/', views_administration.group_information_add_permission_set, name='group_information_add_permission_set'),

	#User information
	url(r'^new_user/$', views_administration.new_user, name='new_user'),
	url(r'^user_information/(?P<user_id>[0-9]+)/$', views_administration.user_information, name='user_information'),

url(r'^product_and_service_search/', views_administration.product_and_service_search, name='product_and_service_search'),
url(r'^product_and_service_new/', views_administration.product_and_service_new, name='product_and_service_new'),
url(r'^product_and_service_discontinued/(?P<product_id>[0-9]+)/', views_administration.product_and_service_discontinued, name='product_and_service_discontinued'),
url(r'^product_and_service_edit/(?P<product_id>[0-9]+)/', views_administration.product_and_service_edit, name='product_and_service_edit'),

url(r'^assigned_group_add/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)/$', views.assigned_group_add , name='assigned_group_add'),
url(r'^assigned_group_add/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)/(?P<group_id>[0-9]+)', views.assigned_group_add , name='assigned_group_add'),
url(r'^assigned_group_delete/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)/', views.assigned_group_delete , name='assigned_group_delete'),
url(r'^assigned_group_list/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)/', views.assigned_group_list , name='assigned_group_list'),

url(r'^list_of_taxes_information/', views_administration.list_of_taxes_information, name='list_of_taxes_information'),
url(r'^list_of_taxes_list/', views_administration.list_of_taxes_list, name='list_of_taxes_list'),
url(r'^list_of_taxes_edit/(?P<tax_id>[0-9]+)/', views_administration.list_of_taxes_edit, name='list_of_taxes_edit'),
url(r'^list_of_taxes_new/', views_administration.list_of_taxes_new, name='list_of_taxes_new'),
url(r'^list_of_taxes_deactivate/(?P<tax_id>[0-9]+)/', views_administration.list_of_taxes_deactivate, name='list_of_taxes_deactivate'),

#Kanban Board
	url(r'^kanban_list/', views.kanban_list,name='kanban_list'),
	url(r'^kanban_information/(?P<kanban_board_id>[0-9]+)/', views.kanban_information, name='kanban_information'),
	url(r'^kanban_move_card/(?P<kanban_card_id>[0-9]+)/(?P<kanban_column_id>[0-9]+)/(?P<kanban_level_id>[0-9]+)/', views.kanban_move_card, name='kanban_move_card'),
	url(r'^kanban_new_card/(?P<kanban_board_id>[0-9]+)/$', views.kanban_new_card,name='kanban_new_card'),
	url(r'^kanban_edit_card/(?P<kanban_card_id>[0-9]+)/$', views.kanban_edit_card,name='kanban_edit_card'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


