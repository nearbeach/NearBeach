import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useObjectStore } from "@/stores/object/object.ts";
import {PublicLinks} from ".";
import { vi } from "vitest";
import {nextTick} from "vue";

const i18n = {
  install: () => {},
};

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
    const wrapper = mount(PublicLinks, {
      global: {
        plugins: [i18n],
      },
    });

    expect(wrapper.exists()).toBe(true);
  });

  test("displays error message on fetch failure", async () => {
    const mockFetchResponse = {
      status: 500,
      json: async () => ({ error: "Server error" }),
    };

    vi.spyOn(globalThis, "fetch").mockResolvedValue(mockFetchResponse as Response);

    const wrapper = mount(PublicLinks, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    expect(fetch).toHaveBeenCalledWith(
      "/api/test-destination/123/public-links/"
    );

    const errorMessage = wrapper.find(".error-message");
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.text()).toBe("Server error");
  });
});