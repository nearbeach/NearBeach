import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {NavMenu} from ".";
import {NavMenuItem} from "./nav_menu_item";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

async function mountNavMenu() {
  const wrapper = mount(NavMenu, {
    global: {
      plugins: [router, i18n],
    },
  });

  // Flush all promises
  await flushPromises();
  await nextTick();

  return wrapper;
}

function getDestinations(wrapper: Awaited<ReturnType<typeof mountNavMenu>>) {
  return wrapper.findAllComponents(NavMenuItem).map((item) => item.props("destination"));
}

describe("NavMenu", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("mounting component", async () => {
    // NavMenu component exists
    expect(NavMenu).toBeTruthy();
  });

  test("renders dashboard menu item", async () => {
    const wrapper = await mountNavMenu();

    // Check if dashboard menu item exists and links to the root
    const dashboardItem = wrapper.findAllComponents(NavMenuItem).at(0);
    expect(dashboardItem?.props("destination")).toBe("dashboard");
    expect(dashboardItem?.find("a").attributes("href")).toBe("/");
  });

  test("only renders the dashboard when the user has no permissions", async () => {
    const wrapper = await mountNavMenu();

    expect(getDestinations(wrapper)).toEqual(["dashboard"]);
  });

  test("renders menu items for the objects the user has permissions for", async () => {
    const permissionStore = usePermissionStore();
    permissionStore.maximumPermissions.kanban_board = 1;
    permissionStore.maximumPermissions.project = 1;

    const wrapper = await mountNavMenu();

    expect(getDestinations(wrapper)).toEqual(["dashboard", "kanban_board", "project"]);
  });

  test("renders create new link only when the user can create the object", async () => {
    const permissionStore = usePermissionStore();
    permissionStore.maximumPermissions.project = 3;
    permissionStore.maximumPermissions.task = 2;

    const wrapper = await mountNavMenu();

    const items = wrapper.findAllComponents(NavMenuItem);
    const projectItem = items.find((item) => item.props("destination") === "project");
    const taskItem = items.find((item) => item.props("destination") === "task");

    expect(projectItem?.find(".nav-bar--menu--item-new").attributes("href")).toBe("/project/new");
    expect(taskItem?.find(".nav-bar--menu--item-new").exists()).toBe(false);
  });
});

describe("NavMenu - creating objects", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("a permission that is not a number gives no create link", async () => {
    const wrapper = await mountNavMenu();
    const canUserCreate = (wrapper.vm as unknown as { canUserCreate: (object: string) => string }).canUserCreate;

    expect(canUserCreate("not_a_permission")).toBe("");
  });

  test("create links need permission level 3", async () => {
    const wrapper = await mountNavMenu();
    const canUserCreate = (wrapper.vm as unknown as { canUserCreate: (object: string) => string }).canUserCreate;
    const permissionStore = usePermissionStore();

    permissionStore.maximumPermissions.project = 2;
    expect(canUserCreate("project")).toBe("");

    permissionStore.maximumPermissions.project = 3;
    expect(canUserCreate("project")).toBe("/project/new");
  });
});
