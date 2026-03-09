import 'vite/modulepreload-polyfill';
import 'whelk-ui/dist/whelk-ui.css';
import axios from "axios";
import {createApp} from "vue";
import LoginApp from "@/pages/login_app/LoginApp.vue";
import loginRouter from "./router/loginRouter.ts";
import i18n from "@/i18n.ts";

// Setup Axios Instance
const axiosInstance = axios.create({
    withCredentials: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFTOKEN",
});

const loginApp = createApp(LoginApp);

// Configure app
loginApp.provide('apiClient', axiosInstance);

// Setup app
loginApp.use(i18n);
loginApp.use(loginRouter);
loginApp.mount("#loginApp");
