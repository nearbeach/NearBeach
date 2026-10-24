import {beforeEach, afterEach, describe, expect, test} from "vitest";
import {mount, flushPromises} from "@vue/test-utils";
import {AddRelationship} from ".";
import {createPinia, setActivePinia} from "pinia";
import {useObjectStore} from "@/stores/object/object.ts";
import {vi} from "vitest";
import i18n from "@/i18n.ts";
import {nextTick} from "vue";
import {createRouter, createWebHistory} from "vue-router";

const router = createRouter({
    history: createWebHistory(),
    routes: [],
});

describe("AddRelationship", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        const objectStore = useObjectStore();
        objectStore.id = 1;
        objectStore.destination = "test";
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    test("mounting component", async () => {
        const wrapper = mount(AddRelationship, {
            global: {
                plugins: [router, i18n],
            },
        });

        expect(AddRelationship).toBeTruthy();
    });

    test("fetches data on mount", async () => {
        const mockResponse = {
            object_assignment_id: 1,
            object_id: 2,
            object_title: "Test Object",
            object_status: "active",
            object_type: "test",
            parent_link: "parent",
            link_relationship: "related",
            reverse_relation: false,
        };

        vi.spyOn(globalThis, "fetch").mockResolvedValue({
            status: 200,
            json: async () => [mockResponse],
        } as Response);

        const wrapper = mount(AddRelationship, {
            global: {
                plugins: [router, i18n],
            },
        });

        await flushPromises();
        await nextTick();

        const options = wrapper.findAll("#object-selector option");
        // first option is the blank placeholder
        expect(options).toHaveLength(2);
        expect(options[1].text()).toContain("Test Object");
    });

    test("displays error message on fetch failure", async () => {
        vi.spyOn(globalThis, "fetch").mockResolvedValue({
            status: 500,
            statusText: "Server error",
            json: async () => ({}),
        } as Response);

        const wrapper = mount(AddRelationship, {
            global: {
                plugins: [router, i18n],
            },
        });

        await flushPromises();
        await nextTick();

        // expect(wrapper.vm.errorMessage).toBe("Server error");
        const errorDiv = wrapper.find(".error");
        expect(errorDiv.text()).toBe("Error fetching potential object links: Server error");
    });

    test("button is disabled until an object is selected", async () => {
        const wrapper = mount(AddRelationship, {
            global: {
                plugins: [router, i18n],
            },
        });
        await flushPromises();

        const button = wrapper.find("button");
        expect(button.element.disabled).toBe(true);

        await wrapper.find("#object-selector").setValue("test-2");
        expect(button.element.disabled).toBe(false);
    });
});