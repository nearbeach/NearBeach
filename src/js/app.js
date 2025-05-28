//Vue
import {createApp} from "vue/dist/vue.esm-bundler";

//VueX
import {store} from "./vuex-store";

//Import Bootstrap



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


//Naive-ui
import {NConfigProvider} from "naive-ui";

//Lazy Load Parent Components
import {
    CarbonArrowUp,
    CarbonCloseOutline,
    CarbonDocument,
    CarbonDocumentPdf,
    CarbonEmail,
    CarbonFolder,
    CarbonImage,
    CarbonInformation,
    CarbonLink,
    CarbonTrashCan,
    ChangeTaskInformation,
    ChangeTaskModules,
    ConfirmKanbanBoardClosure,
    ConfirmKanbanBoardReopen,
    CustomerInformation,
    CustomerModules,
    DashboardKanbanList,
    DashboardMyObjects,
    DashboardRfcApprovals,
    DashboardTodoToday,
    DashboardUnassignedObjects,
    DashboardUsersWithNoGroups,
    DiagnosticInformation,
    EditSprint,
    GanttInformation,
    GdprWizard,
    GroupInformation,
    KanbanDangerZone,
    KanbanEditBoard,
    KanbanGroupPermissions,
    KanbanInformation,
    KanbanPublicLinks,
    ListSearchResults,
    MdiMicrosoftExcel,
    MdiMicrosoftPowerPoint,
    MdiMicrosoftWord,
    MyPlanner,
    NewCustomer,
    NewGroup,
    NewKanban,
    NewNotification,
    NewOrganisation,
    NewPermissionSet,
    NewProject,
    NewRequestForChange,
    NewRequirement,
    NewScheduledObject,
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
    ScheduleObjects,
    ScheduleObjectInformation,
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
        CarbonArrowUp,
        CarbonCloseOutline,
        CarbonDocument,
        CarbonDocumentPdf,
        CarbonEmail,
        CarbonFolder,
        CarbonImage,
        CarbonInformation,
        CarbonLink,
        CarbonTrashCan,
        ConfirmKanbanBoardClosure,
        ConfirmKanbanBoardReopen,
        ChangeTaskInformation,
        ChangeTaskModules,
        CustomerInformation,
        CustomerModules,
        DashboardKanbanList,
        DashboardMyObjects,
        DashboardRfcApprovals,
        DashboardTodoToday,
        DashboardUnassignedObjects,
        DashboardUsersWithNoGroups,
        DiagnosticInformation,
        EditSprint,
        GanttInformation,
        GdprWizard,
        GroupInformation,
        KanbanDangerZone,
        KanbanEditBoard,
        KanbanGroupPermissions,
        KanbanInformation,
        KanbanPublicLinks,
        ListSearchResults,
        MdiMicrosoftExcel,
        MdiMicrosoftPowerPoint,
        MdiMicrosoftWord,
        MyPlanner,
        NewCustomer,
        NewGroup,
        NewKanban,
        NewNotification,
        NewOrganisation,
        NewPermissionSet,
        NewProject,
        NewRequestForChange,
        NewRequirement,
        NewScheduledObject,
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
        ScheduleObjects,
        ScheduleObjectInformation,
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
