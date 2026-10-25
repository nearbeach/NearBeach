import { NewLink } from "@/components/object_components/document/create_and_filter/new_link";
import { UploadDocument } from "@/components/object_components/document/create_and_filter/upload_document";
import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {CreateAndFilter} from ".";
import i18n from "@/i18n.ts";
import { createPinia, setActivePinia } from "pinia";
import {nextTick} from "vue";
import {NewFolder} from "@/components/object_components/document/create_and_filter/new_folder";

// Keep the teleported modal inside the wrapper so it can be found
function mountCreateAndFilter() {
  return mount(CreateAndFilter, {
    global: {
      plugins: [i18n],
      stubs: {
        teleport: true,
      }
    },
  });
}

async function openNewFolderModal(wrapper: ReturnType<typeof mountCreateAndFilter>) {
  // Click on the dropdown button
  const dropdownButton = wrapper.find(".wlk-drop-down > button");
  await dropdownButton.trigger("click");

  // Click on the "Create a new folder" dropdown item
  const newFolderItem = wrapper.findAll(".drop-down-item").find((item) => item.text() === "Create a new folder");
  await newFolderItem!.trigger("click");

  await flushPromises();
  await nextTick();
}

describe("CreateAndFilter", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("clicking dropdown item opens modal with correct content", async () => {
    const wrapper = mountCreateAndFilter();

    // Modal starts closed
    expect(wrapper.find(".wlk-modal.open").exists()).toBe(false);

    await openNewFolderModal(wrapper);

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
    const wrapper = mountCreateAndFilter();

    await openNewFolderModal(wrapper);
    expect(wrapper.find(".wlk-modal.open").exists()).toBe(true);

    // Click on the close (X) icon
    const closeButton = wrapper.find(".modal-header-row svg.lucide-x");
    await closeButton.trigger("click");

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Modal is closed
    const modal = wrapper.find(".wlk-modal.open");
    expect(modal.exists()).toBe(false);
  });
});

describe("CreateAndFilter - other dropdown items", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  async function chooseItem(wrapper: ReturnType<typeof mountCreateAndFilter>, label: string) {
    await wrapper.find(".wlk-drop-down > button").trigger("click");
    const item = wrapper.findAll(".drop-down-item").find((row) => row.text() === label);
    await item!.trigger("click");
    await flushPromises();
  }

  test("the hyperlink item opens the new link form", async () => {
    const wrapper = mountCreateAndFilter();

    await chooseItem(wrapper, "Create a new hyperlink");

    expect(wrapper.find(".wlk-modal.open").exists()).toBe(true);
    expect(wrapper.findComponent(NewLink).exists()).toBe(true);
  });

  test("the upload item opens the upload form", async () => {
    const wrapper = mountCreateAndFilter();

    await chooseItem(wrapper, "Upload a document");

    expect(wrapper.find(".wlk-modal.open").exists()).toBe(true);
    expect(wrapper.findComponent(UploadDocument).exists()).toBe(true);
  });
});
