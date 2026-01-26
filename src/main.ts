import 'vite/modulepreload-polyfill';
import 'whelk-ui/dist/whelk-ui.css'
import { createPinia } from "pinia";
import { createApp } from "vue";
import App from "./pages/app/App.vue";
import i18n from "./i18n";
import router from "./router/router.ts";

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(i18n);
app.use(pinia);
app.mount("#app");
