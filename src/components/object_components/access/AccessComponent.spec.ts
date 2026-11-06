import { beforeEach, describe, expect, test } from "vitest";
import i18n from "@/i18n.ts";
import { mount, flushPromises } from "@vue/test-utils";
import {AccessComponent} from ".";
import { createPinia, setActivePinia } from "pinia";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import { WlkCard } from "whelk-ui";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

describe("AccessComponent", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    usePermissionStore().currentObjectPermissions.currentObject = 2;
  });

  test("renders WlkCard component", async () => {
    const wrapper = mount(AccessComponent, {
      global: {
        plugins: [router, i18n],
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
        plugins: [router, i18n],
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
        plugins: [router, i18n],
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