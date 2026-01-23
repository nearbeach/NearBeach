import 'vite/modulepreload-polyfill';
import axios from "axios";
import {createApp} from "vue";
import LoginApp from "@/pages/login_app/LoginApp.vue";
import i18n from "./i18n";
import loginRouter from "./router/loginRouter.ts";

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
loginApp.use(loginRouter);
loginApp.use(i18n);
loginApp.mount("#loginApp");
