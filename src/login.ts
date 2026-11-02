import 'vite/modulepreload-polyfill';
import 'whelk-ui/dist/whelk-ui.css';
import {createApp} from "vue";
import LoginApp from "@/pages/login_app/LoginApp.vue";
import loginRouter from "./router/loginRouter.ts";
import i18n, {loadLocale} from "@/i18n.ts";

const loginApp = createApp(LoginApp);

// Setup app
loginApp.use(i18n);
loginApp.use(loginRouter);

// Wait for the page language so the first render is already translated
loadLocale().finally(() => loginApp.mount("#loginApp"));
