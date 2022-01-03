//Vue
import { createApp, defineAsyncComponent } from 'vue';

//VueX
import { createStore } from 'vuex';

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
// const HelloWorld = defineAsyncComponent(() =>
//     import('./components/HelloWorld.vue')
// )

import HelloWorld from './components/HelloWorld.vue';

//Construction of the VUE App
let app = new createApp({
  components: {
    HelloWorld,
  }
})
app.mount("#app")
