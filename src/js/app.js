//import Vue from 'vue';
import Vue from 'vue/dist/vue.js';

//Vue Component Library
import BugsModule from "./components/modules/sub_modules/BugsModule.vue";
import CustomersModule from "./components/modules/sub_modules/CustomersModule.vue";
import DocumentsModule from "./components/modules/sub_modules/DocumentsModule.vue";
import GetStakeholders from './components/organisations/GetStakeholders.vue';
import GroupPermissions from "./components/permissions/GroupPermissions.vue";
import GroupsAndUsersModule from "./components/modules/sub_modules/GroupsAndUsersModule.vue";
import ParentModules from "./components/modules/ParentModules.vue";
import MiscModule from "./components/modules/sub_modules/MiscModule.vue";
import AddBugWizard from "./components/modules/wizards/AddBugWizard.vue";
import AddCustomerWizard from "./components/modules/wizards/AddCustomerWizard.vue";
import AddFolderWizard from "./components/modules/wizards/AddFolderWizard.vue";
import AddGroupWizard from "./components/modules/wizards/AddGroupWizard.vue";
import AddLinkWizard from "./components/modules/wizards/AddLinkWizard.vue";
import AddUserWizard from "./components/modules/wizards/AddUserWizard.vue";
import NewCustomer from './components/customers/NewCustomer.vue';
import NewOrganisation from './components/organisations/NewOrganisation.vue';
import NewRequirements from './components/requirements/NewRequirement.vue';
import NewHistoryNoteWizard from "./components/modules/wizards/NewHistoryNoteWizard.vue";
import NewRequirementItemWizard from "./components/modules/wizards/NewRequirementItemWizard.vue";
import NewRequirementLinkWizard from "./components/modules/wizards/NewRequirementLinkWizard.vue";
import RequirementInformation from './components/requirements/RequirementInformation.vue';
import RequirementItemLinksModule from "./components/modules/sub_modules/RequirementItemLinksModule.vue";
import RequirementItemsModule from "./components/modules/sub_modules/RequirementItemsModule.vue";
import RequirementLinksModule from "./components/modules/sub_modules/RequirementLinksModule.vue";
import UploadDocumentWizard from "./components/modules/wizards/UploadDocumentWizard.vue";
import RequirementItemInformation from "./components/requirement_items/RequirementItemInformation.vue";
import ListOrganisations from "./components/organisations/ListOrganisations.vue";
import SearchOrganisations from "./components/search/SearchOrganisations.vue";
import OrganisationInformation from "./components/organisations/OrganisationInformation.vue";
import OrganisationModules from "./components/organisations/OrganisationModules.vue";
import CustomersListModule from "./components/modules/sub_modules/CustomersListModule.vue";
import AssociatedObjects from "./components/modules/sub_modules/AssociatedObjects.vue";
import NewCustomerForm from "./components/customers/NewCustomerForm.vue";
import NewCustomerModal from "./components/customers/NewCustomerModal.vue";
import SearchCustomers from "./components/search/SearchCustomers.vue";
import ListCustomers from "./components/customers/ListCustomers.vue";
import CustomerInformation from "./components/customers/CustomerInformation.vue";
import SearchObjects from "./components/search/SearchObjects.vue";
import ListSearchResults from "./components/search/ListSearchResults.vue";
import ProjectInformation from "./components/projects/ProjectInformation.vue";
import NewProject from "./components/projects/NewProject.vue";
import TaskInformation from "./components/tasks/TaskInformation.vue";
import NewTask from "./components/tasks/NewTask.vue";
import BetweenDates from "./components/dates/BetweenDates.vue";
import StakeholderInformation from "./components/organisations/StakeholderInformation.vue";
import NewKanban from "./components/kanban/NewKanban.vue";
import KanbanPropertyOrder from "./components/kanban/KanbanPropertyOrder.vue";
import KanbanInformation from "./components/kanban/KanbanInformation.vue";
import KanbanCard from "./components/kanban/KanbanCard.vue";
import KanbanBoard from "./components/kanban/KanbanBoard.vue";
import KanbanRow from "./components/kanban/KanbanRow.vue";
import DashboardBugList from "./components/dashboard/DashboardBugList.vue";
import NewKanbanCard from "./components/modules/wizards/NewKanbanCard.vue";
import CardInformation from "./components/kanban/CardInformation.vue";
import ListNotes from "./components/modules/sub_modules/ListNotes.vue";
import NewKanbanLinkWizard from "./components/modules/wizards/NewKanbanLinkWizard.vue";
import DashboardMyObjects from "./components/dashboard/DashboardMyObjects.vue";
import RenderObjectTable from "./components/render/RenderObjectTable.vue";
import ObjectLinks from "./components/modules/sub_modules/ObjectLinks.vue";
import NewLinkWizard from "./components/modules/wizards/NewLinkWizard.vue";
import NewRequestForChange from "./components/request_for_change/NewRequestForChange.vue";
import RfcBackoutPlan from "./components/request_for_change/tabs/RfcBackoutPlan.vue";
import RfcDetails from "./components/request_for_change/tabs/RfcDetails.vue";
import RfcImplementationPlan from "./components/request_for_change/tabs/RfcImplementationPlan.vue";
import RfcRisk from "./components/request_for_change/tabs/RfcRisk.vue";
import RfcTestPlan from "./components/request_for_change/tabs/RfcTestPlan.vue";
import RfcDescription from "./components/request_for_change/tabs/RfcDescription.vue";
import RfcInformation from "./components/request_for_change/RfcInformation.vue";
import RfcModules from "./components/request_for_change/RfcModules.vue";
import RfcNewRunItem from "./components/request_for_change/modules/RfcNewRunItem.vue";
import RfcRunSheetList from "./components/request_for_change/modules/RfcRunSheetList.vue";
import DashboardRfcApprovals from "./components/dashboard/DashboardRfcApprovals.vue";
import RfcApprovalButtons from "./components/request_for_change/modules/RfcApprovalButtons.vue";
import SearchGroups from "./components/search/SearchGroups.vue";
import SearchPermissionSets from "./components/search/SearchPermissionSets.vue";
import SearchUsers from "./components/search/SearchUsers.vue";
import NewGroup from "./components/groups/NewGroup.vue";
import GroupInformation from "./components/groups/GroupInformation.vue";
import UserList from "./components/administration/UserList.vue";
import AdminAddUser from "./components/administration/AdminAddUser.vue";


