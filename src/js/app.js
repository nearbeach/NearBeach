//Vue
import {createApp} from "vue/dist/vue.esm-bundler";

//VueX
import {store} from "./vuex-store";

//Import Bootstrap
import {createPopper} from "@popperjs/core";
import bootstrap from "bootstrap";

//SCSS Library
import "../sass/main.scss";

//custom javascript
import "./global.js";

//Import axios for ajax
const axios = require("axios");
const axiosInstance = axios.create({
    withCredentials: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFTOKEN",
});

//nextTick
import {nextTick} from 'vue';

//Naive-ui
import {NConfigProvider} from "naive-ui";

//Lazy Load Parent Components
import {
    //BugsModule,
    ChangeTaskInformation,
    ChangeTaskModules,
    ConfirmKanbanBoardClosure,
    ConfirmKanbanBoardReopen,
    CustomerInformation,
    DashboardKanbanList,
    DashboardMyObjects,
    DashboardRfcApprovals,
    DashboardUnassignedObjects,
    DashboardUsersWithNoGroups,
    DiagnosticInformation,
    GroupInformation,
    KanbanDangerZone,
    KanbanEditBoard,
    KanbanGroupPermissions,
    KanbanInformation,
    KanbanPublicLinks,
    ListSearchResults,
    NewCustomer,
    NewGroup,
    NewKanban,
    NewNotification,
    NewOrganisation,
    NewPermissionSet,
    NewProject,
    NewRequestForChange,
    NewRequirement,
    NewTask,
    NewUser,
    NotificationInformation,
    ObjectStatusInformation,
    ObjectStatusList,
    OrganisationInformation,
    OrganisationModules,
    ParentModules,
    PermissionInformation,
    ProfileInformation,
    ProjectInformation,
    PublicCardInformation,
    PublicKanbanBoard,
    PublicRequirementItemList,
    RenderToasts,
    RequirementInformation,
    RequirementItemInformation,
    ResetUserPassword,
    RfcInformation,
    RfcModules,
    SearchCustomers,
    SearchGroups,
    SearchNotifications,
    SearchObjects,
    SearchOrganisations,
    SearchPermissionSets,
    SearchSprints,
    SearchTags,
    SearchUsers,
    SprintInformation,
    TaskInformation,
    UpdateProfilePicture,
    UserInformation,
    UserList,
} from "./components";

//Construction of the VUE App
const app = createApp({
    components: {
        //BugsModule,
        ConfirmKanbanBoardClosure,
        ConfirmKanbanBoardReopen,
        ChangeTaskInformation,
        ChangeTaskModules,
        CustomerInformation,
        DashboardKanbanList,
        DashboardMyObjects,
        DashboardRfcApprovals,
        DashboardUnassignedObjects,
        DashboardUsersWithNoGroups,
        DiagnosticInformation,
        GroupInformation,
        KanbanDangerZone,
        KanbanEditBoard,
        KanbanGroupPermissions,
        KanbanInformation,
        KanbanPublicLinks,
        ListSearchResults,
        NewCustomer,
        NewGroup,
        NewKanban,
        NewNotification,
        NewOrganisation,
        NewPermissionSet,
        NewProject,
        NewRequestForChange,
        NewRequirement,
        NewTask,
        NewUser,
        NotificationInformation,
        ObjectStatusInformation,
        ObjectStatusList,
        OrganisationInformation,
        OrganisationModules,
        ParentModules,
        PermissionInformation,
        ProfileInformation,
        ProjectInformation,
        PublicCardInformation,
        PublicKanbanBoard,
        PublicRequirementItemList,
        RenderToasts,
        RequirementInformation,
        RequirementItemInformation,
        ResetUserPassword,
        RfcInformation,
        RfcModules,
        SearchCustomers,
        SearchGroups,
        SearchNotifications,
        SearchObjects,
        SearchOrganisations,
        SearchPermissionSets,
        SearchSprints,
        SearchTags,
        SearchUsers,
        SprintInformation,
        TaskInformation,
        UpdateProfilePicture,
        UserInformation,
        UserList,
    },
    mounted() {
        //Remove the loader
        const loader_elem = document.getElementById("loader");
        loader_elem.style.transform = "translateY(-100vh)";

        //Remove the element when we are finished with it
        setTimeout(() => {
            //Destroy the evidance
            loader_elem.remove();
        }, 500);
    },
});
app.config.devtools = true;
app.use(store);
app.config.globalProperties.axios=axiosInstance;
app.component("NConfigProvider", NConfigProvider);
app.mount("#app");
