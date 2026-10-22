// src/components/object_components/link_objects/LinkObjects.spec.ts

import { beforeEach, describe, expect, test, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import LinkObjects from "./LinkObjects.vue";
import { useObjectStore } from "@/stores/object/object.ts";
import { getCsrfToken } from "@/composables/getCsrfToken.ts";

describe("LinkObjects", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        const objectStore = useObjectStore();
        objectStore.group_list = [
            { id: 1, title: "Group 1" },
            { id: 2, title: "Group 2" },
        ];
    });

    test("mounting component", async () => {
        // LinkObjects component exists
        expect(LinkObjects).toBeTruthy();
    });

    test("renders SmallLoadingSkeleton when loading", async () => {
        const wrapper = mount(LinkObjects, {
            global: {
                mocks: {
                    $t: (key: string) => key, // Mock i18n
                },
            },
        });

        // Flush all promises
        await flushPromises();

        // Check if SmallLoadingSkeleton is rendered
        const smallLoadingSkeleton = wrapper.findComponent({ name: "SmallLoadingSkeleton" });
        expect(smallLoadingSkeleton.exists()).toBe(true);
    });

    test("renders AddRelationship when not loading", async () => {
        const wrapper = mount(LinkObjects, {
            global: {
                mocks: {
                    $t: (key: string) => key, // Mock i18n
                },
            },
        });

        // Flush all promises
        await flushPromises();

        // Check if AddRelationship is rendered
        const addRelationship = wrapper.findComponent({ name: "AddRelationship" });
        expect(addRelationship.exists()).toBe(true);
    });

    test("renders LinkObjectsTable when not loading", async () => {
        const wrapper = mount(LinkObjects, {
            global: {
                mocks: {
                    $t: (key: string) => key, // Mock i18n
                },
            },
        });

        // Flush all promises
        await flushPromises();

        // Check if LinkObjectsTable is rendered
        const linkObjectsTable = wrapper.findComponent({ name: "LinkObjectsTable" });
        expect(linkObjectsTable.exists()).toBe(true);
    });

    test("fetches group list on mount", async () => {
        const wrapper = mount(LinkObjects, {
            global: {
                mocks: {
                    $t: (key: string) => key, // Mock i18n
                },
            },
        });

        // Flush all promises
        await flushPromises();

        // Check if group list is fetched
        const objectStore = useObjectStore();
        expect(objectStore.group_list.length).toBe(2);
    });

    test("calls fetch with correct URL", async () => {
        const mockFetch = vi.spyOn(globalThis, "fetch").mockResolvedValue({
            status: 200,
            json: async () => ({
                group_list: [
                    { id: 1, title: "Group 1" },
                    { id: 2, title: "Group 2" },
                ],
            }),
        });

        const wrapper = mount(LinkObjects, {
            global: {
                mocks: {
                    $t: (key: string) => key, // Mock i18n
                },
            },
        });

        // Flush all promises
        await flushPromises();

        // Check if fetch is called with correct URL
        expect(mockFetch).toHaveBeenCalledWith("/api/object/1234567890/relationship/", {
            method: "GET",
            headers: {
                "X-CSRFToken": getCsrfToken(),
                "Content-Type": "application/json",
            },
        });

        // Restore fetch
        vi.restoreAllMocks();
    });
});