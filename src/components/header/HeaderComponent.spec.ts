import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import HeaderComponent from "./HeaderComponent.vue";
import { createPinia, setActivePinia } from "pinia";
import App from "@/App.vue";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import { useNavStore } from "@/stores/nav/nav.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("HeaderComponent", () => {
  test("mounting component", async () => {
    // Header component exists
    expect(HeaderComponent).toBeTruthy();
  });
});

describe("HeaderComponent - toggle Menu", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    Object.defineProperty(window, "innerWidth", {
      writable: true, // Make it writable for mocking
      configurable: true, // Allow redefinition
      value: 1440, // Set your desired mock width
    });
  });

  test("menu button exists", async () => {
    const wrapper = mount(HeaderComponent, {});

    // Flush all promises
    await flushPromises();
    await nextTick();

    // There exists only one menu button
    const menu_button = wrapper.findAll(".header--show-menu");
    expect(menu_button.length).toBe(1);
  });

  test("toggle menu closes the menu", async () => {
    // Mount the wrapper
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Default the menu will be open on desktops
    const nav = useNavStore();
    expect(nav.isNavOpen).toBe(true);

    // Click on the menu button
    const menu_button = wrapper.find(".header--show-menu");
    await menu_button.trigger("click");

    // Check the menu is now closed
    await nextTick();
    expect(nav.isNavOpen).toBe(false);
  });

  test("toggle menu opens the menu", async () => {
    // Nav store
    const nav = useNavStore();

    // Mount the wrapper
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Update the isNavOpen to true
    nav.isNavOpen = true;
    expect(nav.isNavOpen).toBe(true);

    // Click on the menu button
    const menu_button = wrapper.find(".header--show-menu");
    await menu_button.trigger("click");

    // Check the menu is now closed
    await nextTick();
    expect(nav.isNavOpen).toBe(false);
  });
});

describe("HeaderComponent - A12Y", () => {
  test("Hidden Visually to be in the document", async () => {
    // Mount the wrapper
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    // Check to see if the <span> exists
    const hidden_visually = wrapper.findAll(".hidden-visually");
    expect(hidden_visually.length).toBe(1);

    // Unmount wrapper
    wrapper.unmount();
  });

  test("closed menu - tells screen reader 'Open Navigation Menu'", async () => {
    // Nav store
    const nav = useNavStore();

    // Mount the wrapper
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    // Update the isNavOpen to false
    nav.isNavOpen = false;
    expect(nav.isNavOpen).toBe(false);

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Click on the menu button
    const hidden_visually = wrapper.find(".hidden-visually");
    expect(hidden_visually.text()).toBe("Open Navigation Menu");

    // Unmount
    wrapper.unmount();
  });

  test("open menu - tells screen reader 'Close Navigation Menu'", async () => {
    // Nav store
    const nav = useNavStore();

    // Mount the wrapper
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    // Update the isNavOpen to true
    nav.isNavOpen = true;
    expect(nav.isNavOpen).toBe(true);

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Click on the menu button
    const hidden_visually = wrapper.find(".hidden-visually");
    expect(hidden_visually.text()).toBe("Close Navigation Menu");

    // Unmount
    wrapper.unmount();
  });
});
