from django.urls import path, include


#The following two imports are for the static files
from django.conf import settings
from django.conf.urls.static import static


#Password reset
"""
from django.contrib.auth.views import \
	password_reset, \
	password_reset_done, \
	password_reset_confirm, \
	password_reset_complete
"""


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
path('accounts/', include('django.contrib.auth.urls')),

	path('', views.index, name='index'),
	path('alerts/',views.alerts,name='alerts'),
	path('assign_customer_project_task/(?P<customer_id>[0-9]+)/', views.assign_customer_project_task,
		name='assign_customer_project_task'),
	path('associate/(?P<project_id>[0-9]+)/(?P<task_id>[0-9]+)/(?P<project_or_task>[P,T])', views.associate,
		name='associate'),
	path('associated_projects/(?P<task_id>[0-9]+)/', views.associated_projects, name='associated_projects'),
	path('associated_tasks/(?P<project_id>[0-9]+)/', views.associated_tasks, name='associated_tasks'),
	path('campus_information/(?P<campus_information>[0-9]+)/', views.campus_information, name='campus_information'),
	path('customers_campus_information/(?P<customer_campus_id>[0-9]+)/(?P<customer_or_org>["CUST","CAMP"]+)',
		views.customers_campus_information, name="customers_campus_information"),
	path('customer_information/(?P<customer_id>[0-9]+)/', views.customer_information, name='customer_information'),
	path('dashboard/$', views.dashboard,name='dashboard'),
	path('dashboard/active_projects', views.dashboard_active_projects,
		name='dashboard_active_projects'),
path('dashboard/active_quotes', views.dashboard_active_quotes,
		name='dashboard_active_quotes'),
path('dashboard/active_requirements', views.dashboard_active_requirements, name='dashboard_active_requirements'),
	path('dashboard/active_tasks', views.dashboard_active_tasks, name='dashboard_active_tasks'),
	path('dashboard/group_active_projects', views.dashboard_group_active_projects,name='dashboard_group_active_projects'),
	path('dashboard/group_active_tasks', views.dashboard_group_active_tasks,name='dashboard_group_active_tasks'),
	path('dashboard/group_opportunities', views.dashboard_group_opportunities, name='dashboard_group_opportunities'),
	path('dashboard/opportunities', views.dashboard_opportunities, name='dashboard_opportunities'),
	path('delete_cost/(?P<cost_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])', views.delete_cost,
		name='delete_cost'),
	path('delete_campus_contact/(?P<customers_campus_id>[0-9]+)/(?P<cust_or_camp>["CUST","CAMP"]+)',views.delete_campus_contact, name='delete_campus_contact'),

	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('new_campus/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer"]+)/$', views.new_campus, name='new_campus'),
	path('new_customer/(?P<organisations_id>[0-9]+)/', views.new_customer, name='new_customer'),
	path('new_opportunity/$', views.new_opportunity, name='new_opportunity'),
	#path('new_opportunity/(?P<organisation_id>[0-9]+)/$', views.new_opportunity, name='new_opportunity'),
	#path('new_opportunity/(?P<organisation_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views.new_opportunity,
path('new_opportunity/(?P<location_id>[0-9]+)/(?P<destination>["customer","organisation"]+)/$', views.new_opportunity,name='new_opportunity'),
	path('new_organisation', views.new_organisation, name='new_organisation'),

	path('new_project/(?P<location_id>[0-9]+)/(?P<destination>["customer","organisation","opportunity"]+)/$',views.new_project,name='new_project'),
	path('new_project/$', views.new_project, name='new_project'),
	path('new_quote/(?P<primary_key>[0-9]+)/(?P<destination>["project","task","opportunity","customer","organisation"]+)/',views.new_quote, name='new_quote'),

	path('new_task/$', views.new_task, name='new_task'),
path('new_task/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer","opportunity"]+)/$', views.new_task, name='new_task'),


	path('opportunity_information/(?P<opportunity_id>[0-9]+)/', views.opportunity_information,
		name='opportunity_information'),

	path('opportunity_information/opportunity_group_permission/(?P<opportunity_id>[0-9]+)',views.opportunity_group_permission,name='opportunity_group_permission'),
