import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useErrorStore } from "@/stores/error/error.ts";
import ErrorModal from "./ErrorModal.vue";
import i18n from "@/i18n.ts";

describe("ErrorModal", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders modal when showErrorModal is true", async () => {
    const errorStore = useErrorStore();
    errorStore.showErrorModal = true;
    errorStore.message = "Test error message";

    const wrapper = mount(ErrorModal, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    expect(wrapper.find(".wlk-modal").classes()).toContain("open");
    expect(wrapper.text()).toContain("Test error message");
  });

  test("does not render modal when showErrorModal is false", async () => {
    const errorStore = useErrorStore();
    errorStore.showErrorModal = false;

    const wrapper = mount(ErrorModal, {
      global: {
        plugins: [i18n],
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
      },
    });

    await flushPromises();
    await nextTick();

    const closeButton = wrapper.find(".info.compact");
    await closeButton.trigger("click");

    await flushPromises();
    await nextTick();

    expect(errorStore.showErrorModal).toBe(false);
  });

  test("disables close button for 1 second after modal opens", async () => {
    const errorStore = useErrorStore();
    errorStore.showErrorModal = true;

    const wrapper = mount(ErrorModal, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const closeButton = wrapper.find(".info.compact");
    expect(closeButton.attributes("disabled")).toBeUndefined();

    await new Promise(resolve => setTimeout(resolve, 1000));

    await flushPromises();
    await nextTick();

    expect(closeButton.attributes("disabled")).toBe("disabled");
  });
});