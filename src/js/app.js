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
