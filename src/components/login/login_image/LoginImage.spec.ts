import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import LoginImage from "./LoginImage.vue";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("LoginImage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("image is not displayed on small screens", async () => {
    // Mock innerWidth to be less than medium screen size
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 768, // Example small screen width
    });

    // Mount the component
    const wrapper = mount(LoginImage, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check that the login image is not visible
    const loginImage = wrapper.find(".login-image");
    expect(loginImage.isVisible()).toBe(false);
  });

  test("image is displayed on medium screens", async () => {
    // Mock innerWidth to be a medium screen size
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1440, // Example medium screen width
    });

    // Mount the component
    const wrapper = mount(LoginImage, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check that the login image is visible
    const loginImage = wrapper.find(".login-image");
    expect(loginImage.isVisible()).toBe(true);
  });
});