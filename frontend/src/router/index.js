import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/Home.vue";
import AboutView from "../views/About.vue";
import UserSignInView from "../views/UserSignIn.vue";
import NotFoundView from "../views/NotFound.vue";
import UserRegisterView from "../views/UserRegister.vue";
import DisplayBooksView from "../views/DisplayBooks.vue";
import DisplaySectionsView from "../views/DisplaySections.vue";
import AddBooksView from "../views/AddBooks.vue";
import AddSectionsView from "../views/AddSections.vue";
import UpdateBooksView from "../views/UpdateBooks.vue";
import UpdateSectionsView from "../views/UpdateSections.vue";
import ProfileView from "../views/Profile.vue";
import AdminDashboardView from "@/views/AdminDashboard.vue";
import ReadBookView from "@/views/ReadBook.vue";
import DisplaySectionBooksView from "@/views/DisplaySectionBooks.vue";
import AddReviewView from "@/views/AddReview.vue";
import DisplayReviewsView from "@/views/DisplayReviews.vue";
import DisplayUsersView from "@/views/DisplayUsers.vue";

const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
    },
    {
        path: "/about",
        name: "about",
        component: AboutView,
    },
    {
        path: "/login",
        name: "user-sign-in",
        component: UserSignInView,
    },
    {
        path: "/register/user",
        name: "user-register",
        component: UserRegisterView,
    },
    {
        path: "/display/books",
        name: "display-books",
        component: DisplayBooksView,
    },
    {
        path: "/display/sections",
        name: "display-sections",
        component: DisplaySectionsView,
    },
    {
        path: "/add/books",
        name: "add-books",
        component: AddBooksView,
    },
    {
        path: "/add/sections",
        name: "add-sections",
        component: AddSectionsView,
    },
    {
        path: "/update/sections/:id",
        name: "update-sections",
        component: UpdateSectionsView,
    },
    {
        path: "/update/books/:id",
        name: "update-books",
        component: UpdateBooksView,
    },
    {
        path: "/profile/:userid",
        name: "profile",
        component: ProfileView,
    },
    {
        path: "/dashboard",
        name: "admin-dashboard",
        component: AdminDashboardView,
    },
    {
        path: "/read/books/:id",
        name: "read-book",
        component: ReadBookView,
    },
    {
        path: "/display/section-books/:id",
        name: "display-section-books",
        component: DisplaySectionBooksView,
    },
    {
        path: "/add-review/:id",
        name: "add-review",
        component: AddReviewView,
    },
    {
        path: "/display-reviews/:id",
        name: "display-review",
        component: DisplayReviewsView,
    },
    {
        path: "/display/users",
        name: "display-users",
        component: DisplayUsersView,
    },
    //catch all 404
    {
        path: "/:catchAll(.*)",
        name: "NotFound",
        component: NotFoundView,
    },
];

function isAuthenticated() {
    const user = localStorage.getItem("userSession");
    return user !== null;
}

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !isAuthenticated()) {
        next({ name: "login" });
    } else {
        next();
    }
});

export default router;
