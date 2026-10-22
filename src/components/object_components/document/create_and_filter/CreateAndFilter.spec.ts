import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises, nextTick } from "@vue/test-utils";
import CreateAndFilter from "./CreateAndFilter.vue";
import i18n from "@/i18n.ts";
import { createPinia, setActivePinia } from "pinia";

describe("CreateAndFilter", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("clicking dropdown item opens modal with correct content", async () => {
    const wrapper = mount(CreateAndFilter, {
      global: {
        plugins: [i18n],
      },
    });

    // Click on the dropdown button
    const dropdownButton = wrapper.find(".wlk-dropdown-button");
    await dropdownButton.trigger("click");

    // Click on the "new_folder" dropdown item
    const newFolderItem = wrapper.find(".wlk-dropdown-item[data-event='new_folder']");
    await newFolderItem.trigger("click");

    // Modal is open
    const modal = wrapper.find(".wlk-modal.open");
    expect(modal.exists()).toBe(true);

    // Modal header is correct
    const modalHeader = wrapper.find(".modal-header-row h3");
    expect(modalHeader.text()).toBe("Create a new folder");

    // NewFolder component is rendered
    const newFolderComponent = wrapper.findComponent(NewFolder);
    expect(newFolderComponent.exists()).toBe(true);
  });

  test("clicking close button closes modal", async () => {
    const wrapper = mount(CreateAndFilter, {
      global: {
        plugins: [i18n],
      },
    });

    // Click on the dropdown button
    const dropdownButton = wrapper.find(".wlk-dropdown-button");
    await dropdownButton.trigger("click");

    // Click on the "new_folder" dropdown item
    const newFolderItem = wrapper.find(".wlk-dropdown-item[data-event='new_folder']");
    await newFolderItem.trigger("click");

    // Click on the close button
    const closeButton = wrapper.find(".modal-header-row .x");
    await closeButton.trigger("click");

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Modal is closed
    const modal = wrapper.find(".wlk-modal.open");
    expect(modal.exists()).toBe(false);
  });
});