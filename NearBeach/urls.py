from django.urls import path, include


#The following two imports are for the static files
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path


#Password reset
from django.contrib.auth import views as auth_views


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
	views_administration, \
	views_whiteboard
"""
from .views import authentication_views, \
	customer_views, \
	dashboard_views, \
	document_views, \
	kanban_views, \
	object_data_views, \
	organisation_views, \
	project_views, \
	requirement_item_views, \
	requirement_views, \
	search_views, \
	task_views

urlpatterns = [
	path('', dashboard_views.dashboard, name='dashboard'),

	# Customer
	path('customer_information/<int:customer_id>/',customer_views.customer_information,name='customer_information'),
	path('customer_information/<int:customer_id>/save/',customer_views.customer_information_save,name='customer_information_save'),

	# Dashboard
	path('dashboard/get/bug_list/',dashboard_views.get_bug_list,name='get_bug_list'),
	path('dashboard/get/my_objects/',dashboard_views.get_my_objects,name='get_my_objects'),

	# Documentation
	path('documentation/<destination>/<location_id>/add_folder/',document_views.document_add_folder,name='document_add_folder'),
	path('documentation/<destination>/<location_id>/add_link/',document_views.document_add_link,name='document_add_link'),
	path('documentation/<destination>/<location_id>/list/files/',document_views.document_list_files,name='document_list_files'),
	path('documentation/<destination>/<location_id>/list/folders/',document_views.document_list_folders,name='document_list_folders'),
	path('documentation/<destination>/<location_id>/upload/',document_views.document_upload,name='document_upload'),


	# Kanban
	path('kanban_information/<int:kanban_board_id>/',kanban_views.kanban_information,name='kanban_information'),
	path('kanban_information/<int:kanban_board_id>/<object_lookup>/add_link/',kanban_views.add_kanban_link,name='add_kanban_link'),
	path('kanban_information/<int:kanban_board_id>/<object_lookup>/link_list/',kanban_views.kanban_link_list,name='kanban_link_list'),
	path('kanban_information/<int:kanban_board_id>/new_card/',kanban_views.new_kanban_card,name='new_kanban_card'),
	path('kanban_information/<int:kanban_card_id>/move_card/',kanban_views.move_kanban_card,name='move_kanban_card'),
	path('kanban_information/check_kanban_board_name/',kanban_views.check_kanban_board_name,name='check_kanban_board_name'),


	# Authentication
	path('login', authentication_views.login, name='login'),
	path('logout', authentication_views.logout, name='logout'),

	# Private files
	path('private/<uuid:document_key>/',document_views.private_download_file,name='private_download_file'),

	# New Objects
	path('new_customer/',customer_views.new_customer,name='new_customer'),
	path('new_customer/save/',customer_views.new_customer_save,name='new_customer_save'),
	path('new_kanban/',kanban_views.new_kanban,name='new_kanban'),
	path('new_kanban_save/',kanban_views.new_kanban_save,name='new_kanban_save'),
	path('new_organisation/',organisation_views.new_organisation,name='new_organisation'),
	path('new_organisation/save/',organisation_views.new_organisation_save,name='new_organisation_save'),
	path('new_project/',project_views.new_project,name='new_project'),
	path('new_project/save/',project_views.new_project_save,name='new_project_save'),
	path('new_requirement/',requirement_views.new_requirement, name='new_requirement'),
	path('new_requirement/save/',requirement_views.new_requirement_save, name='new_requirement_save'),
	path('new_requirement_item/save/<int:requirement_id>/',requirement_item_views.new_requirement_item,name='new_requirement_item'),
	path('new_task/',task_views.new_task,name='new_task'),
	path('new_task/save/',task_views.new_task_save,name='new_task_save'),

	# Object Data
	path('object_data/<destination>/<location_id>/add_bug/',object_data_views.add_bug,name='add_bug'),
	path('object_data/<destination>/<location_id>/add_customer/',object_data_views.add_customer,name='add_customer'),
	path('object_data/<destination>/<location_id>/add_group/',object_data_views.add_group,name='add_group'),
	path('object_data/<destination>/<location_id>/add_notes/',object_data_views.add_notes,name='add_notes'),
	path('object_data/<destination>/<location_id>/add_user/',object_data_views.add_user,name='add_user'),
	path('object_data/<destination>/<location_id>/associated_objects/',object_data_views.associated_objects,name='associated_objects'),
	path('object_data/bug_client_list/',object_data_views.bug_client_list,name='bug_client_list'),
	path('object_data/<destination>/<location_id>/bug_list/',object_data_views.bug_list,name='bug_list'),
	path('object_data/<destination>/<location_id>/customer_list/',object_data_views.customer_list,name='customer_list'),
	path('object_data/<destination>/<location_id>/customer_list_all/',object_data_views.customer_list_all,name='customer_list_all'),
	path('object_data/<destination>/<location_id>/group_list/',object_data_views.group_list,name='group_list'),
	path('object_data/<destination>/<location_id>/group_list_all/',object_data_views.group_list_all,name='group_list_all'),
	path('object_data/<destination>/<location_id>/<object_lookup>/link_list/',object_data_views.link_list,name='link_list'),
	path('object_data/<destination>/<location_id>/note_list/',object_data_views.note_list,name='note_list'),
	path('object_data/<destination>/<location_id>/query_bug_client/',object_data_views.query_bug_client,name='query_bug_client'),
	path('object_data/<destination>/<location_id>/user_list/',object_data_views.user_list,name='user_list'),
	path('object_data/<destination>/<location_id>/user_list_all/',object_data_views.user_list_all,name='user_list_all'),

	# Organisation
	path('organisation_duplicates/',organisation_views.organisation_duplicates,name='organisation_duplicates'),
	path('organisation_information/<int:organisation_id>/',organisation_views.organisation_information,name='organisation_information'),
	path('organisation_information/<int:organisation_id>/save/',organisation_views.organisation_information_save,name='organisation_information_save'),
	path('organisation_information/<int:organisation_id>/update_profile/',organisation_views.organisation_update_profile,name='organisation_update_profile'),

	# Projects
	path('project_information/<int:project_id>/',project_views.project_information,name='project_information'),
	path('project_information/<int:project_id>/save/',project_views.project_information_save,name='project_information_save'),

	# Requirements
	path('requirement_information/<int:requirement_id>/',requirement_views.requirement_information,name='requirement_information'),
	path('requirement_information/<int:requirement_id>/add_link/',requirement_views.add_requirement_link,name='add_requirement_link'),
	path('requirement_information/<int:requirement_id>/data/item_links/',requirement_views.get_requirement_item_links,name='get_requirement_item_links'),
	path('requirement_information/<int:requirement_id>/data/items/',requirement_views.get_requirement_items,name='get_requirement_items'),
	path('requirement_information/<int:requirement_id>/data/item_status/',requirement_views.get_requirement_item_status_list,name='get_requirement_item_status_list'),
	path('requirement_information/<int:requirement_id>/data/item_type/',requirement_views.get_requirement_item_type_list,name='get_requirement_item_type_list'),
	path('requirement_information/<int:requirement_id>/data/links/',requirement_views.get_requirement_links_list,name='get_requirement_links_list'),
	path('requirement_information/<int:requirement_id>/save/',requirement_views.requirement_information_save,name='requirement_information_save'),

	# Requirement Items
	path('requirement_item_information/<int:requirement_item_id>/', requirement_item_views.requirement_item_information,name='requirement_item_information'),
	path('requirement_item_information/<int:requirement_item_id>/add_link/',requirement_item_views.add_requirement_item_link,name='add_requirement_item_link'),
	path('requirement_item_information/<int:requirement_item_id>/',requirement_item_views.requirement_item_information,name='requirement_item_information'),
	path('requirement_item_information/<int:requirement_item_id>/data/links/',requirement_item_views.get_requirement_item_links_list,name='get_requirement_item_links_list'),
	path('requirement_item_information/<int:requirement_item_id>/save/',requirement_item_views.requirement_information_save,name='requirement_information_save'),

	# Search Items
	path('search/',search_views.search,name='search'),
	path('search/data/',search_views.search_data,name='search_data'),
	path('search/customer/',search_views.search_customer,name='search_customer'),
	path('search/customer/data/',search_views.search_customer_data,name='search_customer_data'),
	path('search/organisation/',search_views.search_organisation,name='search_organisation'),
	path('search/organisation/data/',search_views.search_organisation_data,name='search_organisation_data'),

	# Tasks
	path('task_information/<int:task_id>/',task_views.task_information,name='task_information'),
	path('task_information/<int:task_id>/save/',task_views.task_information_save,name='task_information_save'),
]


"""
urlpatterns = [
	
re_path(r'^$', views.index, name='index'),
re_path(r'^add_campus_to_customer/(?P<customer_id>[0-9]+)/(?P<campus_id>[0-9]+)/', views.add_campus_to_customer,name='add_campus_to_customer'),
re_path(r'^admin_group/(?P<location_id>[0-9]+)/(?P<destination>["group","permission_set","user"])',views.admin_group,name="admin_group"),
re_path(r'^admin_permission_set/(?P<group_id>[0-9]+)/',views.admin_permission_set,name="admin_permission_set"),
re_path(r'^admin_add_user/(?P<group_id>[0-9]+)/', views.admin_add_user, name="admin_add_user"),
re_path(r'^alerts/',views.alerts,name='alerts'),
re_path(r'^assign_customer_project_task/(?P<customer_id>[0-9]+)/', views.assign_customer_project_task,name='assign_customer_project_task'),
re_path(r'^assigned_group_add/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity","request_for_change"]+)/$', views.assigned_group_add , name='assigned_group_add'),
re_path(r'^assigned_group_delete/(?P<object_assignment_id>[0-9]+)/', views.assigned_group_delete , name='assigned_group_delete'),
re_path(r'^assigned_group_list/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity","request_for_change"]+)/', views.assigned_group_list , name='assigned_group_list'),
re_path(r'^assigned_opportunity_connection_add/(?P<opportunity_id>[0-9]+)/(?P<destination>["organisation","customer"]+)/',views.assigned_opportunity_connection_add,name='assigned_opportunity_connection_add'),
re_path(r'^assigned_rfc_connection_delete/(?P<rfc_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer"]+)/',views.assigned_rfc_connection_delete,name='assigned_rfc_connection_delete'),
re_path(r'^assigned_rfc_connection_add/(?P<rfc_id>[0-9]+)/(?P<destination>["organisation","customer"]+)/',views.assigned_rfc_connection_add,name='assigned_rfc_connection_add'),
re_path(r'^assigned_opportunity_connection_delete/(?P<opportunity_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer"]+)/',views.assigned_opportunity_connection_delete,name='assigned_opportunity_connection_delete'),
re_path(r'^assigned_user_add/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity"]+)/$',views.assigned_user_add,name='assigned_user_add'),
re_path(r'^assigned_user_delete/(?P<object_assignment_id>[0-9]+)/', views.assigned_user_delete , name='assigned_user_delete'),
re_path(r'^assigned_user_list/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity"]+)/$',views.assigned_user_list,name='assigned_user_list'),
re_path(r'^associate/(?P<project_id>[0-9]+)/(?P<task_id>[0-9]+)/(?P<project_or_task>[P,T])', views.associate,name='associate'),
re_path(r'^associated_projects/(?P<task_id>[0-9]+)/', views.associated_projects, name='associated_projects'),
re_path(r'^associated_task/(?P<project_id>[0-9]+)/', views.associated_task, name='associated_task'),
re_path(r'^bug_add/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/(?P<bug_id>[0-9]+)/(?P<bug_client_id>[0-9]+)',views.bug_add,name='bug_add'),
re_path(r'^bug_client_delete/(?P<bug_client_id>[0-9]+)/$', views.bug_client_delete, name='bug_client_delete'),
re_path(r'^bug_client_information/(?P<bug_client_id>[0-9]+)/$', views.bug_client_information,name='bug_client_information'),
re_path(r'^bug_client_list/$',views.bug_client_list,name='bug_client_list'),
re_path(r'^bug_list/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/$', views.bug_list, name='bug_list'),
re_path(r'^bug_list/$', views.bug_list, name='bug_list'),
re_path(r'^bug_search/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/$', views.bug_search, name='bug_search'),
re_path(r'^campus_information/(?P<campus_information>[0-9]+)/', views.campus_information, name='campus_information'),
re_path(r'^campus_readonly/(?P<campus_information>[0-9]+)/', views.campus_readonly, name='campus_readonly'),
re_path(r'^change_group_leader/(?P<user_group_id>[0-9]+)/', views.change_group_leader, name='change_group_leader'),
re_path(r'^change_task_edit/(?P<change_task_id>[0-9]+)/', views.change_task_edit, name='change_task_edit'),
re_path(r'^change_task_finish/(?P<change_task_id>[0-9]+)/', views.change_task_finish, name='change_task_finish'),
re_path(r'^change_task_information/(?P<change_task_id>[0-9]+)/', views.change_task_information, name='change_task_information'),
re_path(r'^change_task_list/(?P<rfc_id>[0-9]+)/', views.change_task_list, name='change_task_list'),
re_path(r'^change_task_start/(?P<change_task_id>[0-9]+)/', views.change_task_start, name='change_task_start'),
re_path(r'^cost_information/(?P<location_id>[0-9]+)/(?P<destination>["project","task"]+)/$',views.cost_information,name='cost_information'),
re_path(r'^customer_information/(?P<customer_id>[0-9]+)/', views.customer_information, name='customer_information'),
re_path(r'^customer_campus_information/(?P<customer_campus_id>[0-9]+)/(?P<customer_or_org>["CUST","CAMP"]+)',views.customer_campus_information, name="customer_campus_information"),
re_path(r'^customer_readonly/(?P<customer_id>[0-9]+)/', views.customer_readonly, name='customer_readonly'),
re_path(r'^dashboard/$', views.dashboard,name='dashboard'),
re_path(r'^dashboard/active_bugs', views.dashboard_active_bugs,name='dashboard_active_bugs'),
re_path(r'^dashboard/active_projects', views.dashboard_active_projects,name='dashboard_active_projects'),
re_path(r'^dashboard/active_quotes', views.dashboard_active_quotes,name='dashboard_active_quotes'),
re_path(r'^dashboard/active_requirement', views.dashboard_active_requirement, name='dashboard_active_requirement'),
re_path(r'^dashboard/active_task', views.dashboard_active_task, name='dashboard_active_task'),
re_path(r'^dashboard/administration_task', views.dashboard_administration_task, name='dashboard_administration_task'),
re_path(r'^dashboard/group_active_projects', views.dashboard_group_active_projects,name='dashboard_group_active_projects'),
re_path(r'^dashboard/group_active_task', views.dashboard_group_active_task,name='dashboard_group_active_task'),
re_path(r'^dashboard/group_opportunities', views.dashboard_group_opportunities, name='dashboard_group_opportunities'),
re_path(r'^dashboard/group_request_for_change', views.dashboard_group_request_for_change, name='dashboard_group_request_for_change'),
re_path(r'^dashboard/opportunities', views.dashboard_opportunities, name='dashboard_opportunities'),
re_path(r'^dashboard/ready_for_approval', views.dashboard_ready_for_approval, name='ready_for_approval'),
re_path(r'^deactivate_campus/(?P<campus_id>[0-9]+)/$',views.deactivate_campus,name='deactivate_campus'),
re_path(r'^delete_campus_contact/(?P<customer_campus_id>[0-9]+)/(?P<cust_or_camp>["CUST","CAMP"]+)',views.delete_campus_contact, name='delete_campus_contact'),
re_path(r'^delete_cost/(?P<cost_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<project_or_task>[P,T])', views.delete_cost,name='delete_cost'),
re_path(r'^delete_customer/(?P<customer_id>[0-9]+)/',views.delete_customer,name='delete_customer'),
re_path(r'^delete_group/(?P<group_id>[0-9]+)/',views.delete_group,name='delete_group'),
re_path(r'^delete_document/(?P<document_key>[0-9A-Za-z_\-]+)/$', views_document_tree.delete_document, name='delete_document'),
re_path(r'^delete_folder/(?P<folder_id>[0-9]+)/$', views_document_tree.delete_folder, name='delete_folder'),
re_path(r'^delete_organisation/(?P<organisation_id>[0-9]+)/',views.delete_organisation,name='delete_organisation'),
re_path(r'^delete_permission_set/(?P<permission_set_id>[0-9]+)/',views.delete_permission_set,name='delete_permission_set'),
re_path(r'^delete_tag/(?P<tag_id>[0-9]+)/',views.delete_tag,name="delete_tag"),
re_path(r'^delete_tag_from_object/(?P<tag_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity"]+)/$', views.delete_tag_from_object, name='delete_tag_from_object'),
re_path(r'^delete_user_permission/(?P<user_id>[0-9]+)/(?P<permission_set_id>[0-9]+)/(?P<group_id>[0-9]+)/$', views.delete_user_permission, name='delete_user_permission'),
re_path(r'^diagnostic_information/$', views.diagnostic_information, name='diagnostic_information'),
re_path(r'^diagnostic_render_pdf/pdf_example/$', views.pdf_example, name='pdf_example'),
re_path(r'^diagnostic_render_pdf/$', views.diagnostic_render_pdf, name='diagnostic_render_pdf'),
re_path(r'^diagnostic_test_database/',views.diagnostic_test_database,name='diagnostic_test_database'),
re_path(r'^diagnostic_test_document_upload/',views.diagnostic_test_document_upload,name='diagnostic_test_document_upload'),
re_path(r'^diagnostic_test_email/',views.diagnostic_test_email,name='diagnostic_test_email'),
re_path(r'^diagnostic_test_location_services/',views.diagnostic_test_location_services,name='diagnostic_test_location_services'),
re_path(r'^diagnostic_test_recaptcha/',views.diagnostic_test_recaptcha,name='diagnostic_test_recaptcha'),
re_path(r'^document_tree_folder/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity","organisation","customer","request_for_change"]+)/(?P<folder_id>[0-9]+)/$', views_document_tree.document_tree_folder,name='document_tree_folder'),
re_path(r'^document_tree_list/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity","organisation","customer","request_for_change"]+)/(?P<folder_id>[0-9]+)/', views_document_tree.document_tree_list,name='document_tree_list'),
re_path(r'^document_tree_list/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity","organisation","customer","request_for_change"]+)/$', views_document_tree.document_tree_list,name='document_tree_list'),
re_path(r'^document_tree_upload/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity","organisation","customer","request_for_change"]+)/(?P<folder_id>[0-9]+)/$', views_document_tree.document_tree_upload,name="document_tree_upload"),
re_path(r'^document_tree_url/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity","organisation","customer","request_for_change"]+)/(?P<folder_id>[0-9]+)/$', views_document_tree.document_tree_url,name='document_tree_url'),
re_path(r'^email_history/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer","project","task","opportunity","quote"]+)/$', views.email_history,name='email_history'),
re_path(r'^email_information/(?P<email_content_id>[0-9]+)/$', views.email_information,name='email_information'),
re_path(r'^email/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer","project","task","opportunity","quote"]+)/$', views.email,name='email'),
re_path(r'^extract_quote/(?P<quote_uuid>[0-9A-Za-z_\-]+)/(?P<quote_template_id>[0-9]+)/', views.extract_quote,name='extract_quote'),
re_path(r'^extract_requirement/(?P<requirement_id>[0-9]+)/', views.extract_requirement,name='extract_requirement'),
re_path(r'^group_information/(?P<group_id>[0-9]+)/$',views.group_information,name='group_information'),
re_path(r'^information_customer_contact_history/(?P<customer_id>[0-9]+)/$',views_customer_information.information_customer_contact_history,name='information_customer_contact_history'),
re_path(r'^information_organisation_contact_history/(?P<organisation_id>[0-9]+)/$',views_organisation_information.information_organisation_contact_history,name='information_organisation_contact_history'),
re_path(r'^information_project_customer/(?P<project_id>[0-9]+)/$', views_project_information.information_project_customer, name='information_project_customer'),
re_path(r'^information_project_history/(?P<project_id>[0-9]+)/$', views_project_information.information_project_history, name='information_project_history'),
re_path(r'^information_task_customer/(?P<task_id>[0-9]+)/$', views_task_information.information_task_customer,name='information_task_customer'),
re_path(r'^information_task_history/(?P<task_id>[0-9]+)/$', views_task_information.information_task_history,name='information_task_history'),
re_path(r'^kanban_board_close/(?P<kanban_board_id>[0-9]+)/$', views.kanban_board_close,name='kanban_board_close'),
re_path(r'^kanban_edit_card/(?P<kanban_card_id>[0-9]+)/$', views.kanban_edit_card,name='kanban_edit_card'),
re_path(r'^kanban_edit_xy_name/(?P<location_id>[0-9]+)/(?P<destination>["column","level"]+)/$', views.kanban_edit_xy_name,name='kanban_edit_xy_name'),
re_path(r'^kanban_information/(?P<kanban_board_id>[0-9]+)/', views.kanban_information, name='kanban_information'),
re_path(r'^kanban_move_card/(?P<kanban_card_id>[0-9]+)/(?P<kanban_column_id>[0-9]+)/(?P<kanban_level_id>[0-9]+)/', views.kanban_move_card, name='kanban_move_card'),
re_path(r'^kanban_new_card/(?P<kanban_board_id>[0-9]+)/$', views.kanban_new_card,name='kanban_new_card'),
re_path(r'^kanban_new_link/(?P<kanban_board_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/$', views.kanban_new_link,name='kanban_new_link'),
re_path(r'^kanban_new_link/(?P<kanban_board_id>[0-9]+)/$', views.kanban_new_link,name='kanban_new_link'),
re_path(r'^kanban_properties/(?P<kanban_board_id>[0-9]+)/$', views.kanban_properties,name='kanban_properties'),
re_path(r'^kanban_read_only/(?P<kanban_board_id>[0-9]+)/', views.kanban_read_only, name='kanban_read_only'),
re_path(r'^kanban_requirement_information/(?P<kanban_board_id>[0-9]+)/$',views.kanban_requirement_information,name='kanban_requirement_information'),
re_path(r'^kanban_requirement_item_update/(?P<requirement_item_id>[0-9]+)/(?P<status_id>[0-9]+)/$',views.kanban_requirement_item_update,name="kanban_requirement_item_update"),
re_path(r'^kudos_rating/(?P<kudos_key>[0-9A-Za-z_\-]+)/$', views.kudos_rating, name='kudos_rating'),
re_path(r'^kudos_read_only/(?P<kudos_key>[0-9A-Za-z_\-]+)/$', views.kudos_read_only, name='kudos_read_only'),
re_path(r'^list_of_tags/',views.list_of_tags,name='list_of_tags'),
re_path(r'^list_of_taxes_deactivate/(?P<tax_id>[0-9]+)/', views_administration.list_of_taxes_deactivate, name='list_of_taxes_deactivate'),
re_path(r'^list_of_taxes_edit/(?P<tax_id>[0-9]+)/', views_administration.list_of_taxes_edit, name='list_of_taxes_edit'),
re_path(r'^list_of_taxes_information/', views_administration.list_of_taxes_information, name='list_of_taxes_information'),
re_path(r'^list_of_taxes_list/', views_administration.list_of_taxes_list, name='list_of_taxes_list'),
re_path(r'^list_of_taxes_new/', views_administration.list_of_taxes_new, name='list_of_taxes_new'),
re_path(r'^login', views.login, name='login'),
re_path(r'^logout', views.logout, name='logout'),
re_path(r'^lookup_product/(?P<product_id>[0-9]+)/$', views_lookup.lookup_product, name='lookup_product'),
re_path(r'^merge_tags/(?P<old_tag_id>[0-9]+)/$',views.merge_tags,name='merge_tags'),
re_path(r'^merge_tags/(?P<old_tag_id>[0-9]+)/(?P<new_tag_id>[0-9]+)/',views.merge_tags,name='merge_tags'),
re_path(r'^my_profile', views.my_profile,name='my_profile'),
re_path(r'^new_bug_client/$',views.new_bug_client, name='new_bug_client'),
re_path(r'^new_campus/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer"]+)/$', views.new_campus, name='new_campus'),
re_path(r'^new_change_task/(?P<rfc_id>[0-9]+)/', views.new_change_task, name='new_change_task'),
re_path(r'^new_customer/(?P<organisation_id>[0-9]+)/', views.new_customer, name='new_customer'),
re_path(r'^new_group/',views.new_group,name="new_group"),
re_path(r'^new_kanban_board/$', views.new_kanban_board,name='new_kanban_board'),
re_path(r'^new_kanban_requirement_board/(?P<requirement_id>[0-9]+)/',views.new_kanban_requirement_board,name='new_kanban_requirement_board'),
re_path(r'^new_kudos/(?P<project_id>[0-9]+)/',views.new_kudos,name='new_kudos'),
re_path(r'^new_opportunity/$', views.new_opportunity, name='new_opportunity'),
re_path(r'^new_opportunity_link/(?P<opportunity_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/(?P<location_id>[0-9]+)/', views.new_opportunity_link, name='new_opportunity_link'),
re_path(r'^new_opportunity_link/(?P<opportunity_id>[0-9]+)/(?P<destination>["project","task","requirement"]+)/$', views.new_opportunity_link, name='new_opportunity_link'),
re_path(r'^new_organisation', views.new_organisation, name='new_organisation'),
re_path(r'^new_permission_set/', views.new_permission_set, name='new_permission_set'),
re_path(r'^new_project/(?P<location_id>[0-9]+)/(?P<destination>["customer","organisation","opportunity","requirement","requirement_item"]+)/$',views.new_project,name='new_project'),
re_path(r'^new_project/$', views.new_project, name='new_project'),
re_path(r'^new_quote_template/',views.new_quote_template,name='new_quote_template'),
re_path(r'^new_quote/(?P<primary_key>[0-9]+)/(?P<destination>["project","task","opportunity","customer","organisation"]+)/',views.new_quote, name='new_quote'),
re_path(r'^new_quote_link/(?P<quote_id>[0-9]+)/(?P<destination>["customer","organisation"]+)/(?P<location_id>[0-9]+)',views.new_quote_link, name='new_quote_link'),
re_path(r'^new_quote_link/(?P<quote_id>[0-9]+)/(?P<destination>["customer","organisation"]+)/',views.new_quote_link, name='new_quote_link'),
re_path(r'^new_request_for_change/', views.new_request_for_change,name="new_request_for_change"),
re_path(r'^new_requirement/(?P<location_id>[0-9]+)/(?P<destination>["opportunity"]+)/', views_requirements.new_requirement,name="new_requirement"),
re_path(r'^new_requirement/', views_requirements.new_requirement,name="new_requirement"),
re_path(r'^new_requirement_item/(?P<requirement_id>[0-9]+)/', views_requirements.new_requirement_item, name="new_requirement_item"),
re_path(r'^new_requirement_item_link/(?P<requirement_item_id>[0-9]+)/$',views_requirements.new_requirement_item_link,name='new_requirement_item_link'),
re_path(r'^new_requirement_item_link/(?P<requirement_item_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task"]+)/$',views_requirements.new_requirement_item_link,name='new_requirement_item_link'),
re_path(r'^new_requirement_link/(?P<requirement_id>[0-9]+)/$',views_requirements.new_requirement_link,name='new_requirement_link'),
re_path(r'^new_requirement_link/(?P<requirement_id>[0-9]+)/(?P<location_id>[0-9]+)/(?P<destination>["project","task","opportunity"]+)/$',views_requirements.new_requirement_link,name='new_requirement_link'),
re_path(r'^new_task/(?P<location_id>[0-9]+)/(?P<destination>["organisation","customer","opportunity","project","requirement","requirement_item"]+)/$', views.new_task, name='new_task'),
re_path(r'^new_task/$', views.new_task, name='new_task'),
re_path(r'^new_user/$', views_administration.new_user, name='new_user'),
re_path(r'^new_whiteboard/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","requirement_item","opportunity"]+)/(?P<folder_id>[0-9]+)/', views.new_whiteboard, name='new_whiteboard'),
re_path(r'^opportunity_connection_list/(?P<opportunity_id>[0-9]+)/', views.opportunity_connection_list,name='opportunity_connection_list'),
re_path(r'^opportunity_information/(?P<opportunity_id>[0-9]+)/', views.opportunity_information,name='opportunity_information'),
re_path(r'^opportunity_readonly/(?P<opportunity_id>[0-9]+)/', views.opportunity_readonly,name='opportunity_readonly'),
re_path(r'^organisation_information/(?P<organisation_id>[0-9]+)/', views.organisation_information,name='organisation_information'),
re_path(r'^organisation_readonly/(?P<organisation_id>[0-9]+)/', views.organisation_readonly,name='organisation_readonly'),
re_path(r'^permission_denied', views.permission_denied, name='permission_denied'),
re_path(r'^permission_set_information/(?P<permission_set_id>[0-9]+)/$',views.permission_set_information,name='permission_set_information'),
re_path(r'^permission_set_remove/(?P<permission_set_id>[0-9]+)/(?P<group_id>[0-9]+)',views.permission_set_remove,name='permission_set_remove'),
re_path(r'^preview_quote/(?P<quote_uuid>[0-9A-Za-z_\-]+)/(?P<quote_template_id>[0-9]+)/',views.preview_quote,name='preview_quote'),
re_path(r'^preview_requirement/(?P<requirement_id>[0-9]+)/',views.preview_requirement,name='preview_requirement'),
re_path(r'^private/(?P<document_key>[0-9A-Za-z_\-]+)/$', views.private_document, name='private'),
re_path(r'^product_and_service_discontinued/(?P<product_id>[0-9]+)/', views_administration.product_and_service_discontinued, name='product_and_service_discontinued'),
re_path(r'^product_and_service_edit/(?P<product_id>[0-9]+)/', views_administration.product_and_service_edit, name='product_and_service_edit'),
re_path(r'^product_and_service_new/', views_administration.product_and_service_new, name='product_and_service_new'),
re_path(r'^product_and_service_search/', views_administration.product_and_service_search, name='product_and_service_search'),
re_path(r'^project_information/(?P<project_id>[0-9]+)/', views.project_information, name='project_information'),
re_path(r'^project_readonly/(?P<project_id>[0-9]+)/', views.project_readonly, name='project_readonly'),
re_path(r'^project_remove_customer/(?P<project_customer_id>[0-9]+)/',views.project_remove_customer,name='project_remove_customer'),
re_path(r'^quote_delete_line_item/(?P<line_item_id>[0-9]+)/$', views_quotes.delete_line_item, name='quote_delete_line_item'),
re_path(r'^quote_delete_responsible_customer/(?P<quote_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views_quotes.delete_responsible_customer, name='quote_delete_responsible_customer'),
re_path(r'^quote_information/(?P<quote_id>[0-9]+)/$', views.quote_information, name='quote_information'),
re_path(r'^quote_list_of_line_items/(?P<quote_id>[0-9]+)/$', views_quotes.list_of_line_items, name='quote_list_of_line_items'),
re_path(r'^quote_new_line_item/(?P<quote_id>[0-9]+)/$', views_quotes.new_line_item, name='quote_new_line_item'),
re_path(r'^quote_readonly/(?P<quote_id>[0-9]+)/$', views.quote_readonly, name='quote_readonly'),
re_path(r'^quote_responsible_customer/(?P<quote_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views_quotes.responsible_customer, name='quote_responsible_customer'),
re_path(r'^quote_responsible_customer/(?P<quote_id>[0-9]+)/$', views_quotes.responsible_customer, name='quote_responsible_customer'),
re_path(r'^quote_template_information/(?P<quote_template_id>[0-9]+)/',views.quote_template_information,name='quote_template_information'),
re_path(r'^rename_document/(?P<document_key>[0-9A-Za-z_\-]+)/$', views.rename_document, name='rename_document'),
re_path(r'^request_for_change_approve/(?P<rfc_id>[0-9]+)/', views.request_for_change_approve, name='request_for_change_approve'),
re_path(r'^request_for_change_draft/(?P<rfc_id>[0-9]+)/', views.request_for_change_draft, name='request_for_change_draft'),
re_path(r'^request_for_change_finish/(?P<rfc_id>[0-9]+)/', views.request_for_change_finish, name='request_for_change_finish'),
re_path(r'^request_for_change_information/(?P<rfc_id>[0-9]+)/', views.request_for_change_information, name='request_for_change_information'),
re_path(r'^request_for_change_reject/(?P<rfc_id>[0-9]+)/', views.request_for_change_reject, name='request_for_change_reject'),
re_path(r'^request_for_change_set_to_draft/(?P<rfc_id>[0-9]+)/', views.request_for_change_set_to_draft, name='request_for_change_set_to_draft'),
re_path(r'^request_for_change_start/(?P<rfc_id>[0-9]+)/', views.request_for_change_start, name='request_for_change_start'),
re_path(r'^request_for_change_submit/(?P<rfc_id>[0-9]+)/', views.request_for_change_submit, name='request_for_change_submit'),
re_path(r'^request_for_change_information/(?P<rfc_id>[0-9]+)/', views.request_for_change_information, name='request_for_change_information'),
re_path(r'^requirement_customer_information/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_customer_information, name='requirement_customer_information'),
re_path(r'^requirement_documents_uploads/(?P<location_id>[0-9]+)/(?P<destination>["requirement","requirement_item"]+)', views_requirements.requirement_documents_uploads, name='requirement_documents_uploads'),
re_path(r'^requirement_information/(?P<requirement_id>[0-9]+)/', views_requirements.requirement_information,name="requirement_information"),
re_path(r'^requirement_item_information/(?P<requirement_item_id>[0-9]+)/', views_requirements.requirement_item_information, name="requirement_item_information"),
re_path(r'^requirement_item_link_remove/(?P<requirement_item_link_id>[0-9]+)/', views_requirements.requirement_item_link_remove, name="requirement_item_link_remove"),
re_path(r'^requirement_readonly/(?P<requirement_id>[0-9]+)/$', views_requirements.requirement_readonly,name="requirement_readonly"),
re_path(r'^requirement_link_list/(?P<requirement_id>[0-9]+)/$', views_requirements.requirement_link_list,name="requirement_link_list"),
re_path(r'^requirement_link_remove/(?P<requirement_link_id>[0-9]+)/$', views_requirements.requirement_link_remove,name="requirement_link_remove"),
re_path(r'^requirement_remove_customer/(?P<requirement_id>[0-9]+)/(?P<customer_id>[0-9]+)/$', views_requirements.requirement_remove_customer,name="requirement_remove_customer"),
re_path(r'^resolve_project/(?P<project_id>[0-9]+)/', views.resolve_project,    name='resolve_project'),
re_path(r'^resolve_task/(?P<task_id>[0-9]+)/', views.resolve_task, name='resolve_task'),
re_path(r'^search_customer', views.search_customer, name='search_customer'),
re_path(r'^search_group', views.search_group, name='search_group'),
re_path(r'^search_kanban', views.search_kanban,name='search_kanban'),
re_path(r'^search_organisation', views.search_organisation, name='search_organisation'),
re_path(r'^search_permission_set', views.search_permission_set, name='search_permission_set'),
re_path(r'^search_projects_task', views.search_projects_task, name='search_projects_task'),
re_path(r'^search_tags/',views.search_tags,name='search_tags'),
re_path(r'^search_templates/',views.search_templates,name='search_templates'),
re_path(r'^search_users', views_administration.search_users, name='search_users'),
re_path(r'^search/', views.search, name='search'),
re_path(r'^tag_information/(?P<location_id>[0-9]+)/(?P<destination>["project","task","requirement","quote","kanban_board","opportunity","organisation","customer"]+)/$',views.tag_information,name='tag_information'),
re_path(r'^task_information/(?P<task_id>[0-9]+)', views.task_information, name='task_information'),
re_path(r'^task_readonly/(?P<task_id>[0-9]+)', views.task_readonly, name='task_readonly'),
re_path(r'^task_remove_customer/(?P<task_customer_id>[0-9]+)/',views.task_remove_customer,name='task_remove_customer'),
re_path(r'^timeline_data/$', views.timeline_data, name='timeline_data'),
re_path(r'^timeline/$', views.timeline, name='timeline'),
re_path(r'^timesheet/(?P<location_id>[0-9]+)/(?P<destination>["requirement_item","project","task"]+)', views.timesheet_information,name="timesheet_information"),
re_path(r'^to_do_complete/(?P<to_do_id>[0-9]+)/$', views.to_do_complete, name='to_do_complete'),
re_path(r'^to_do/(?P<location_id>[0-9]+)/(?P<destination>["project","task","opportunity"]+)/$', views.to_do_list, name='to_do'),
re_path(r'^user_information/(?P<user_id>[0-9]+)/$', views_administration.user_information, name='user_information'),
re_path(r'^user_permissions', views_lookup.lookup_user_permissions, name='user_permissions'),
re_path(r'^user_want_remove/(?P<user_want_id>[0-9]+)', views.user_want_remove,name="user_want_remove"),
re_path(r'^user_want_view', views.user_want_view,name='user_want_view'),
re_path(r'^user_weblink_remove/(?P<user_weblink_id>[0-9]+)',views.user_weblink_remove,name='user_weblink_remove'),
re_path(r'^user_weblink_view',views.user_weblink_view,name='user_weblink_view'),
re_path(r'^whiteboard_information/common_xml',views_whiteboard.whiteboard_common_xml,name='whiteboard_common_xml'),
re_path(r'^whiteboard_information/graph_xml',views_whiteboard.whiteboard_graph_xml,name='whiteboard_graph_xml'),
re_path(r'^whiteboard_information/editor_xml',views_whiteboard.whiteboard_editor_xml,name='whiteboard_editor_xml'),
re_path(r'^whiteboard_information/toolbar_xml',views_whiteboard.whiteboard_toolbar_xml,name='whiteboard_toolbar_xml'),
re_path(r'^whiteboard_information/(?P<whiteboard_id>[0-9]+)',views_whiteboard.whiteboard_information,name='whiteboard_information'),
re_path(r'^whiteboard_information/$',views_whiteboard.whiteboard_information,name='whiteboard_information'),
re_path(r'^whiteboard_save/(?P<whiteboard_id>[0-9]+)',views_whiteboard.whiteboard_save,name='whiteboard_save'),


	path('change-password/', auth_views.PasswordChangeView.as_view()),
	path(
		'password_reset/',
		auth_views.PasswordResetView.as_view(
			template_name='NearBeach/password_reset.html',
		),
		name='password_reset',
	),
	path(
		'password_reset/done/',
		auth_views.PasswordResetDoneView.as_view(
			template_name='NearBeach/password_reset_done.html',
		),
		name='password_reset_done',
	),
	path(
		'reset/<uidb64>/<token>/',
		auth_views.PasswordResetConfirmView.as_view(
			template_name='NearBeach/reset.html',
		),
		name='password_reset_confirm',
	),
	path(
		'reset/done',
		auth_views.PasswordResetCompleteView.as_view(
			template_name='NearBeach/reset_done.html',
		),
		name='password_reset_complete'
	),



]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""

