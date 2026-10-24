// src/components/object_components/link_objects/LinkObjects.spec.ts

import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { createMemoryHistory, createRouter } from "vue-router";
import { defineComponent, h } from "vue";
import {LinkObjects} from ".";
import {AddRelationship} from "./add_relationship";
import {LinkObjectsTable} from "./link_objects_table";
import {SmallLoadingSkeleton} from "@/components/object_components/skeletons";
import { useObjectStore } from "@/stores/object/object.ts";
import i18n from "@/i18n.ts";

// Use a plain router - the app router's guard makes network requests
const router = createRouter({
    history: createMemoryHistory(),
    routes: [{ path: "/:catchAll(.*)*", component: defineComponent({ render: () => h("div") }) }],
});

function mountLinkObjects() {
    return mount(LinkObjects, {
        global: {
            plugins: [
                router,
                i18n
            ],
        },
    });
}

describe("LinkObjects", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        const objectStore = useObjectStore();
        objectStore.destination = "project";
        objectStore.id = 1;
        objectStore.group_list = [
            { id: 1, name: "Group 1", parent_group: null },
            { id: 2, name: "Group 2", parent_group: { id: 1, name: "Group 1"} },
        ];

        vi.spyOn(globalThis, "fetch").mockResolvedValue({
            status: 200,
            json: async () => ([]),
        } as Response);
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    test("mounting component", async () => {
        // LinkObjects component exists
        expect(LinkObjects).toBeTruthy();
    });

    test("renders SmallLoadingSkeleton while the object is loading", async () => {
        // objectStore.is_loaded is false - nothing has been fetched yet
        const wrapper = mountLinkObjects();

        // Flush all promises
        await flushPromises();

        // Check if SmallLoadingSkeleton is rendered instead of the table
        expect(wrapper.findComponent(SmallLoadingSkeleton).exists()).toBe(true);
        expect(wrapper.findComponent(LinkObjectsTable).exists()).toBe(false);
        expect(wrapper.findComponent(AddRelationship).exists()).toBe(false);
        expect(globalThis.fetch).not.toHaveBeenCalled();
    });

    test("renders AddRelationship and LinkObjectsTable once the links are loaded", async () => {
        useObjectStore().is_loaded = true;
        const wrapper = mountLinkObjects();

        // Flush all promises
        await flushPromises();

        expect(wrapper.findComponent(SmallLoadingSkeleton).exists()).toBe(false);
        expect(wrapper.findComponent(AddRelationship).exists()).toBe(true);
        expect(wrapper.findComponent(LinkObjectsTable).exists()).toBe(true);
    });

    test("fetches the link list once the object has loaded", async () => {
        const wrapper = mountLinkObjects();
        await flushPromises();
        expect(globalThis.fetch).not.toHaveBeenCalled();

        // The object finishes loading after the component is mounted
        useObjectStore().is_loaded = true;
        await flushPromises();

        expect(globalThis.fetch).toHaveBeenCalledWith(
            "/api/v1/project/1/link_list/",
            expect.objectContaining({ method: "GET" }),
        );
        expect(wrapper.findComponent(LinkObjectsTable).exists()).toBe(true);
    });

    test("keeps the group list from the object store", async () => {
        useObjectStore().is_loaded = true;
        mountLinkObjects();

        // Flush all promises
        await flushPromises();

        const objectStore = useObjectStore();
        expect(objectStore.group_list.length).toBe(2);
    });
});
