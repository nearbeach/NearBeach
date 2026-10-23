import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import { defineComponent, h } from "vue";
import {ObjectIdTag} from ".";
import shortObjectType from "@/utils/dictionary/ShortObjectDictionary.ts";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    {
      path: "/:objectType/:id",
      component: defineComponent({ render: () => h("div") }),
    },
  ],
});

describe("ObjectIdTag", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders the correct link text", async () => {
    const wrapper = mount(ObjectIdTag, {
      props: {
        id: 123,
        objectType: "customer",
      },
      global: {
        plugins: [router],
      },
    });

    await router.push("/customer/123");
    await router.isReady();

    const link = wrapper.find("a");
    expect(link.text()).toBe("Cust-123");
  });

  test("renders the correct class based on object type", async () => {
    const wrapper = mount(ObjectIdTag, {
      props: {
        id: 456,
        objectType: "kanban_board",
      },
      global: {
        plugins: [router],
      },
    });

    await router.push("/kanban_board/456");
    await router.isReady();

    const span = wrapper.find("span");
    expect(span.classes()).toContain("kanban_board");
  });

  test("emits the correct route when clicked", async () => {
    const wrapper = mount(ObjectIdTag, {
      props: {
        id: 789,
        objectType: "organisation",
      },
      global: {
        plugins: [router],
      },
    });

    await router.push("/organisation/789");
    await router.isReady();

    const link = wrapper.find("a");
    await link.trigger("click");

    expect(router.currentRoute.value.path).toBe("/organisation/789");
  });

  test("validator accepts valid object types", () => {
    expect(shortObjectType["customer"]).toBe("Cust");
    expect(shortObjectType["kanban_board"]).toBe("Kan");
    expect(shortObjectType["kanban_card"]).toBe("Card");
    expect(shortObjectType["organisation"]).toBe("Org");
    expect(shortObjectType["request_for_change"]).toBe("RFC");
    expect(shortObjectType["requirement"]).toBe("Req");
    expect(shortObjectType["requirement_item"]).toBe("Item");
    expect(shortObjectType["project"]).toBe("Pro");
    expect(shortObjectType["task"]).toBe("Task");
  });

  test("validator rejects invalid object types", () => {
    expect(shortObjectType["invalidType"]).toBeUndefined();
  });
});