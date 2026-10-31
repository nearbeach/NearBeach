import { beforeEach, describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import {DocumentListRender} from ".";
import { createPinia, setActivePinia } from "pinia";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import i18n from "@/i18n.ts";

describe("DocumentListRender", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders empty folder message when there are no documents or folders", () => {
    // Attached so isVisible() can see the v-show display style
    const wrapper = mount(DocumentListRender, {
      attachTo: document.body,
      global: {
        plugins: [i18n],
      },
    });

    // Check if the empty folder message is visible
    const emptyFolderMessage = wrapper.find(".empty-folder");
    expect(emptyFolderMessage.isVisible()).toBe(true);
    wrapper.unmount();
  });

  test("does not render empty folder message when there are documents", () => {
    const documentationStore = useDocumentationStore();
    documentationStore.documents = [
        { description: "The document of writing unit tests", document: null, folder: null, key: "doc1", parent_folder_id: 0, url_location: null }
    ];

    // Attached so isVisible() can see the v-show display style
    const wrapper = mount(DocumentListRender, {
      attachTo: document.body,
      global: {
        plugins: [i18n],
      },
    });

    // Check if the empty folder message is not visible
    const emptyFolderMessage = wrapper.find(".empty-folder");
    expect(emptyFolderMessage.isVisible()).toBe(false);
    wrapper.unmount();
  });

  test("does not render empty folder message when there are folders", () => {
    const documentationStore = useDocumentationStore();
    documentationStore.folders = [{ id: 1, description: "Folder 1", parent_folder_id: 0 }];

    // Attached so isVisible() can see the v-show display style
    const wrapper = mount(DocumentListRender, {
      attachTo: document.body,
      global: {
        plugins: [i18n],
      },
    });

    // Check if the empty folder message is not visible
    const emptyFolderMessage = wrapper.find(".empty-folder");
    expect(emptyFolderMessage.isVisible()).toBe(false);
    wrapper.unmount();
  });
});