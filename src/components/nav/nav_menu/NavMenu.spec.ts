import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {NavMenu} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import { usePermissionStore } from "@/stores/permission.ts";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("NavMenu", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("mounting component", async () => {
    // NavMenu component exists
    expect(NavMenu).toBeTruthy();
  });

  test("renders dashboard menu item", async () => {
    const wrapper = mount(NavMenu, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if dashboard menu item exists
    const dashboardItem = wrapper.find("a.dashboard");
    expect(dashboardItem.exists()).toBe(true);
  });

  test("renders settings menu item", async () => {
    const wrapper = mount(NavMenu, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if settings menu item exists
    const settingsItem = wrapper.find("a.settings");
    expect(settingsItem.exists()).toBe(true);
  });

  test("does not render admin menu item if user has no admin permissions", async () => {
    const permissionStore = usePermissionStore();
    permissionStore.processPermissionData();

    const wrapper = mount(NavMenu, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if admin menu item does not exist
    const adminItem = wrapper.find("a.admin");
    expect(adminItem.exists()).toBe(false);
  });

  test("renders admin menu item if user has admin permissions", async () => {
    const permissionStore = usePermissionStore();
    permissionStore.maximumPermissions.administration_assign_user_to_group = 1;
    permissionStore.processPermissionData();

    const wrapper = mount(NavMenu, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if admin menu item exists
    const adminItem = wrapper.find("a.admin");
    expect(adminItem.exists()).toBe(true);
  });
});