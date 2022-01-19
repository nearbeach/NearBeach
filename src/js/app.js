//Vue
import { createApp } from 'vue/dist/vue.esm-bundler';

//VueX
// import { createStore } from 'vuex';
import { store } from './vuex-store';

//Import Bootstrap
import { createPopper } from '@popperjs/core';
import bootstrap from 'bootstrap';

//SCSS Library
import '../sass/main.scss';

//custom javascript
import './global.js';

//Import axios for ajax
const axios = require('axios');
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';

//Lazy Load Parent Components
import {
    ChangeTaskInformation,
    CustomerInformation,
    DashboardMyObjects,
    DashboardRfcApprovals,
    DashboardUnassignedObjects,
    DashboardUsersWithNoGroups,
    GroupInformation,
    KanbanEditBoard,
    KanbanGroupPermissions,
    KanbanInformation,
    ListSearchResults,
    NewCustomer,
    NewGroup,
    NewKanban,
    NewOrganisation,
    NewPermissionSet,
    NewProject,
    NewRequestForChange,
    NewRequirement,
    NewTask,
    OrganisationInformation,
    OrganisationModules,
    ParentModules,
    PermissionInformation,
    ProfileInformation,
    ProjectInformation,
    RequirementInformation,
    RequirementItemInformation,
    ResetUserPassword,
    RfcInformation,
    SearchCustomers,
    SearchGroups,
    SearchObjects,
    SearchOrganisations,
    SearchPermissionSets,
    SearchTags,
    SearchUsers,
    TaskInformation,
    UserInformation,
    UserList,
} from './components';

//Construction of the VUE App
const app = createApp({
    components: {
        ChangeTaskInformation,
        CustomerInformation,
        DashboardMyObjects,
        DashboardRfcApprovals,
        DashboardUnassignedObjects,
        DashboardUsersWithNoGroups,
        GroupInformation,
        KanbanEditBoard,
        KanbanGroupPermissions,
        KanbanInformation,
        ListSearchResults,
        NewCustomer,
        NewGroup,
        NewKanban,
        NewOrganisation,
        NewPermissionSet,
        NewProject,
        NewRequestForChange,
        NewRequirement,
        NewTask,
        OrganisationInformation,
        OrganisationModules,
        ParentModules,
        PermissionInformation,
        ProfileInformation,
        ProjectInformation,
        RequirementInformation,
        RequirementItemInformation,
        ResetUserPassword,
        RfcInformation,
        SearchCustomers,
        SearchGroups,
        SearchObjects,
        SearchOrganisations,
        SearchPermissionSets,
        SearchTags,
        SearchUsers,
        TaskInformation,
        UserInformation,
        UserList,
    },
    mounted() {
        //Remove the loader
        var loader_elem = document.getElementById('loader');
        loader_elem.style.transform = 'translateY(-100vh)';

        //Remove the element when we are finished with it
        setTimeout(() => {
            //Destroy the evidance
            loader_elem.remove();
        }, 500);
    },
})
app.use(store)
app.mount("#app")
