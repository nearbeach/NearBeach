import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import SearchHeader from "./SearchHeader.vue";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("SearchHeader", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders title in English", async () => {
    const wrapper = mount(SearchHeader, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const title = wrapper.find(".object-title");
    expect(title.text()).toBe("Title");
  });

  test("renders status in English", async () => {
    const wrapper = mount(SearchHeader, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const status = wrapper.find(".object-status-tag");
    expect(status.text()).toBe("Status");
  });

  test("renders title in Japanese", async () => {
    const wrapper = mount(SearchHeader, {
      global: {
        plugins: [i18n],
      },
    });

    // Change locale to Japanese
    wrapper.vm.$i18n.locale = "ja";

    await flushPromises();
    await nextTick();

    const title = wrapper.find(".object-title");
    expect(title.text()).toBe("タイトル");
  });

  test("renders status in Japanese", async () => {
    const wrapper = mount(SearchHeader, {
      global: {
        plugins: [i18n],
      },
    });

    // Change locale to Japanese
    wrapper.vm.$i18n.locale = "ja";

    await flushPromises();
    await nextTick();

    const status = wrapper.find(".object-status-tag");
    expect(status.text()).toBe("状態");
  });
});