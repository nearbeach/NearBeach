import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useErrorStore } from "@/stores/error/error.ts";
import {ErrorModal} from ".";
import i18n from "@/i18n.ts";
import { nextTick } from "vue";

describe("ErrorModal", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders modal when showErrorModal is true", async () => {
    const errorStore = useErrorStore();
    errorStore.showErrorModal = true;
    errorStore.message = "Test error message";

    await nextTick();

    const wrapper = mount(ErrorModal, {
      global: {
        plugins: [i18n],
        stubs: {
          teleport: true,
        }
      },
    });

    await flushPromises();
    await nextTick();

    console.log(wrapper);

    expect(wrapper.find(".wlk-modal").classes()).toContain("open");
    expect(wrapper.text()).toContain("Test error message");
  });

  test("does not render modal when showErrorModal is false", async () => {
    const errorStore = useErrorStore();
    errorStore.showErrorModal = false;

    const wrapper = mount(ErrorModal, {
      global: {
        plugins: [i18n],
        stubs: {
          teleport: true,
        }
      },
    });

    await flushPromises();
    await nextTick();

    expect(wrapper.find(".wlk-modal").classes()).not.toContain("open");
  });

  test("closes modal when close button is clicked", async () => {
    const errorStore = useErrorStore();
    errorStore.showErrorModal = true;

    const wrapper = mount(ErrorModal, {
      global: {
        plugins: [i18n],
        stubs: {
          teleport: true,
        }
      },
    });

    await flushPromises();
    await nextTick();

    // Close the button
    const closeButton = wrapper.find(".info.compact");
    await closeButton.trigger("click");

    await flushPromises();
    await nextTick();

    expect(errorStore.showErrorModal).toBe(false);
  });
});