path('opportunity_information/opportunity_delete_permission/(?P<opportunity_permissions_id>[0-9]+)',views.opportunity_delete_permission,name='opportunity_delete_permission'),
path('opportunity_information/opportunity_user_permission/(?P<opportunity_id>[0-9]+)',views.opportunity_user_permission,name='opportunity_user_permission'),



	path('organisation_information/(?P<organisations_id>[0-9]+)/', views.organisation_information,
		name='organisation_information'),


	path('permission_denied', views.permission_denied, name='permission_denied'),
	path('private/(?P<document_key>[0-9A-Za-z_\-]+)/$', views.private_document, name='private'),
	path('project_information/(?P<project_id>[0-9]+)/', views.project_information, name='project_information'),
	path('quote_information/(?P<quote_id>[0-9]+)/$', views.quote_information, name='quote_information'),


	path('search_customers', views.search_customers, name='search_customers'),
	path('search_organisations', views.search_organisations, name='search_organisations'),
	path('search_projects_tasks', views.search_projects_tasks, name='search_projects_tasks'),
	path('search_users', views_administration.search_users, name='search_users'),
	path('task_information/(?P<task_id>[0-9]+)', views.task_information, name='task_information'),
	#Bug - if this line is before the other search functions, it will override other functions
	path('search/', views.search, name='search'),


	#Quotes Modules
	path('quote_list_of_line_items/(?P<quote_id>[0-9]+)/$', views_quotes.list_of_line_items, name='quote_list_of_line_items'),
	path('quote_new_line_item/(?P<quote_id>[0-9]+)/$', views_quotes.new_line_item, name='quote_new_line_item'),
	path('quote_delete_line_item/(?P<line_item_id>[0-9]+)/$', views_quotes.delete_line_item, name='quote_delete_line_item'),
	path('quote_responsible_customer/(?P<quote_id>[0-9]+)/$', views_quotes.responsible_customer, name='quote_responsible_customer'),
	path('quote_delete_responsible_customer/(?P<quote_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views_quotes.delete_responsible_customer, name='quote_delete_responsible_customer'),
	path('quote_responsible_customer/(?P<quote_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views_quotes.responsible_customer, name='quote_responsible_customer'),


	#Project Information
	path('information_project_costs/(?P<project_id>[0-9]+)/$', views_project_information.information_project_costs, name='information_project_costs'),
	path('information_project_customers/(?P<project_id>[0-9]+)/$', views_project_information.information_project_customers, name='information_project_customers'),
	path('information_project_history/(?P<project_id>[0-9]+)/$', views_project_information.information_project_history, name='information_project_history'),
	path('information_project_assign_users/(?P<project_id>[0-9]+)/$', views_project_information.information_project_assigned_users, name='information_project_assigned_users'),
	path('information_project_delete_assigned_users/(?P<project_id>[0-9]+)/(?P<location_id>[0-9]+)', views_project_information.information_project_delete_assigned_users, name='information_project_delete_assigned_users'),


	#Task Information
	path('information_task_costs/(?P<task_id>[0-9]+)/$', views_task_information.information_task_costs,
		name='information_task_costs'),
	path('information_task_customers/(?P<task_id>[0-9]+)/$', views_task_information.information_task_customers,
		name='information_task_customers'),
	path('information_task_history/(?P<task_id>[0-9]+)/$', views_task_information.information_task_history,
		name='information_task_history'),
	path('information_task_assign_users/(?P<task_id>[0-9]+)/$', views_task_information.information_task_assigned_users,
		name='information_task_assigned_users'),



	path('information_task_delete_assigned_users/(?P<task_id>[0-9]+)/(?P<user_id>[0-9]+)/$', views_task_information.information_task_delete_assigned_users,
		name='information_task_delete_assigned_users'),

	# organisation Information
	path('information_organisation_contact_history/(?P<organisation_id>[0-9]+)/$',
		views_organisation_information.information_organisation_contact_history,
		name='information_organisation_contact_history'),
	path('information_organisation_documents_list/(?P<organisation_id>[0-9]+)/$',
		views_organisation_information.information_organisation_documents_list,
		name='information_organisation_documents_list'),
	path('information_organisation_documents_uploads/(?P<organisation_id>[0-9]+)/$',
		views_organisation_information.information_organisation_documents_upload,
		name='information_organisation_documents_uploads'),

	# customer Information
	path('information_customer_contact_history/(?P<customer_id>[0-9]+)/$',
		views_customer_information.information_customer_contact_history,
		name='information_customer_contact_history'),
	path('information_customer_documents_upload/(?P<customer_id>[0-9]+)/$',
		views_customer_information.information_customer_documents_upload,
		name='information_customer_documents_upload'),
	path('information_customer_documents_list/(?P<customer_id>[0-9]+)/$',
		views_customer_information.information_customer_documents_list,
		name='information_customer_documents_list'),

	path('information_customer_documents_list/(?P<customer_id>[0-9]+)/(?P<organisations_id>[0-9]+)/$',
		views_customer_information.information_customer_documents_list,
		name='information_customer_documents_list'),

	#Look up
	path('lookup_product/(?P<product_id>[0-9]+)/$', views_lookup.lookup_product, name='lookup_product'),

	#Resolve
	path('resolve_project/(?P<project_id>[0-9]+)/', views.resolve_project,	name='resolve_project'),
	path('resolve_task/(?P<task_id>[0-9]+)/', views.resolve_task,	name='resolve_task'),

	#Document functions
	path('delete_document/(?P<document_key>[0-9A-Za-z_\-]+)/$', views.delete_document, name='delete_document'),
	path('rename_document/(?P<document_key>[0-9A-Za-z_\-]+)/$', views.rename_document, name='rename_document'),

	#Document Tree
	path('document_tree_list/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/$', views_document_tree.document_tree_list,name='document_tree_list'),
	path('document_tree_list/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/(?P<folder_id>[0-9]+)/', views_document_tree.document_tree_list,name='document_tree_list'),

	path('document_tree_upload/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/', views_document_tree.document_tree_upload, name='document_tree_upload'),
	path('document_tree_upload_documents/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/', views_document_tree.document_tree_upload_documents, name='document_tree_upload_documents'),

	path('document_tree_create_folder/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])/', views_document_tree.document_tree_create_folder, name='document_tree_create_folder'),

	#requirements
	path('new_requirement/', views_requirements.new_requirement,
		name="new_requirement"),
	path('requirement_information/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_information,
		name="requirement_information"),
	path('requirement_item_edit/(?P<requirement_item_id>[0-9]+)/', views_requirements.requirement_item_edit,
		name="requirement_item_edit"),
	path('requirement_items_list/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_items_list,
		name="requirement_items_list"),
	path('requirement_items_new/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_items_new,
		name="requirement_items_new"),
	path('requirement_items_new_link/(?P<requirement_item_id>[0-9]+)/$', views_requirements.requirement_items_new_link,
		name="requirement_items_new_link"),
path('requirement_items_new_link/(?P<requirement_item_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)',
	views_requirements.requirement_items_new_link, name="requirement_items_new_link"),
	path('requirement_links_list/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_links_list,
		name="requirement_links_list"),
	path('requirement_new_link/(?P<requirement_id>[0-9]+)/$', views_requirements.requirement_new_link,
		name="requirement_new_link"),
	path('requirement_documents_uploads/(?P<location_id>[0-9]+)/(?P<destination>["requirement","requirement_item"]+)'
		, views_requirements.requirement_documents_uploads
		, name='requirement_documents_uploads'),

path('requirement_new_link/(?P<requirement_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)'
	, views_requirements.requirement_new_link,
		name="requirement_new_link"),

path('user_permissions', views_lookup.lookup_user_permissions, name='user_permissions'),

	#Permission sets
	path('permission_set_information/',views_administration.permission_set_information, name='permission_set_information'),
	path('permission_set_information_edit/(?P<permission_set_id>[0-9]+)/$', views_administration.permission_set_information_edit,
		name='permission_set_information_edit'),
	path('permission_set_information_list/',views_administration.permission_set_information_list, name='permission_set_information_list'),
	path('permission_set_information_create/', views_administration.permission_set_information_create,
		name='permission_set_information_create'),


path('group_information/', views_administration.group_information, name='group_information'),
	path('group_information_create/', views_administration.group_information_create, name='group_information_create'),
path('group_information_edit/(?P<group_id>[0-9]+)/', views_administration.group_information_edit, name='group_information_edit'),
path('group_information_edit_users/(?P<group_id>[0-9]+)/', views_administration.group_information_edit_users, name='group_information_edit_users'),
path('group_information_list/', views_administration.group_information_list, name='group_information_list'),
path('group_information_add_permission_set/(?P<group_id>[0-9]+)/', views_administration.group_information_add_permission_set, name='group_information_add_permission_set'),

	#User information
	path('new_user/$', views_administration.new_user, name='new_user'),
	path('user_information/(?P<user_id>[0-9]+)/$', views_administration.user_information, name='user_information'),

path('product_and_service_search/', views_administration.product_and_service_search, name='product_and_service_search'),
path('product_and_service_new/', views_administration.product_and_service_new, name='product_and_service_new'),
path('product_and_service_discontinued/(?P<product_id>[0-9]+)/', views_administration.product_and_service_discontinued, name='product_and_service_discontinued'),
path('product_and_service_edit/(?P<product_id>[0-9]+)/', views_administration.product_and_service_edit, name='product_and_service_edit'),

path('assigned_group_add/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)/$', views.assigned_group_add , name='assigned_group_add'),
path('assigned_group_add/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)/(?P<group_id>[0-9]+)', views.assigned_group_add , name='assigned_group_add'),
path('assigned_group_delete/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)/', views.assigned_group_delete , name='assigned_group_delete'),
path('assigned_group_list/(?P<location_id>[0-9]+)/(?P<destination>["project","task","organisation"]+)/', views.assigned_group_list , name='assigned_group_list'),

path('list_of_taxes_information/', views_administration.list_of_taxes_information, name='list_of_taxes_information'),
path('list_of_taxes_list/', views_administration.list_of_taxes_list, name='list_of_taxes_list'),
path('list_of_taxes_edit/(?P<tax_id>[0-9]+)/', views_administration.list_of_taxes_edit, name='list_of_taxes_edit'),
path('list_of_taxes_new/', views_administration.list_of_taxes_new, name='list_of_taxes_new'),
path('list_of_taxes_deactivate/(?P<tax_id>[0-9]+)/', views_administration.list_of_taxes_deactivate, name='list_of_taxes_deactivate'),

#Kanban Board
	path('kanban_list/', views.kanban_list,name='kanban_list'),
	path('kanban_information/(?P<kanban_board_id>[0-9]+)/', views.kanban_information, name='kanban_information'),
	path('kanban_move_card/(?P<kanban_card_id>[0-9]+)/(?P<kanban_column_id>[0-9]+)/(?P<kanban_level_id>[0-9]+)/', views.kanban_move_card, name='kanban_move_card'),
	path('kanban_new_card/(?P<kanban_board_id>[0-9]+)/$', views.kanban_new_card,name='kanban_new_card'),
	path('kanban_edit_card/(?P<kanban_card_id>[0-9]+)/$', views.kanban_edit_card,name='kanban_edit_card'),
path('kanban_properties/(?P<kanban_board_id>[0-9]+)/$', views.kanban_properties,name='kanban_properties'),
path('new_kanban_board/$', views.new_kanban_board,name='new_kanban_board'),
path('kanban_new_link/(?P<kanban_board_id>[0-9]+)/$', views.kanban_new_link,name='kanban_new_link'),
path('kanban_new_link/(?P<kanban_board_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/$', views.kanban_new_link,name='kanban_new_link'),
	path('to_do/(?P<location_id>[0-9]+)/(?P<destination>["project","task","opportunity"]+)/$', views.to_do_list, name='to_do'),
path('to_do_complete/(?P<to_do_id>[0-9]+)/$', views.to_do_complete, name='to_do_complete'),

	path('bug_client_list/$',views.bug_client_list,name='bug_client_list'),
	path('new_bug_client/$',views.new_bug_client, name='new_bug_client'),

	path('bug_list/$', views.bug_list, name='bug_list'),
	path('bug_list/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/$', views.bug_list, name='bug_list'),

	path('bug_search/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/$', views.bug_search, name='bug_search'),

	path('bug_add/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/(?P<bug_id>[0-9]+)/(?P<bug_client_id>[0-9]+)',views.bug_add,name='bug_add'),
	path('bug_client_information/(?P<bug_client_id>[0-9]+)/$', views.bug_client_information,name='bug_client_information'),
	path('bug_client_delete/(?P<bug_client_id>[0-9]+)/$', views.bug_client_delete, name='bug_client_delete'),

	path('kanban_edit_xy_name/(?P<location_id>[0-9]+)/(?P<destination>["column","level"]+)/$', views.kanban_edit_xy_name,name='kanban_edit_xy_name'),
path('email/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer","project","task","opportunity","quote"]+)/$', views.email,name='email'),
path('email_history/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer","project","task","opportunity","quote"]+)/$', views.email_history,name='email_history'),
path('email_information/(?P<email_content_id>[0-9]+)/$', views.email_information,name='email_information'),
path('timeline/$', views.timeline, name='timeline'),
path('timeline_data/(?P<destination>["project","task"]+)/$', views.timeline_data, name='timeline_data'),
path('add_campus_to_customer/(?P<customer_id>[0-9]+)/(?P<campus_id>[0-9]+)/', views.add_campus_to_customer,name='add_campus_to_customer'),
path('search_templates/',views.search_templates,name='search_templates'),
    path('new_quote_template/',views.new_quote_template,name='new_quote_template'),
	path('quote_template_information/(?P<quote_template_id>[0-9]+)/',views.quote_template_information,name='quote_template_information'),
	path('preview_quote/(?P<quote_uuid>[0-9A-Za-z_\-]+)/(?P<quote_template_id>[0-9]+)/',views.preview_quote,name='preview_quote'),
	path('extract_quote/(?P<quote_uuid>[0-9A-Za-z_\-]+)/(?P<quote_template_id>[0-9]+)/', views.extract_quote,
		name='extract_quote'),

	#ADD IN PASSWORD RESET

]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


