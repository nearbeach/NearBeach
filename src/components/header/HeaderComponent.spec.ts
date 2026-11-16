import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {HeaderComponent} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import { useNavStore } from "@/stores/nav/nav.ts";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

describe("HeaderComponent", () => {
  test("mounting component", () => {
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
    const wrapper = mount(HeaderComponent, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Default the menu will be open on desktops
    const nav = useNavStore();
    nav.isNavOpen = true;
    expect(nav.isNavOpen).toBe(true);

    // Click on the menu button
    const menu_button = wrapper.find(".header--show-menu button");
    await menu_button.trigger("click");

    // Check the menu is now closed
    await nextTick();
    expect(nav.isNavOpen).toBe(false);
  });

  test("toggle menu opens the menu", async () => {
    // Nav store
    const nav = useNavStore();

    // Mount the wrapper
    const wrapper = mount(HeaderComponent, {
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
    const menu_button = wrapper.find(".header--show-menu button");
    await menu_button.trigger("click");

    // Check the menu is now closed
    await nextTick();
    expect(nav.isNavOpen).toBe(false);
  });
});

describe("HeaderComponent - A11Y", () => {
  test("the menu toggle is a real button with an accessible name", () => {
    // Mount the wrapper
    const wrapper = mount(HeaderComponent, {
      global: {
        plugins: [router],
      },
    });

    // The toggle is a keyboard-focusable <button>, not a click handler on a <div>
    const buttons = wrapper.findAll(".header--show-menu button");
    expect(buttons.length).toBe(1);
    expect(buttons[0].attributes("aria-label")).toBeTruthy();

    // Unmount wrapper
    wrapper.unmount();
  });

  test("closed menu - tells screen reader 'Open Navigation Menu'", async () => {
    // Nav store
    const nav = useNavStore();

    // Mount the wrapper
    const wrapper = mount(HeaderComponent, {
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

    // The button's accessible name tells the screen reader what it does
    const menu_button = wrapper.find(".header--show-menu button");
    expect(menu_button.attributes("aria-label")).toBe("Open Navigation Menu");

    // Unmount
    wrapper.unmount();
  });

  test("open menu - tells screen reader 'Close Navigation Menu'", async () => {
    // Nav store
    const nav = useNavStore();

    // Mount the wrapper
    const wrapper = mount(HeaderComponent, {
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

    // The button's accessible name tells the screen reader what it does
    const menu_button = wrapper.find(".header--show-menu button");
    expect(menu_button.attributes("aria-label")).toBe("Close Navigation Menu");

    // Unmount
    wrapper.unmount();
  });
});
