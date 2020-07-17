//import Vue from 'vue';
import Vue from 'vue/dist/vue.js';

//Vue Component Library
import NewRequirements from './components/requirements/NewRequirement.vue';

//Import jquery
var $ = require('jquery');
global.jQuery = $;

//Import Foundation
import Foundation from 'foundation-sites';

//SCSS Library
import '../sass/main.scss';

//Font awesome
//import '@fortawesome/fontawesome-free/js/fontawesome';
//import '@fortawesome/fontawesome-free/js/solid';
// import '@fortawesome/fontawesome-free/js/regular';
// import '@fortawesome/fontawesome-free/js/brands';

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

//Construction of the VUE App
window.vm = new Vue({
    el: "#app",
    components: {
        Editor,
        NewRequirements,
        vSelect,
        axios,
    },
    data() {
        return {};
    },
    methods: {},
    mounted() {
        console.log("VUE JS MOUNTED");
    }
});
