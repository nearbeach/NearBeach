# Password reset
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import admin_views, \
    authentication_views, \
    change_task_views, \
    customer_views, \
    dashboard_views, \
    document_views, \
    error_views, \
    group_views, \
    kanban_views, \
    object_data_views, \
    organisation_views, \
    permission_set_views, \
    project_views, \
    request_for_change_views, \
    requirement_item_views, \
    requirement_views, \
    search_views, \
    task_views, \
    user_views

# The following two imports are for the static files
# 404 and 500 pages

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),

    # Administration
    path('admin/add_user/', admin_views.add_user, name='admin_add_user'),

    # Change Task
    path('change_task_update_status/<int:change_task_id>/', change_task_views.update_status,
         name='change_task_update_status'),

    # Customer
    path('customer_information/<int:customer_id>/', customer_views.customer_information, name='customer_information'),
    path('customer_information/<int:customer_id>/save/', customer_views.customer_information_save,
         name='customer_information_save'),

    # Dashboard
    path('dashboard/get/bug_list/', dashboard_views.get_bug_list, name='get_bug_list'),
    path('dashboard/get/my_objects/', dashboard_views.get_my_objects, name='get_my_objects'),
    path('dashboard/get/rfc_approvals/', dashboard_views.rfc_approvals, name='rfc_approvals'),

    # Documentation
    path('documentation/<destination>/<location_id>/add_folder/', document_views.document_add_folder,
         name='document_add_folder'),
    path('documentation/<destination>/<location_id>/add_link/', document_views.document_add_link,
         name='document_add_link'),
    path('documentation/<destination>/<location_id>/list/files/', document_views.document_list_files,
         name='document_list_files'),
    path('documentation/<destination>/<location_id>/list/folders/', document_views.document_list_folders,
         name='document_list_folders'),
    path('documentation/<destination>/<location_id>/upload/', document_views.document_upload, name='document_upload'),
    path('documentation/get/max_upload/', document_views.get_max_upload, name='document_get_max_upload'),

    # Groups
    path('group_information/<int:group_id>/', group_views.group_information, name='group_information'),
    path('group_information/<int:group_id>/save/', group_views.group_information_save, name='group_information_save'),
    path('group_information/check_group_name/', group_views.check_group_name, name='check_group_name'),

    # Kanban
    path('kanban_information/<int:kanban_board_id>/', kanban_views.kanban_information, name='kanban_information'),
    path('kanban_information/<int:kanban_board_id>/<object_lookup>/add_link/', kanban_views.add_kanban_link,
         name='add_kanban_link'),
    path('kanban_information/<int:kanban_board_id>/<object_lookup>/link_list/', kanban_views.kanban_link_list,
         name='kanban_link_list'),
    path('kanban_information/<int:kanban_board_id>/new_card/', kanban_views.new_kanban_card, name='new_kanban_card'),
    path('kanban_information/<int:kanban_card_id>/move_card/', kanban_views.move_kanban_card, name='move_kanban_card'),
    path('kanban_information/check_kanban_board_name/', kanban_views.check_kanban_board_name,
         name='check_kanban_board_name'),
    path('kanban_information/update_card/', kanban_views.update_card, name='kanban_update_card'),

    # Authentication
    path('login', authentication_views.login, name='login'),
    path('logout', authentication_views.logout, name='logout'),

    # Permission Sets
    path('permission_set_information/<int:permission_set_id>/', permission_set_views.permission_set_information,
         name='permission_set_information'
    ),
    path('permission_set_information/<int:permission_set_id>/save/',
         permission_set_views.permission_set_information_save,
         name='permission_set_information_save'
    ),

    # Private files
    path('private/<uuid:document_key>/', document_views.private_download_file, name='private_download_file'),

    # New Objects
    path('new_customer/', customer_views.new_customer, name='new_customer'),
    path('new_customer/save/', customer_views.new_customer_save, name='new_customer_save'),
    path('new_group/', group_views.new_group, name='new_group'),
    path('new_group/save/', group_views.new_group_save, name='new_group_save'),
    path('new_kanban/', kanban_views.new_kanban, name='new_kanban'),
    path('new_kanban_save/', kanban_views.new_kanban_save, name='new_kanban_save'),
    path('new_organisation/', organisation_views.new_organisation, name='new_organisation'),
    path('new_organisation/save/', organisation_views.new_organisation_save, name='new_organisation_save'),
    path('new_permission_set/', permission_set_views.new_permission_set, name='new_permission_set'),
    path('new_permission_set/save/', permission_set_views.new_permission_set_save, name='new_permission_set_save'),
    path('new_project/', project_views.new_project, name='new_project'),
    path('new_project/save/', project_views.new_project_save, name='new_project_save'),
    path('new_request_for_change/', request_for_change_views.new_request_for_change, name='new_request_for_change'),
    path('new_request_for_change/save/', request_for_change_views.new_request_for_change_save,
         name='new_request_for_change_save'),
    path('new_requirement/', requirement_views.new_requirement, name='new_requirement'),
    path('new_requirement/save/', requirement_views.new_requirement_save, name='new_requirement_save'),
    path('new_requirement_item/save/<int:requirement_id>/', requirement_item_views.new_requirement_item,
         name='new_requirement_item'),
    path('new_task/', task_views.new_task, name='new_task'),
    path('new_task/save/', task_views.new_task_save, name='new_task_save'),
    path('new_user/', user_views.new_user, name='new_user'),
    path('new_user/save/', user_views.new_user_save, name='new_user_save'),

    # Object Data
    path('object_data/admin_add_user/', object_data_views.admin_add_user, name='admin_add_user'),
    path('object_data/<destination>/<location_id>/add_bug/', object_data_views.add_bug, name='add_bug'),
    path('object_data/<destination>/<location_id>/add_customer/', object_data_views.add_customer, name='add_customer'),
    path('object_data/<destination>/<location_id>/add_group/', object_data_views.add_group, name='add_group'),
    path('object_data/<destination>/<location_id>/add_link/', object_data_views.add_link, name='add_link'),
    path('object_data/<destination>/<location_id>/add_notes/', object_data_views.add_notes, name='add_notes'),
    path('object_data/<destination>/<location_id>/add_user/', object_data_views.add_user, name='add_user'),
    path('object_data/<destination>/<location_id>/associated_objects/', object_data_views.associated_objects,
         name='associated_objects'),
    path('object_data/bug_client_list/', object_data_views.bug_client_list, name='bug_client_list'),
    path('object_data/<destination>/<location_id>/bug_list/', object_data_views.bug_list, name='bug_list'),
    path('object_data/<destination>/<location_id>/customer_list/', object_data_views.customer_list,
         name='customer_list'),
    path('object_data/<destination>/<location_id>/customer_list_all/', object_data_views.customer_list_all,
         name='customer_list_all'),
    path('object_data/<destination>/<location_id>/group_list/', object_data_views.group_list, name='group_list'),
    path('object_data/<destination>/<location_id>/group_list_all/', object_data_views.group_list_all,
         name='group_list_all'),
    path('object_data/<destination>/<location_id>/<object_lookup>/link_list/', object_data_views.link_list,
         name='link_list'),
    path('object_data/<destination>/<location_id>/note_list/', object_data_views.note_list, name='note_list'),
    path('object_data/<destination>/<location_id>/object_link_list/', object_data_views.object_link_list,
         name='object_link_list'),  # WTF - Please check to make sure we need this function?
    path('object_data/<destination>/<location_id>/query_bug_client/', object_data_views.query_bug_client,
         name='query_bug_client'),
    path('object_data/<destination>/<location_id>/user_list/', object_data_views.user_list, name='user_list'),
    path('object_data/<destination>/<location_id>/user_list_all/', object_data_views.user_list_all,
         name='user_list_all'),
    path('object_data/lead_user_list/', object_data_views.lead_user_list, name='lead_user_list'),

    # Organisation
    path('organisation_duplicates/', organisation_views.organisation_duplicates, name='organisation_duplicates'),
    path('organisation_information/<int:organisation_id>/', organisation_views.organisation_information,
         name='organisation_information'),
    path('organisation_information/<int:organisation_id>/save/', organisation_views.organisation_information_save,
         name='organisation_information_save'),
    path('organisation_information/<int:organisation_id>/update_profile/',
         organisation_views.organisation_update_profile, name='organisation_update_profile'),

    # Projects
    path('project_information/<int:project_id>/', project_views.project_information, name='project_information'),
    path('project_information/<int:project_id>/save/', project_views.project_information_save,
         name='project_information_save'),

    # Requirements
    path('requirement_information/<int:requirement_id>/', requirement_views.requirement_information,
         name='requirement_information'),
    path('requirement_information/<int:requirement_id>/add_link/', requirement_views.add_requirement_link,
         name='add_requirement_link'),
    path('requirement_information/<int:requirement_id>/data/item_links/', requirement_views.get_requirement_item_links,
         name='get_requirement_item_links'),
    path('requirement_information/<int:requirement_id>/data/items/', requirement_views.get_requirement_items,
         name='get_requirement_items'),
    path('requirement_information/<int:requirement_id>/data/item_status/',
         requirement_views.get_requirement_item_status_list, name='get_requirement_item_status_list'),
    path('requirement_information/<int:requirement_id>/data/item_type/',
         requirement_views.get_requirement_item_type_list, name='get_requirement_item_type_list'),
    path('requirement_information/<int:requirement_id>/data/links/', requirement_views.get_requirement_links_list,
         name='get_requirement_links_list'),
    path('requirement_information/<int:requirement_id>/save/', requirement_views.requirement_information_save,
         name='requirement_information_save'),

    # Requirement Items
    path('requirement_item_information/<int:requirement_item_id>/', requirement_item_views.requirement_item_information,
         name='requirement_item_information'),
    path('requirement_item_information/<int:requirement_item_id>/add_link/',
         requirement_item_views.add_requirement_item_link, name='add_requirement_item_link'),
    path('requirement_item_information/<int:requirement_item_id>/', requirement_item_views.requirement_item_information,
         name='requirement_item_information'),
    path('requirement_item_information/<int:requirement_item_id>/data/links/',
         requirement_item_views.get_requirement_item_links_list, name='get_requirement_item_links_list'),
    path('requirement_item_information/<int:requirement_item_id>/save/',
         requirement_item_views.requirement_information_save, name='requirement_information_save'),

    # Request for Change
    path('rfc_deployment/<int:rfc_id>/', request_for_change_views.rfc_deployment, name='rfc_deployment'),
    path('rfc_information/<int:rfc_id>/', request_for_change_views.rfc_information, name='rfc_information'),
    path('rfc_information/<int:rfc_id>/change_task_list/', request_for_change_views.rfc_change_task_list,
         name='rfc_change_task_list'),
    path('rfc_information/<int:rfc_id>/new_change_task/', request_for_change_views.rfc_new_change_task,
         name='rfc_new_change_task'),
    path('rfc_information/<int:rfc_id>/save/', request_for_change_views.rfc_information_save,
         name='rfc_information_save'),
    path('rfc_information/<int:rfc_id>/save/backout/', request_for_change_views.rfc_save_backout,
         name='rfc_save_backout'),
    path('rfc_information/<int:rfc_id>/save/implementation/', request_for_change_views.rfc_save_implementation,
         name='rfc_save_implementation'),
    path('rfc_information/<int:rfc_id>/save/risk/', request_for_change_views.rfc_save_risk, name='rfc_save_risk'),
    path('rfc_information/<int:rfc_id>/save/test/', request_for_change_views.rfc_save_test, name='rfc_save_test'),
    path('rfc_information/<int:rfc_id>/update_status/', request_for_change_views.rfc_update_status,
         name='rfc_update_status'),
    path('rfc_readonly/<int:rfc_id>/', request_for_change_views.rfc_readonly, name='rfc_readonly'),

    # Search Items
    path('search/', search_views.search, name='search'),
    path('search/data/', search_views.search_data, name='search_data'),
    path('search/group/', search_views.search_group, name='search_group'),
    path('search/group/data/', search_views.search_group_data, name='search_group_data'),
    path('search/customer/', search_views.search_customer, name='search_customer'),
    path('search/customer/data/', search_views.search_customer_data, name='search_customer_data'),
    path('search/organisation/', search_views.search_organisation, name='search_organisation'),
    path('search/organisation/data/', search_views.search_organisation_data, name='search_organisation_data'),
    path('search/permission_set/', search_views.search_permission_set, name='search_permission_set'),
    path('search/permission_set/data/', search_views.search_permission_set_data, name='search_permission_set_data'),
    path('search/user/', search_views.search_user, name='search_user'),
    path('search/user/data/', search_views.search_user_data, name='search_user_data'),

    # Tasks
    path('task_information/<int:task_id>/', task_views.task_information, name='task_information'),
    path('task_information/<int:task_id>/save/', task_views.task_information_save, name='task_information_save'),

    # Users
    path('user_information/<int:username>/', user_views.user_information, name='user_information'),
    path('user_information/<int:username>/save/', user_views.user_information_save, name='user_information_save'),

    # Changing and Resetting Passwords
    # path('change-password/', auth_views.PasswordChangeView.as_view()),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='NearBeach/authentication/password_reset.html',
            email_template_name='NearBeach/authentication/password_reset_email.html',
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='NearBeach/authentication/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='NearBeach/authentication/reset.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='NearBeach/authentication/reset_done.html',
        ),
        name='password_reset_complete'
    ),
]

handler403 = error_views.error_403
handler404 = error_views.error_404
handler500 = error_views.error_500

"""
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


"""
