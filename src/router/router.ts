import {createRouter, createWebHistory} from "vue-router";
import {usePermissionStore} from "@/stores/permissions/permission.ts";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useUserStore} from "@/stores/user/user.ts";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import ServerErrorPage from "@/components/error/ServerErrorPage/ServerErrorPage.vue";
import ForbiddenPage from "@/components/error/ForbiddenPage/ForbiddenPage.vue";
import {useErrorStore} from "@/stores/error/error.ts";

// Async components
const DashboardPage = () =>
    import("@/components/dashboard/dashboard_page/DashboardPage.vue");
const NewProject = () =>
    import("@/components/new_object/NewObject.vue");
const NotFoundPage = () =>
    import("@/components/error/NotFoundPage/NotFoundPage.vue");
const ProjectPage = () =>
    import("@/components/project/ProjectPage.vue");
const SearchPage = () => import("@/components/search/SearchPage.vue");

// Define functions
async function fetchObjectMetaData() {
    const permissionStore = usePermissionStore();
    const objectMetaDataStore = useObjectMetaDataStore();
    const userStore = useUserStore();

    // Use fetch to get data
    try {
        const response = await fetch("/api/v1/user/initial_data/");
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        
        // Fetch data
        const result = await response.json();

        // Update and process permission store
        permissionStore.$patch({
            permissionData: result.permissions,
        });
        permissionStore.processPermissionData();

        // Update object meta data
        objectMetaDataStore.$patch({
            all_groups: result.all_groups,
            object_status: result.object_status,
            object_types: result.object_types,
            tags: result.tags,
        });

        // Update user
        userStore.$patch({
            id: result.id,
            username: result.username,
            first_name: result.first_name,
            last_name: result.last_name,
            email: result.email,
            profile_picture: result.profile_picture,
            profile_picture_path: result.profile_picture_path,
        });
    } catch (error) {
        const errorStore = useErrorStore();
        errorStore.setError(error);
        await router.push({name: "server-error"});
    }
}

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
        component: ForbiddenPage,
    },
    {
        path: "/not-found",
        name: "not-found",
        meta: {
            destination: "not-found",
        },
        component: NotFoundPage,
    },
    {
        path: "/server-error",
        name: "server-error",
        meta: {
            destination: "server-error",
        },
        component: ServerErrorPage,
    },
    // Fallback page
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
    const documentationStore = useDocumentationStore();
    const objectStore = useObjectStore();

    // Check the user permissions have been loaded
    if (!permissionStore.is_loaded) {
        await fetchObjectMetaData();
    }

    // Clean up store data on route change
    documentationStore.resetDocumentation();
    objectStore.resetObject();

    // Validated the permissions
    if (destination === undefined) {
        next();
    } else if (permissionStore.hasPermission(destination)) {
        next();
    } else {
        next({name: "forbidden"})
    }
});

export {routes};

export default router;
