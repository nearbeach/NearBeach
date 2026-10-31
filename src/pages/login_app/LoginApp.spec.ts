import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import LoginApp from "./LoginApp.vue";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

describe("LoginApp", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("mounting component", () => {
    // LoginApp component exists
    expect(LoginApp).toBeTruthy();
  });

  test("renders RouterView with transition", async () => {
    const wrapper = mount(LoginApp, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if RouterView exists
    const routerView = wrapper.findComponent({ name: "RouterView" });
    expect(routerView.exists()).toBe(true);

    // Check if Transition exists
    const transition = wrapper.findComponent({ name: "Transition" });
    expect(transition.exists()).toBe(true);

    // Check if Transition has correct props
    expect(transition.attributes("name")).toBe("fade");
    expect(transition.attributes("mode")).toBe("out-in");
  });

  test("renders main element with correct attributes", async () => {
    const wrapper = mount(LoginApp, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if main element exists
    const mainElement = wrapper.find("main");
    expect(mainElement.exists()).toBe(true);

    // Check if main element has correct attributes
    expect(mainElement.attributes("id")).toBe("main");
    expect(mainElement.attributes("aria-labelledby")).toBe("main-title");
    expect(mainElement.attributes("role")).toBe("main");
  });
});