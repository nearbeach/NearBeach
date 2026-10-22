import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises, nextTick } from "@vue/test-utils";
import DocumentListRender from "./DocumentListRender.vue";
import { createPinia, setActivePinia } from "pinia";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import i18n from "@/i18n.ts";

describe("DocumentListRender", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders empty folder message when there are no documents or folders", async () => {
    const wrapper = mount(DocumentListRender, {
      global: {
        plugins: [i18n],
      },
    });

    // Check if the empty folder message is visible
    const emptyFolderMessage = wrapper.find(".empty-folder");
    expect(emptyFolderMessage.exists()).toBe(true);
  });

  test("does not render empty folder message when there are documents", async () => {
    const documentationStore = useDocumentationStore();
    documentationStore.documents = [{ key: "doc1", parent_folder_id: 0 }];

    const wrapper = mount(DocumentListRender, {
      global: {
        plugins: [i18n],
      },
    });

    // Check if the empty folder message is not visible
    const emptyFolderMessage = wrapper.find(".empty-folder");
    expect(emptyFolderMessage.exists()).toBe(false);
  });

  test("does not render empty folder message when there are folders", async () => {
    const documentationStore = useDocumentationStore();
    documentationStore.folders = [{ id: 1, description: "Folder 1", parent_folder_id: 0 }];

    const wrapper = mount(DocumentListRender, {
      global: {
        plugins: [i18n],
      },
    });

    // Check if the empty folder message is not visible
    const emptyFolderMessage = wrapper.find(".empty-folder");
    expect(emptyFolderMessage.exists()).toBe(false);
  });
});