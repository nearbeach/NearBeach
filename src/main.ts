import { createPinia } from "pinia";
import { createApp } from "vue";
import App from "./App.vue";
// import "./styles/style.css";
import i18n from "./i18n";
import router from "./router/router.ts";

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(i18n);
app.use(pinia);
app.mount("#app");
