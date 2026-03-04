import 'vite/modulepreload-polyfill';
import 'whelk-ui/dist/whelk-ui.css'
import axios from "axios";
import { createPinia } from "pinia";
import { createApp } from "vue";
import App from "./pages/app/App.vue";
import i18n from "./i18n";
import router from "./router/router.ts";

// Setup Axios Instance
const axiosInstance = axios.create({
    withCredentials: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFTOKEN",
});

const pinia = createPinia();
const app = createApp(App);
app.use(pinia);

// Configure app
app.provide('apiClient', axiosInstance);

app.use(router);
app.use(i18n);
app.mount("#app");
