import 'vite/modulepreload-polyfill';
import 'whelk-ui/dist/whelk-ui.css'
import { createPinia } from "pinia";
import { createApp } from "vue";
import {App} from "./pages/app/";
import i18n from "./i18n";
import router from "./router/router.ts";

const pinia = createPinia();
const app = createApp(App);
app.use(pinia);

app.use(router);
app.use(i18n);
app.mount("#app");
