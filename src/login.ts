import 'vite/modulepreload-polyfill';
import 'whelk-ui/dist/whelk-ui.css';
import {createApp} from "vue";
import LoginApp from "@/pages/login_app/LoginApp.vue";
import loginRouter from "./router/loginRouter.ts";
import i18n from "@/i18n.ts";

const loginApp = createApp(LoginApp);

// Setup app
loginApp.use(i18n);
loginApp.use(loginRouter);
loginApp.mount("#loginApp");
