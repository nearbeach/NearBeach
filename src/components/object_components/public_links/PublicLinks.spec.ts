import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useObjectStore } from "@/stores/object/object.ts";
import {PublicLinks} from ".";
import { vi } from "vitest";
import {nextTick} from "vue";
import i18n from "@/i18n.ts";

function mountPublicLinks() {
  return mount(PublicLinks, {
    global: {
      plugins: [i18n],
    },
  });
}

describe("PublicLinks", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.is_loaded = true;
    objectStore.destination = "test-destination";
    objectStore.id = 123;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("mounting component", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ([]),
    } as Response);

    const wrapper = mountPublicLinks();
    await flushPromises();

    expect(wrapper.exists()).toBe(true);
    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/v1/test-destination/123/public_link/",
      expect.any(Object),
    );
  });

  test("does not render the links table when the fetch fails", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 500,
      json: async () => ({ error: "Server error" }),
    } as Response);

    const wrapper = mountPublicLinks();

    await flushPromises();
    await nextTick();

    // The component keeps the error, but does not display it yet
    expect(wrapper.find("table").exists()).toBe(false);
  });
});
