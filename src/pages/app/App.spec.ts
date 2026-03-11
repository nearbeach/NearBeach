// App.spec.ts
import {routes} from "@/router/router.ts";
import {useNavStore} from "@/stores/nav/nav.ts";
import {mount} from "@vue/test-utils";
import {setActivePinia, createPinia} from "pinia";
import {describe, test, expect, beforeEach} from "vitest";
import {createRouter, createWebHistory} from "vue-router";
import App from "./App.vue";
import {usePermissionStore} from "@/stores/permissions/permission.ts";
import {createI18n} from "petite-vue-i18n";
import i18n from "@/i18n.ts";

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});

describe("App", () => {
    const i18n = createI18n({});

    beforeEach(() => {
        setActivePinia(createPinia());
        const permissions = usePermissionStore();
        permissions.isLoaded = true;
        permissions.maximumPermissions = {
            administration_create_permission_set: 0,
            administration_create_user: 0,
            administration_create_group: 0,
            administration_assign_user_to_group: 0,
            kanban_board: 4,
            project: 4,
            request_for_change: 4,
            requirement: 4,
            settings: 4,
            task: 4,
        };
    });

    test("mount component", async () => {
        // Load the basic dashboard page
        await router.push("/");
        await router.isReady();

        // App exists
        expect(App).toBeTruthy();

        // Mount the wrapper
        const wrapper = mount(App, {
            global: {
                plugins: [
                    router,
                    i18n
                ],
            },
        });

        // Test to make sure there is only ONE heading
        const allHeadings = wrapper.findAll("h1");
        expect(allHeadings.length).toBe(1);

        // Test to make sure we have landed on the correct dashboard page
        const heading = allHeadings[0];
        expect(heading?.text()).toBe("Dashboard");
    });
});

describe("App - mobile view", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        Object.defineProperty(window, "innerWidth", {
            writable: true, // Make it writable for mocking
            configurable: true, // Allow redefinition
            value: 375, // Set your desired mock width
        });
    });

    test("mobile viewport - navbar should close automatically", async () => {
        // await page.viewport(375, 812);
        // global.screen.width = 3755;

        // Load the basic dashboard page
        await router.push("/");
        await router.isReady();

        // App exists
        expect(App).toBeTruthy();

        // Make sure the nav is not open
        const nav = useNavStore();
        expect(nav.isNavOpen).toBe(false);

        // Check screen width
        expect(window.innerWidth).toBe(375);
    });
});

describe("App - table view", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        Object.defineProperty(window, "innerWidth", {
            writable: true, // Make it writable for mocking
            configurable: true, // Allow redefinition
            value: 1080, // Set your desired mock width
        });
    });

    test("table viewport - navbar should close automatically", async () => {
        // await page.viewport(375, 812);
        // global.screen.width = 3755;

        // Load the basic dashboard page
        await router.push("/");
        await router.isReady();

        // App exists
        expect(App).toBeTruthy();

        // Make sure the nav is not open
        const nav = useNavStore();
        expect(nav.isNavOpen).toBe(false);

        // Check screen width
        expect(window.innerWidth).toBe(1080);
    });
});

describe("App - desktop view", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        Object.defineProperty(window, "innerWidth", {
            writable: true, // Make it writable for mocking
            configurable: true, // Allow redefinition
            value: 1440, // Set your desired mock width
        });
        const permissions = usePermissionStore();
        permissions.isLoaded = true;
        permissions.maximumPermissions = {
            administration_assign_user_to_group: 0,
            administration_create_group: 0,
            administration_create_permission_set: 0,
            administration_create_user: 0,
            kanban_board: 4,
            project: 4,
            request_for_change: 4,
            requirement: 4,
            settings: 4,
            task: 4,
        };
    });

    test("desktop viewport - navbar should open automatically", async () => {
        // Mount the wrapper
        const wrapper = mount(App, {
            global: {
                plugins: [
                    router,
                    i18n
                ],
            },
        });

        // Load the basic dashboard page
        await router.push("/");
        await router.isReady();

        // App exists
        expect(App).toBeTruthy();

        // Make sure the nav is open
        const nav = useNavStore();
        expect(nav.isNavOpen).toBe(true);

        // Check screen width
        expect(window.innerWidth).toBe(1440);

        // Unmount
        wrapper.unmount();
    });
});
