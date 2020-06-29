//import Vue from 'vue';
import Vue from 'vue/dist/vue.js';

//Vue Component Library
// import ListBugs from './components/requirements/ListBugs.vue';
// import ListRequirementItems from './components/requirements/ListRequirementItems.vue';
// import ListRequirementLinks from './components/requirements/ListRequirementLinks.vue';
// import RequirementInformation from './components/requirements/RequirementInformation.vue';
// import TabComponents from './components/requirements/TabComponents.vue';


//Import jquery
var $ = require('jquery');
global.jQuery = $;

//Import Foundation
import Foundation from 'foundation-sites';

//SCSS Library
import './sass/main.scss';

//Font awesome
import '@fortawesome/fontawesome-free/js/fontawesome';
import '@fortawesome/fontawesome-free/js/solid';
import '@fortawesome/fontawesome-free/js/regular';
import '@fortawesome/fontawesome-free/js/brands';

//custom javascript
import './js/global.js';

//Construction of the VUE APp
window.vm = new Vue({
    el: "#app",
    components: {},
    data() {
        return {};
    },
    methods: {},
});
