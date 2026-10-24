import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {DocumentComponent} from ".";
import { createPinia, setActivePinia } from "pinia";
import { vi } from "vitest";
import i18n from "@/i18n.ts";
import {createRouter, createWebHistory} from "vue-router";
import {nextTick} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: [],
});

describe("DocumentComponent", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ({
        documents: [],
        folders: [],
        max_upload_size: 10,
      }),
    } as Response);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("mounting component", async () => {
    expect(DocumentComponent).toBeTruthy();
  });

  test("fetches data on mount", async () => {
    const wrapper = mount(DocumentComponent, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    expect(globalThis.fetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.any(Object)
    );
  });

  test("sets isLoaded to true after data fetch", async () => {
    const wrapper = mount(DocumentComponent, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const objectStore = useObjectStore();
    expect(objectStore.is_loaded).toBe(true);
  });

  test("resets object store on unmount", async () => {
    const wrapper = mount(DocumentComponent, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    wrapper.unmount();
    const objectStore = useObjectStore();
    expect(objectStore.is_loaded).toBe(false);
  });
});