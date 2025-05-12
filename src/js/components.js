import {defineAsyncComponent} from "vue/dist/vue.esm-bundler";

export const
    CarbonArrowUp = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-arrow-up" */
            "./components/icons/CarbonArrowUp.vue"
            )
    ),
    CarbonCloseOutline = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-close-outline" */
            "./components/icons/CarbonCloseOutline.vue"
            )
    ),
    CarbonDocument = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-document" */
            "./components/icons/CarbonDocument.vue"
            )
    ),
    CarbonDocumentPdf = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-document-pdf" */
            "./components/icons/CarbonDocumentPdf.vue"
            )
    ),
    CarbonEmail = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-email" */
            "./components/icons/CarbonEmail.vue"
            )
    ),
    CarbonFolder = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-folder" */
            "./components/icons/CarbonFolder.vue"
            )
    ),
    CarbonImage = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-image" */
            "./components/icons/CarbonImage.vue"
            )
    ),
    CarbonInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-information" */
            "./components/icons/CarbonInformation.vue"
            )
    ),
    CarbonLink = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-link" */
            "./components/icons/CarbonLink.vue"
            )
    ),
    CarbonTrashCan = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "carbon-trash-can" */
            "./components/icons/CarbonTrashCan.vue"
            )
    ),
    ChangeTaskInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "change-task-information" */
            "./components/change_task/ChangeTaskInformation.vue"
            )
    ),
    ChangeTaskModules = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "change-task-modules" */
            "./components/change_task/ChangeTaskModules.vue"
            )
    ),
    ConfirmKanbanBoardClosure = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "confirm-kanban-board-closure" */
            "./components/kanban/ConfirmKanbanBoardClosure.vue"
            )
    ),
    ConfirmKanbanBoardReopen = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "confirm-kanban-board-reopen" */
            "./components/kanban/ConfirmKanbanBoardReopen.vue"
            )
    ),
    CustomerInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "customer-information" */
            "./components/customers/CustomerInformation.vue"
            )
    ),
    CustomerModules = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "customer-modules" */
            "./components/customers/CustomerModules.vue"
            )
    ),
    DashboardKanbanList = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-kanban-list" */
            "./components/dashboard/DashboardKanbanList.vue"
            )
    ),
    DashboardMyObjects = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-my-objects" */
            "./components/dashboard/DashboardMyObjects.vue"
            )
    ),
    DashboardRfcApprovals = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-rfc-approvals" */
            "./components/dashboard/DashboardRfcApprovals.vue"
            )
    ),
    DashboardTodoToday = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-todo-today" */
            "./components/dashboard/DashboardTodoToday.vue"
            )
    ),
    DashboardUnassignedObjects = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-unassigned-objects" */
            "./components/dashboard/DashboardUnassignedObjects.vue"
            )
    ),
    DashboardUsersWithNoGroups = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-users-with-no-groups" */
            "./components/dashboard/DashboardUsersWithNoGroups.vue"
            )
    ),
    DiagnosticInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "diagnostic-information" */
            "./components/diagnostic/DiagnosticInformation.vue"
            )
    ),
    EditSprint = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "edit-sprint" */
            "./components/sprints/EditSprint.vue"
            )
    ),
    GanttInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "gantt-information" */
            "./components/gantt_chart/GanttInformation.vue"
            )
    ),
    GdprWizard = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "gdpr-wizard" */
            "./components/gdpr/GdprWizard.vue"
            )
    ),
    GroupInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "group-information" */
            "./components/groups/GroupInformation.vue"
            )
    ),
    KanbanDangerZone = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "kanban-danger-zone" */
            "./components/kanban/KanbanDangerZone.vue"
            )
    ),
    KanbanEditBoard = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "kanban-edit-board" */
            "./components/kanban/KanbanEditBoard.vue"
            )
    ),
    KanbanGroupPermissions = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "kanban-group-permissions" */
            "./components/kanban/KanbanGroupPermissions.vue"
            )
    ),
    KanbanInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "kanban-information" */
            "./components/kanban/KanbanInformation.vue"
            )
    ),
    KanbanPublicLinks = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "kanban-public-links" */
            "./components/kanban/KanbanPublicLinks.vue"
            )
    ),
    ListSearchResults = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "list-search-results" */
            "./components/search/ListSearchResults.vue"
            )
    ),
    MdiMicrosoftExcel = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "mdi-microsoft-excel" */
            "./components/icons/MdiMicrosoftExcel.vue"
            )
    ),
    MdiMicrosoftPowerPoint = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "mdi-microsoft-power-point" */
            "./components/icons/MdiMicrosoftPowerPoint.vue"
            )
    ),
    MdiMicrosoftWord = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "mdi-microsoft-word" */
            "./components/icons/MdiMicrosoftWord.vue"
            )
    ),
    MyPlanner = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "my-planner" */
            "./components/my_planner/MyPlanner.vue"
            )
    ),
    NewCustomer = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-customer" */
            "./components/customers/NewCustomer.vue"
            )
    ),
    NewGroup = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-group" */
            "./components/groups/NewGroup.vue"
            )
    ),
    NewKanban = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-kanban" */
            "./components/kanban/NewKanban.vue"
            )
    ),
    NewNotification = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-notification" */
            "./components/notifications/NewNotification.vue"
            )
    ),
    NewPermissionSet = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-permission-set" */
            "./components/permissions/NewPermissionSet.vue"
            )
    ),
    NewOrganisation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-permission-set" */
            "./components/organisations/NewOrganisation.vue"
            )
    ),
    NewProject = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-project" */
            "./components/projects/NewProject.vue"
            )
    ),
    NewRequestForChange = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-request-for-change" */
            "./components/request_for_change/NewRequestForChange.vue"
            )
    ),
    NewRequirement = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-requirement" */
            "./components/requirements/NewRequirement.vue"
            )
    ),
    NewScheduledObject = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-scheduled-object" */
            "./components/object_scheduler/NewScheduledObject.vue"
            )
    ),
    NewTask = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-task" */
            "./components/tasks/NewTask.vue"
            )
    ),
    NewUser = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "new-user" */
            "./components/users/NewUser.vue"
            )
    ),
    NotificationInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "notification-information" */
            "./components/notifications/NotificationInformation.vue"
            )
    ),
    ObjectStatusInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "object-status-information" */
            "./components/object_status/ObjectStatusInformation.vue"
            )
    ),
    ObjectStatusList = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "object-status-list" */
            "./components/object_status/ObjectStatusList.vue"
            )
    ),
    OrganisationInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "organisation-information" */
            "./components/organisations/OrganisationInformation.vue"
            )
    ),
    OrganisationModules = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "organisation-modules" */
            "./components/organisations/OrganisationModules.vue"
            )
    ),
    ParentModules = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "parent-modules" */
            "./components/modules/ParentModules.vue"
            )
    ),
    PermissionInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "permission-information" */
            "./components/permissions/PermissionInformation.vue"
            )
    ),
    ProjectInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "project-information" */
            "./components/projects/ProjectInformation.vue"
            )
    ),
    ProfileInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "profile-information" */
            "./components/profile/ProfileInformation.vue"
            )
    ),
    PublicCardInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "public-card-information" */
            "./components/public/public_card_information.vue"
            )
    ),
    PublicKanbanBoard = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "public-kanban-board" */
            "./components/public/public_kanban_board.vue"
            )
    ),
    PublicRequirementItemList = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "public-requirement-item-list" */
            "./components/public/public_requirement_item_list.vue"
            )
    ),
    RenderToasts = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "render-toasts" */
            "./components/render/RenderToasts.vue"
            )
    ),
    ResetUserPassword = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "reset-user-password" */
            "./components/users/ResetUserPassword.vue"
            )
    ),
    RfcInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "rfc-Information" */
            "./components/request_for_change/RfcInformation.vue"
            )
    ),
    RfcModules = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "rfc-modules" */
            "./components/request_for_change/RfcModules.vue"
            )
    ),
    RequirementInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "requirement-information" */
            "./components/requirements/RequirementInformation.vue"
            )
    ),
    RequirementItemInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "requirement-item-information" */
            "./components/requirement_items/RequirementItemInformation.vue"
            )
    ),
    ScheduleObjects = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "schedule-objects" */
            "./components/object_scheduler/ScheduleObjects.vue"
            )
    ),
    ScheduleObjectInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "schedule-object-information" */
            "./components/object_scheduler/ScheduledObjectInformation.vue"
            )
    ),
    SearchCustomers = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-customers" */
            "./components/search/SearchCustomers.vue"
            )
    ),
    SearchGroups = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-groups" */
            "./components/search/SearchGroups.vue"
            )
    ),
    SearchNotifications = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-notifications" */
            "./components/search/SearchNotifications.vue"
            )
    ),
    SearchObjects = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-objects" */
            "./components/search/SearchObjects.vue"
            )
    ),
    SearchOrganisations = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-organisations" */
            "./components/search/SearchOrganisations.vue"
            )
    ),
    SearchPermissionSets = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-permission-sets" */
            "./components/search/SearchPermissionSets.vue"
            )
    ),
    SearchSprints = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-sprints" */
            "./components/search/SearchSprints.vue"
            )
    ),
    SearchTags = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-tags" */
            "./components/search/SearchTags.vue"
            )
    ),
    SearchUsers = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-users" */
            "./components/search/SearchUsers.vue"
            )
    ),
    SprintInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "sprint-information" */
            "./components/sprints/SprintInformation.vue"
            )
    ),
    TaskInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "task-information" */
            "./components/tasks/TaskInformation.vue"
            )
    ),
    UpdateProfilePicture = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "update-profile-picture" */
            "./components/profile/UpdateProfilePicture.vue"
            )
    ),
    UserInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "user-information" */
            "./components/users/UserInformation.vue"
            )
    ),
    UserList = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "user-list" */
            "./components/administration/UserList.vue"
            )
    );
