import {beforeEach, afterEach, describe, expect, test} from "vitest";
import {mount, flushPromises} from "@vue/test-utils";
import {AddRelationship} from ".";
import {createPinia, setActivePinia} from "pinia";
import {useObjectStore} from "@/stores/object/object.ts";
import {vi} from "vitest";
import i18n from "@/i18n.ts";
import {createRouter, createWebHistory} from "vue-router";

const router = createRouter({
    history: createWebHistory(),
    routes: [],
});

const mockOption = {
    object_assignment_id: 1,
    object_id: 2,
    object_title: "Test Object",
    object_status: "active",
    object_type: "test",
    parent_link: "parent",
    link_relationship: "related",
    reverse_relation: false,
};

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

    test("mounting component", () => {
        mount(AddRelationship, {
            global: {
                plugins: [router, i18n],
            },
        });

        expect(AddRelationship).toBeTruthy();
    });

    test("renders the object options passed in", async () => {
        const wrapper = mount(AddRelationship, {
            props: {objectOptions: [mockOption]},
            global: {
                plugins: [router, i18n],
            },
        });

        const options = wrapper.findAll("#object-selector option");
        // first option is the blank placeholder
        expect(options).toHaveLength(2);
        expect(options[1].text()).toContain("Test Object");
    });

    test("button is disabled until an object is selected", async () => {
        const wrapper = mount(AddRelationship, {
            props: {objectOptions: [mockOption]},
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

describe("AddRelationship - creating a link", () => {
  const options = [
    { object_assignment_id: 0, object_id: 5, object_title: "Five", object_status: "Open", object_type: "task", parent_link: "", link_relationship: "", reverse_relation: false },
  ];

  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.id = 1;
    objectStore.destination = "project";
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  async function mountReady() {
    const wrapper = mount(AddRelationship, { props: { objectOptions: options }, global: { plugins: [router, i18n] } });
    await flushPromises();
    return wrapper;
  }

  test("emits the chosen object and relationship", async () => {
    const wrapper = await mountReady();

    await wrapper.find("#relationship-type").setValue("blocking");
    await wrapper.find("#object-selector").setValue("task-5");
    await wrapper.find("button").trigger("click");

    expect(wrapper.emitted("createObjectLink")).toEqual([
      [{ objectSelectorModel: "task-5", relationshipModel: "blocking" }],
    ]);
  });

  test("emits nothing while no object is chosen", async () => {
    const wrapper = await mountReady();

    // The button is disabled, so call the handler directly
    (wrapper.vm as unknown as { createObjectLink: () => void }).createObjectLink();

    expect(wrapper.emitted("createObjectLink")).toBeUndefined();
  });
});
