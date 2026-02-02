import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import { initTheme } from "./state/theme";

// Supports weights 300-700
import "@fontsource-variable/space-grotesk";
import "@fontsource/material-icons-outlined";
// Supports weights 100-700
import "@fontsource-variable/material-symbols-outlined";

initTheme();

const app = createApp(App);
app.use(router);
app.mount("#app");
