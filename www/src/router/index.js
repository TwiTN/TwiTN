import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import PostView from "../views/PostView.vue";
import UserView from "../views/UserView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/login", name: "login", component: LoginView },
    { path: "/signup", name: "signup", component: SignupView },
    { path: "/post/:id", name: "post", component: PostView, props: true },
    { path: "/user/:username", name: "user", component: UserView, props: true },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