//Import Bootstrap
import { createPopper } from '@popperjs/core';
import bootstrap from 'bootstrap'

//SCSS Library
import '../sass/main.scss';

//TinyMce
import Editor from '@tinymce/tinymce-vue'

//vSelect
import vSelect from "vue-select";

//VueSortable
import draggable from 'vuedraggable';


//custom javascript
import './global.js';

//D3 Elements
//import * as d3 from "d3";

//Import axios for ajax
const axios = require('axios');
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

//Global Vue Components
Vue.component('vSelect',vSelect);
Vue.component('Editor',Editor);
Vue.component('draggable',draggable);

//Global NearBeach Vue Components
Vue.component('AddBugWizard',AddBugWizard);
Vue.component('AddCustomerWizard',AddCustomerWizard);
Vue.component('AddFolderWizard',AddFolderWizard);
Vue.component('AddGroupWizard',AddGroupWizard);
Vue.component('AddLinkWizard',AddLinkWizard);
Vue.component('AddUserWizard',AddUserWizard);
Vue.component('BugsModule',BugsModule);
Vue.component('CustomersModule',CustomersModule);
Vue.component('DocumentsModule',DocumentsModule);
Vue.component('GetStakeholders',GetStakeholders);
Vue.component('GroupPermissions',GroupPermissions);
Vue.component('GroupsAndUsersModule',GroupsAndUsersModule);
Vue.component('ParentModules',ParentModules);
Vue.component('MiscModule',MiscModule);
Vue.component('NewCustomer',NewCustomer);
Vue.component('NewOrganisation',NewOrganisation);
Vue.component('NewRequirements',NewRequirements);
Vue.component('NewHistoryNoteWizard',NewHistoryNoteWizard);
Vue.component('NewRequirementItemWizard',NewRequirementItemWizard);
Vue.component('NewRequirementLinkWizard',NewRequirementLinkWizard);
Vue.component('RequirementInformation',RequirementInformation);
Vue.component('RequirementItemsModule',RequirementItemsModule);
Vue.component('RequirementItemLinksModule',RequirementItemLinksModule);
Vue.component('RequirementLinksModule',RequirementLinksModule);
Vue.component('UploadDocumentWizard',UploadDocumentWizard);
Vue.component('RequirementItemInformation',RequirementItemInformation);
Vue.component('ListOrganisations',ListOrganisations);
Vue.component('SearchOrganisations',SearchOrganisations);
Vue.component('OrganisationInformation',OrganisationInformation);
Vue.component('OrganisationModules',OrganisationModules);
Vue.component('CustomersListModule',CustomersListModule);
Vue.component('AssociatedObjects',AssociatedObjects);
Vue.component('NewCustomerForm',NewCustomerForm);
Vue.component('NewCustomerModal',NewCustomerModal);
Vue.component('SearchCustomers',SearchCustomers);
Vue.component('ListCustomers',ListCustomers);
Vue.component('CustomerInformation',CustomerInformation);
Vue.component('SearchObjects',SearchObjects);
Vue.component('ListSearchResults',ListSearchResults);
Vue.component('ProjectInformation',ProjectInformation);
Vue.component('NewProject',NewProject);
Vue.component('TaskInformation',TaskInformation);
Vue.component('NewTask',NewTask);
Vue.component('BetweenDates',BetweenDates);
Vue.component('StakeholderInformation',StakeholderInformation);
Vue.component('NewKanban',NewKanban);
Vue.component('KanbanPropertyOrder',KanbanPropertyOrder);
Vue.component('KanbanInformation',KanbanInformation);
Vue.component('KanbanCard',KanbanCard);
Vue.component('KanbanBoard',KanbanBoard);
Vue.component('KanbanRow',KanbanRow);
Vue.component('DashboardBugList',DashboardBugList);
Vue.component('NewKanbanCard',NewKanbanCard);
Vue.component('CardInformation',CardInformation);
Vue.component('ListNotes',ListNotes);
Vue.component('NewKanbanLinkWizard',NewKanbanLinkWizard);
Vue.component('DashboardMyObjects',DashboardMyObjects);
Vue.component('RenderObjectTable',RenderObjectTable);
Vue.component('ObjectLinks',ObjectLinks);
Vue.component('NewLinkWizard',NewLinkWizard);
Vue.component('NewRequestForChange',NewRequestForChange);
Vue.component('RfcBackoutPlan',RfcBackoutPlan);
Vue.component('RfcDetails',RfcDetails);
Vue.component('RfcImplementationPlan',RfcImplementationPlan);
Vue.component('RfcRisk',RfcRisk);
Vue.component('RfcTestPlan',RfcTestPlan);
Vue.component('RfcDescription',RfcDescription);
Vue.component('RfcInformation',RfcInformation);
Vue.component('RfcModules',RfcModules);
Vue.component('RfcNewRunItem',RfcNewRunItem);
Vue.component('RfcRunSheetList',RfcRunSheetList);
Vue.component('DashboardRfcApprovals',DashboardRfcApprovals);
Vue.component('RfcApprovalButtons',RfcApprovalButtons);
Vue.component('SearchGroups',SearchGroups);
Vue.component('SearchPermissionSets',SearchPermissionSets);
Vue.component('SearchUsers',SearchUsers);
Vue.component('NewGroup', NewGroup);
Vue.component('GroupInformation', GroupInformation);
Vue.component('UserList', UserList);
Vue.component('AdminAddUser', AdminAddUser);

//Validation
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)

//Vue-datetime
import { Datetime } from 'vue-datetime';
import 'vue-datetime/dist/vue-datetime.css'
Vue.use(Datetime);
Vue.component('datetime', Datetime);

//Feater Icons
const feather = require('feather-icons')

//Construction of the VUE App
window.vm = new Vue({
    el: "#app",
    components: {
        //Validation
        Vuelidate,

        //Icons
        feather,
    },
    data() {
        return {};
    },
    methods: {},
    mounted() {
        //Remove the loader
        var loader_elem = document.getElementById("loader");
        loader_elem.style.transform = "translateY(-100vh)";

        //Run the feather app
        feather.replace();
    }
});
