import {createRouter, createWebHistory} from "vue-router";

// Async components
const ForgottenPassword = () => import("@/components/login/forgotten_password/ForgottenPassword.vue");
const LoginPage = () => import("@/components/login/login_page/LoginPage.vue");
const PasswordReset = () => import("@/components/login/password_reset/PasswordReset.vue");

// Define the routes
const loginRoutes = [
    {
        path: "/login",
        component: LoginPage,
        name: "login",
    },
    {
        path: "/login/forgotten-password",
        component: ForgottenPassword,
        name: "forgotten-password",
    },
    {
        path: "/login/password-reset",
        component: PasswordReset,
        name: "password-reset",
    },
    // Fall back page
    {
        path: "/:catchAll(.*)*",
        redirect: () => {
            return {path: '/login' }
        },
    }
]

// Router setup
const loginRouter = createRouter({
    history: createWebHistory(),
    routes: loginRoutes,
});

export {loginRoutes};

export default loginRouter;
