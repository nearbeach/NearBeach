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

describe("LinkObjects - managing links", () => {
    const links = [
        { object_assignment_id: 10, object_id: 1, object_title: "One", object_status: "Open", object_type: "task", parent_link: "", link_relationship: "relates", reverse_relation: false },
        { object_assignment_id: 11, object_id: 2, object_title: "Two", object_status: "Open", object_type: "project", parent_link: "", link_relationship: "block", reverse_relation: true },
    ];

    function mockFetch(responses: Record<string, unknown> = {}) {
        return vi.spyOn(globalThis, "fetch").mockImplementation(async (_url, init) => {
            const method = init?.method ?? "GET";
            const body = method in responses ? responses[method] : (method === "GET" ? links : {});
            return { status: 200, json: async () => structuredClone(body) } as Response;
        });
    }

    async function mountLoaded(responses: Record<string, unknown> = {}) {
        const fetchSpy = mockFetch(responses);
        const wrapper = mountLinkObjects();
        await flushPromises();
        return { wrapper, fetchSpy };
    }

    const listOf = (wrapper: ReturnType<typeof mountLinkObjects>) =>
        wrapper.findComponent(LinkObjectsTable).props("objectLinkList") as typeof links;

    beforeEach(() => {
        setActivePinia(createPinia());
        const objectStore = useObjectStore();
        objectStore.destination = "project";
        objectStore.id = 1;
        objectStore.is_loaded = true;
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    test("passes the loaded links to the table", async () => {
        const { wrapper } = await mountLoaded();

        expect(listOf(wrapper).map((l) => l.object_title)).toEqual(["One", "Two"]);
    });

    test("a failed load leaves the skeleton showing", async () => {
        vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
        const wrapper = mountLinkObjects();
        await flushPromises();

        expect(wrapper.findComponent(SmallLoadingSkeleton).exists()).toBe(true);
    });

    test("creating a link splits the barcode, posts it and appends the result", async () => {
        const created = { ...links[0], object_assignment_id: 12, object_title: "Three" };
        const { wrapper, fetchSpy } = await mountLoaded({ POST: created });

        wrapper.findComponent(AddRelationship).vm.$emit("createObjectLink", {
            relationshipModel: "blocking",
            objectSelectorModel: "task-33",
        });
        await flushPromises();

        const post = fetchSpy.mock.calls.find(([, i]) => i?.method === "POST")!;
        expect(post[0]).toBe("/api/v1/project/1/link_list/");
        expect(JSON.parse(post[1]?.body as string)).toEqual({
            object_type: "task",
            object_id: "33",
            object_relation: "blocking",
        });
        expect(listOf(wrapper).map((l) => l.object_title)).toEqual(["One", "Two", "Three"]);
    });

    test("a failed create adds nothing", async () => {
        const { wrapper, fetchSpy } = await mountLoaded();
        fetchSpy.mockRejectedValueOnce(new Error("offline"));

        wrapper.findComponent(AddRelationship).vm.$emit("createObjectLink", {
            relationshipModel: "relates",
            objectSelectorModel: "task-33",
        });
        await flushPromises();

        expect(listOf(wrapper)).toHaveLength(2);
    });

    test("deleting removes the link by index and calls DELETE", async () => {
        const { wrapper, fetchSpy } = await mountLoaded();

        wrapper.findComponent(LinkObjectsTable).vm.$emit("deleteObjectLink", {
            object_assignment_id: 10,
            index: 0,
        });
        await flushPromises();

        const del = fetchSpy.mock.calls.find(([, i]) => i?.method === "DELETE")!;
        expect(del[0]).toBe("/api/v1/project/1/link_list/10/");
        expect(listOf(wrapper).map((l) => l.object_assignment_id)).toEqual([11]);
    });

    test("a failed delete request does not throw", async () => {
        const { wrapper, fetchSpy } = await mountLoaded();
        fetchSpy.mockRejectedValueOnce(new Error("offline"));

        wrapper.findComponent(LinkObjectsTable).vm.$emit("deleteObjectLink", {
            object_assignment_id: 10,
            index: 0,
        });
        await flushPromises();

        expect(wrapper.exists()).toBe(true);
    });

    test("updateRelationship changes the relationship on that row", async () => {
        const { wrapper } = await mountLoaded();

        wrapper.findComponent(LinkObjectsTable).vm.$emit("updateRelationship", {
            index: 1,
            link_relationship: "duplicate",
        });
        await flushPromises();

        expect(listOf(wrapper)[1].link_relationship).toBe("duplicate");
        expect(listOf(wrapper)[0].link_relationship).toBe("relates");
    });

    test("updateRelationship ignores an index that does not exist", async () => {
        const { wrapper } = await mountLoaded();

        wrapper.findComponent(LinkObjectsTable).vm.$emit("updateRelationship", {
            index: 9,
            link_relationship: "duplicate",
        });
        await flushPromises();

        expect(listOf(wrapper)).toHaveLength(2);
    });
});
