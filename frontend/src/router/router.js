import LoginPage from "@/components/LoginPage.vue";
import RegistrationPage from "@/components/RegistrationPage.vue";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: "/",
        redirect: "/login"
    },
    {
        path: "/login",
        component: LoginPage,
        name: "login"

    },
    {
        path: "/registration",
        component: RegistrationPage,
        name: "registration"

    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

export default router;