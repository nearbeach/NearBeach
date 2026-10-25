import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {DocumentComponent} from ".";
import { createPinia, setActivePinia } from "pinia";
import { vi } from "vitest";
import i18n from "@/i18n.ts";
import {createRouter, createWebHistory} from "vue-router";
import {nextTick} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";

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

  test("does not fetch data until the object has loaded", async () => {
    mount(DocumentComponent, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    expect(globalThis.fetch).not.toHaveBeenCalled();
  });

  test("fetches data on mount when the object has loaded", async () => {
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 1;
    objectStore.is_loaded = true;

    mount(DocumentComponent, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/v1/project/1/documents/",
      expect.any(Object)
    );
  });

  test("stores the documentation once the object finishes loading", async () => {
    mount(DocumentComponent, {
      global: {
        plugins: [router, i18n],
      },
    });

    // The object finishes loading after the component is mounted
    useObjectStore().is_loaded = true;
    await flushPromises();
    await nextTick();

    const documentationStore = useDocumentationStore();
    expect(documentationStore.isDocumentationLoaded).toBe(true);
    expect(documentationStore.maxUploadSize).toBe(10);
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

describe("DocumentComponent - already loaded", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("does not fetch again when the documentation is already loaded", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    useDocumentationStore().isDocumentationLoaded = true;
    const objectStore = useObjectStore();
    objectStore.is_loaded = true;

    mount(DocumentComponent, { global: { plugins: [router, i18n] } });
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
