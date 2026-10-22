import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import SearchPage from "./SearchPage.vue";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("SearchPage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders SearchFilter and SearchResults components", async () => {
    const wrapper = mount(SearchPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();

    // Check if SearchFilter component is rendered
    const searchFilter = wrapper.findComponent({ name: "SearchFilter" });
    expect(searchFilter.exists()).toBe(true);

    // Check if SearchResults component is rendered
    const searchResults = wrapper.findComponent({ name: "SearchResults" });
    expect(searchResults.exists()).toBe(true);
  });
});