import { defineAsyncComponent } from 'vue/dist/vue.esm-bundler';

export const
    DashboardMyObjects = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-my-objects" */
            './components/dashboard/DashboardMyObjects.vue'
        )
    ),
    DashboardRfcApprovals = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-rfc-approvals" */
            './components/dashboard/DashboardRfcApprovals.vue'
        )
    ),
    DashboardUnassignedObjects = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-unassigned-objects" */
            './components/dashboard/DashboardUnassignedObjects.vue'
        )
    ),
    DashboardUsersWithNoGroups = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "dashboard-users-with-no-groups" */
            './components/dashboard/DashboardUsersWithNoGroups.vue'
        )
    ),
    GroupInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "group-information" */
            './components/groups/GroupInformation.vue'
        )
    ),
    ListSearchResults = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "list-search-results" */
            './components/search/ListSearchResults.vue'
        )
    ),
    // NewCustomer = defineAsyncComponent(() =>
    //     import(
    //         /* webpackChunkName: "new-customer" */
    //         './components/customers/NewCustomer.vue'
    //     )
    // ),
    // NewOrganisation = defineAsyncComponent(() =>
    //     import(
    //         /* webpackChunkName: "new-customer" */
    //         './components/organisations/NewOrganisation.vue'
    //     )
    // )
    ProfileInformation = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "profile-information" */
            './components/profile/ProfileInformation.vue'
        )
    ),
    ResetUserPassword = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "reset-user-password" */
            './components/users/ResetUserPassword.vue'
        )
    ),
    SearchCustomers = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-customers" */
            './components/search/SearchCustomers.vue'
        )
    ),
    SearchGroups = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-groups" */
            './components/search/SearchGroups.vue'
        )
    ),
    SearchObjects = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-objects" */
            './components/search/SearchObjects.vue'
        )
    ),
    SearchOrganisations = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-organisations" */
            './components/search/SearchOrganisations.vue'
        )
    ),
    SearchPermissionSets = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-permission-sets" */
            './components/search/SearchPermissionSets.vue'
        )
    ),
    SearchTags = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-tags" */
            './components/search/SearchTags.vue'
        )
    ),
    SearchUsers = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "search-users" */
            './components/search/SearchUsers.vue'
        )
    ),
    UserList = defineAsyncComponent(() =>
        import(
            /* webpackChunkName: "user-list" */
            './components/administration/UserList.vue'
        )
    )
