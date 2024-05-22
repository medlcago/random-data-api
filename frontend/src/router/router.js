import LoginPage from "@/pages/LoginPage.vue";
import RegistrationPage from "@/pages/RegistrationPage.vue";
import {createRouter, createWebHistory} from "vue-router";
import ForgotPasswordPage from "@/pages/ForgotPasswordPage.vue";
import NotFoundPage from "@/pages/NotFoundPage.vue";
import ProfilePage from "@/pages/ProfilePage.vue";
import {logoutUser, refreshAccessToken, verifyAccessToken} from "@/services/auth.js";

const routes = [
    {
        path: "/",
        redirect: "/login"
    },
    {
        path: "/logout",
        redirect: "/login"
    },
    {
        path: "/login",
        component: LoginPage,
        name: "login"

    },
    {
        path: "/profile",
        component: ProfilePage,
        name: "profile",
        meta: {
            requiresAuth: true
        }
    },
    {
        path: "/registration",
        component: RegistrationPage,
        name: "registration"

    },
    {
        path: "/forgot-password",
        component: ForgotPasswordPage,
        name: "forgot-password"
    },
    {
        path: "/:pathMatch(.*)*",
        component: NotFoundPage
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

router.beforeEach(async (to, from, next) => {
    const isLoggedIn = await verifyAccessToken();

    if (to.meta.requiresAuth && !isLoggedIn) {
        if (await refreshAccessToken()) {
            next();
        } else {
            await logoutUser();
            next("/login");
        }
    } else if (isLoggedIn && (to.name === "login" || to.name === "registration")) {
        next("/profile");
    } else {
        next();
    }
});

export default router;