// src/components/object_components/link_objects/LinkObjects.spec.ts

import { beforeEach, describe, expect, test, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import {LinkObjects} from ".";
import { useObjectStore } from "@/stores/object/object.ts";
import i18n from "@/i18n.ts";
import router from "@/router/router.ts";

describe("LinkObjects", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        const objectStore = useObjectStore();
        objectStore.group_list = [
            { id: 1, name: "Group 1", parent_group: null },
            { id: 2, name: "Group 2", parent_group: { id: 1, name: "Group 1"} },
        ];
    });

    test("mounting component", async () => {
        // LinkObjects component exists
        expect(LinkObjects).toBeTruthy();
    });

    test("renders SmallLoadingSkeleton when loading", async () => {
        const wrapper = mount(LinkObjects, {
            global: {
                plugins: [
                    router,
                    i18n
                ],
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
                plugins: [
                    router,
                    i18n
                ],
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
                plugins: [
                    router,
                    i18n
                ],
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
                plugins: [
                    router,
                    i18n
                ],
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
});