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
import NewRequirements from './components/requirements/NewRequirement.vue';
import NewHistoryNoteWizard from "./components/modules/wizards/NewHistoryNoteWizard.vue";
import NewRequirementItemWizard from "./components/modules/wizards/NewRequirementItemWizard.vue";
import NewRequirementLinkWizard from "./components/modules/wizards/NewRequirementLinkWizard.vue";
import RequirementInformation from './components/requirements/RequirementInformation.vue';
import RequirementItemsModule from "./components/modules/sub_modules/RequirementItemsModule.vue";
import RequirementLinksModule from "./components/modules/sub_modules/RequirementLinksModule.vue";
import UploadDocumentWizard from "./components/modules/wizards/UploadDocumentWizard.vue";

//Import Bootstrap
import { createPopper } from '@popperjs/core';
import bootstrap from 'bootstrap'

//SCSS Library
import '../sass/main.scss';

//TinyMce
import Editor from '@tinymce/tinymce-vue'

//vSelect
import vSelect from "vue-select";

//custom javascript
import './global.js';

//Import axios for ajax
const axios = require('axios');
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

//Global Vue Components
Vue.component('vSelect',vSelect);
Vue.component('Editor',Editor);

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
Vue.component('NewRequirements',NewRequirements);
Vue.component('NewHistoryNoteWizard',NewHistoryNoteWizard);
Vue.component('NewRequirementItemWizard',NewRequirementItemWizard);
Vue.component('NewRequirementLinkWizard',NewRequirementLinkWizard);
Vue.component('RequirementInformation',RequirementInformation);
Vue.component('RequirementItemsModule',RequirementItemsModule);
Vue.component('RequirementLinksModule',RequirementLinksModule);
Vue.component('UploadDocumentWizard',UploadDocumentWizard);

//Validation
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)

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
