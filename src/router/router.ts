import {createRouter, createWebHistory} from "vue-router";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Async components
const DashboardPage = () =>
    import("@/components/dashboard/dashboard_page/DashboardPage.vue");
const NewProject = () =>
    import("@/components/project/new_project/NewProject.vue");
const NotFoundPage = () =>
    import("@/components/error/NotFoundPage/NotFoundPage.vue");
const ProjectPage = () =>
    import("@/components/project/project_page/ProjectPage.vue");
const SearchPage = () => import("@/components/search/SearchPage.vue");

// Define the routes
const routes = [
    {
        path: "/",
        component: DashboardPage,
        name: "Dashboard",
        meta: {
            destination: "dashboard",
        },
    },
    {
        path: "/project",
        meta: {
            destination: "project",
        },
        children: [
            {path: "", component: SearchPage, name: "SearchProject"},
            {path: "new", component: NewProject, name: "NewProject"},
            {path: ":id", component: ProjectPage, name: "Project"},
        ],
    },
    {
        path: "/kanban_board",
        meta: {
            destination: "kanban_board",
        },
        children: [
            {path: "", component: SearchPage, name: "SearchKanbanBoard"},
            {path: "new", component: DashboardPage, name: "NewKanbanBoard"},
            {path: ":id", component: DashboardPage, name: "KanbanBoard"},
        ],
    },
    {
        path: "/requirement",
        meta: {
            destination: "requirement",
        },
        children: [
            {path: "", component: SearchPage, name: "SearchRequirement"},
            {path: "new", component: DashboardPage, name: "NewRequirement"},
            {path: ":id", component: DashboardPage, name: "Requirement"},
        ],
    },
    {
        path: "/task",
        meta: {
            destination: "task",
        },
        children: [
            {path: "", component: SearchPage, name: "SearchTask"},
            {path: "new", component: DashboardPage, name: "NewTask"},
            {path: ":id", component: DashboardPage, name: "Task"},
        ],
    },
    {
        path: "/request_for_change",
        meta: {
            destination: "request_for_change",
        },
        children: [
            {path: "", component: SearchPage, name: "SearchRequestForChange"},
            {path: "new", component: DashboardPage, name: "NewRequestForChange"},
            {path: ":id", component: DashboardPage, name: "RequestForChange"},
        ],
    },
    // Errors
    {
        path: "/forbidden",
        name: "forbidden",
        meta: {
            destination: "forbidden",
        },
        component: DashboardPage,
    },
    {
        path: "/not-found",
        name: "not-found",
        meta: {
            destination: "not-found",
        },
        component: NotFoundPage,
    },
    // Fall back page
    {
        path: "/:catchAll(.*)*",
        component: NotFoundPage,
    },
];

// Router setup
const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});

router.beforeEach(async (to, _, next) => {
    // Setup store
    const permissionStore = usePermissionStore();
    const destination: string | undefined = to.meta.destination as string | undefined;

    // Check user permissions has been loaded - other load
    if (!permissionStore.isLoaded) {
        await permissionStore.fetchPermissionData();
    }

    // Validated the permissions
    if (destination === undefined || destination === "not-found" || destination === "forbidden") {
        next();
    } else if (permissionStore.hasPermission(destination)) {
        next();
    } else {
        next({ name: "forbidden" })
    }
});

export {routes};

export default router;
