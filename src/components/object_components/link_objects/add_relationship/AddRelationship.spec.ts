import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises, nextTick } from "@vue/test-utils";
import AddRelationship from "./AddRelationship.vue";
import { createPinia, setActivePinia } from "pinia";
import { useObjectStore } from "@/stores/object.ts";
import { vi } from "vitest";
import i18n from "@/i18n.ts";

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

    expect(wrapper.vm.objectLinks).toEqual([mockResponse]);
  });

  test("displays error message on fetch failure", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 500,
      json: async () => ({ error: "Server error" }),
    } as Response);

    const wrapper = mount(AddRelationship, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    expect(wrapper.vm.errorMessage).toBe("Server error");
  });

  test("button is disabled when no object links", async () => {
    const wrapper = mount(AddRelationship, {
      global: {
        plugins: [router, i18n],
      },
    });

    const button = wrapper.find("button");
    expect(button.attributes("disabled")).toBe("disabled");
  });

  test("button is enabled when object links exist", async () => {
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

    const button = wrapper.find("button");
    expect(button.attributes("disabled")).toBeUndefined();
  });
});