import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {NavSettingMenu} from ".";
import { createPinia, setActivePinia } from "pinia";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import i18n from "@/i18n.ts";

describe("NavSettingMenu", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("logout menu item has correct aria-label", async () => {
    const wrapper = mount(NavSettingMenu, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const logoutMenuItem = wrapper.findComponent({ name: "NavMenuItem" }).findComponent({ name: "LogOut" }).parentComponent();
    expect(logoutMenuItem.attributes("aria-label")).toBe("Logout");
  });

  test("settings menu item has correct aria-label", async () => {
    const permissionStore = usePermissionStore();
    permissionStore.hasAdministrationPermission = true;

    const wrapper = mount(NavSettingMenu, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const settingsMenuItem = wrapper.findComponent({ name: "NavMenuItem" }).findComponent({ name: "Cog" }).parentComponent();
    expect(settingsMenuItem.attributes("aria-label")).toBe("Settings");
  });
});