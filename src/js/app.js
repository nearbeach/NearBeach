//import Vue from 'vue';
import Vue from 'vue/dist/vue.js';

//Vue Component Library
import GetStakeholders from './components/organisations/GetStakeholders.vue';
import NewRequirements from './components/requirements/NewRequirement.vue';

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
Vue.component('axios',axios);
Vue.component('bootstrap',bootstrap);
Vue.component('vSelect',vSelect);
Vue.component('Editor',Editor);

//Construction of the VUE App
window.vm = new Vue({
    el: "#app",
    components: {
        GetStakeholders,
        NewRequirements,
    },
    data() {
        return {};
    },
    methods: {},
    mounted() {
        //Remove the loader
        var elem = document.getElementById("loader");
        elem.style.display = "none";
    }
});
