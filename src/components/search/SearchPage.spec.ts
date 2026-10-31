import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {SearchPage} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

describe("SearchPage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());

    // SearchFilter fetches results on mount - there is no backend in the tests
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: () => Promise.resolve({ previous: null, next: null, results: [] }),
    } as Response);
  });

  afterEach(() => {
    vi.restoreAllMocks();
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