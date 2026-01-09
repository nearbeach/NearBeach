import {createRouter, createWebHistory} from "vue-router";

// Async components
const DashboardPage = () =>
    import("@/components/dashboard/dashboard_page/DashboardPage.vue");
const NewProject = () =>
    import("@/components/project/new_project/NewProject.vue");
const NotFoundPage = () =>
    import("@/components/error/NotFoundPage/NotFoundPage.vue");
const PlaygroundPage = () =>
    import("@/components/playground/PlaygroundPage.vue");
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
            {path: "", component: DashboardPage, name: "SearchKanbanBoard"},
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
            {path: "", component: DashboardPage, name: "SearchRequirement"},
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
            {path: "", component: DashboardPage, name: "SearchTask"},
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
            {path: "", component: DashboardPage, name: "SearchRequestForChange"},
            {path: "new", component: DashboardPage, name: "NewRequestForChange"},
            {path: ":id", component: DashboardPage, name: "RequestForChange"},
        ],
    },
    {
        path: "/logout",
        meta: {
            destination: "logout",
        },
        component: PlaygroundPage,
    },
    // Fall back page
    {
        path: "/:catchAll(.*)*",
        component: NotFoundPage,
    },
];

// Router setup
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: routes,
});

export {routes};

export default router;
