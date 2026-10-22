import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import SearchCard from "./SearchCard.vue";
import { createRouter, createMemoryHistory } from "vue-router";
import { nextTick } from "vue";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    {
      path: "/:objectType/:id",
      component: defineComponent({ render: () => h("div") }),
    },
  ],
});

describe("SearchCard", () => {
  beforeEach(async () => {
    await router.push("/test/123");
    await router.isReady();
  });

  test("renders with correct props", async () => {
    const wrapper = mount(SearchCard, {
      props: {
        higherOrderStatus: "normal",
        id: 123,
        objectType: "test",
        status: "active",
        title: "Test Object",
      },
      global: {
        plugins: [router],
      },
    });

    // Check ObjectIdTag
    const objectIdTag = wrapper.findComponent(ObjectIdTag);
    expect(objectIdTag.exists()).toBe(true);
    expect(objectIdTag.props("id")).toBe(123);
    expect(objectIdTag.props("objectType")).toBe("test");

    // Check ObjectStatusTag
    const objectStatusTag = wrapper.findComponent(ObjectStatusTag);
    expect(objectStatusTag.exists()).toBe(true);
    expect(objectStatusTag.props("higherOrderStatus")).toBe("normal");
    expect(objectStatusTag.props("status")).toBe("active");

    // Check RouterLink
    const routerLink = wrapper.findComponent(RouterLink);
    expect(routerLink.exists()).toBe(true);
    expect(routerLink.props("to")).toBe("/test/123");
    expect(routerLink.text()).toBe("Test Object");
  });

  test("renders with default status", async () => {
    const wrapper = mount(SearchCard, {
      props: {
        higherOrderStatus: "normal",
        id: 123,
        objectType: "test",
        title: "Test Object",
      },
      global: {
        plugins: [router],
      },
    });

    // Check ObjectStatusTag
    const objectStatusTag = wrapper.findComponent(ObjectStatusTag);
    expect(objectStatusTag.exists()).toBe(true);
    expect(objectStatusTag.props("higherOrderStatus")).toBe("normal");
    expect(objectStatusTag.props("status")).toBe("");
  });

  test("renders with different higherOrderStatus", async () => {
    const wrapper = mount(SearchCard, {
      props: {
        higherOrderStatus: "blocked",
        id: 123,
        objectType: "test",
        status: "active",
        title: "Test Object",
      },
      global: {
        plugins: [router],
      },
    });

    // Check ObjectStatusTag
    const objectStatusTag = wrapper.findComponent(ObjectStatusTag);
    expect(objectStatusTag.exists()).toBe(true);
    expect(objectStatusTag.props("higherOrderStatus")).toBe("blocked");
    expect(objectStatusTag.props("status")).toBe("active");
  });
});