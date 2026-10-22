import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { defineComponent, h } from "vue";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import AppStructure from "./AppStructure.vue";
import { useNavStore } from "@/stores/nav/nav.ts";
import { nextTick } from "vue";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    {
      path: "/",
      component: defineComponent({ render: () => h("div") }),
    },
  ],
});

describe("AppStructure", () => {
  beforeEach(async () => {
    setActivePinia(createPinia());
    await router.push("/");
    await router.isReady();
  });

  test("main class is set based on nav state", async () => {
    const wrapper = mount(AppStructure, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Initially, nav is closed
    const main = wrapper.find("#main");
    expect(main.classes()).toContain("main");
    expect(main.classes()).not.toContain("nav-open");

    // Open nav
    const navStore = useNavStore();
    navStore.isNavOpen = true;
    await nextTick();

    expect(main.classes()).toContain("nav-open");
  });

  test("main class is set based on window width", async () => {
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1440,
    });

    const wrapper = mount(AppStructure, {
      global: {
        plugins: [router, i18n],
      },
    });

    // On desktop, nav should be open
    const main = wrapper.find("#main");
    expect(main.classes()).toContain("nav-open");

    // On mobile, nav should be closed
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1024,
    });

    await nextTick();
    expect(main.classes()).toContain("main");
    expect(main.classes()).not.toContain("nav-open");
  });
});