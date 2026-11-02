import 'vite/modulepreload-polyfill';
import 'whelk-ui/dist/whelk-ui.css'
import { createPinia } from "pinia";
import { createApp } from "vue";
import {App} from "./pages/app";
import i18n, {loadLocale} from "./i18n";
import router from "./router/router.ts";

const pinia = createPinia();
const app = createApp(App);
app.use(pinia);

app.use(router);
app.use(i18n);

// Wait for the page language so the first render is already translated
loadLocale().finally(() => app.mount("#app"));
