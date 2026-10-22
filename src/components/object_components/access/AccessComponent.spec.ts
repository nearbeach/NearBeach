import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import AccessComponent from "./AccessComponent.vue";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import { useNavStore } from "@/stores/nav/nav.ts";
import { WlkCard } from "whelk-ui";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("AccessComponent", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders WlkCard component", async () => {
    const wrapper = mount(AccessComponent, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if WlkCard component exists
    const wlkCard = wrapper.findComponent(WlkCard);
    expect(wlkCard.exists()).toBe(true);
  });

  test("renders GroupAccess component", async () => {
    const wrapper = mount(AccessComponent, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if GroupAccess component exists
    const groupAccess = wrapper.findComponent({ name: "GroupAccess" });
    expect(groupAccess.exists()).toBe(true);
  });

  test("renders AssignedUsers component", async () => {
    const wrapper = mount(AccessComponent, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if AssignedUsers component exists
    const assignedUsers = wrapper.findComponent({ name: "AssignedUsers" });
    expect(assignedUsers.exists()).toBe(true);
  });
});