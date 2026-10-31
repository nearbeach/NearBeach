import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import FolderList from "./FolderList.vue";

function mountFolders() {
  return mount(FolderList, { global: { plugins: [i18n] } });
}

describe("FolderList", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 31;
    useDocumentationStore().folders = [
      { id: 1, description: "Top", parent_folder_id: null },
      { id: 2, description: "Child", parent_folder_id: 1 },
    ];
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // The first .folder-item is always the "parent folder" row
  const folderRows = (wrapper: ReturnType<typeof mountFolders>) => wrapper.findAll(".folder-item").slice(1);

  test("lists the folders in the current folder", () => {
    const wrapper = mountFolders();

    expect(folderRows(wrapper).map((row) => row.text())).toEqual(["Top"]);
  });

  test("the parent folder row is hidden at the root", () => {
    const wrapper = mountFolders();

    expect(wrapper.find(".folder-item").attributes("style")).toContain("display: none");
  });

  test("opening a folder moves into it and adds a bread crumb", async () => {
    const documentationStore = useDocumentationStore();
    const wrapper = mountFolders();

    await folderRows(wrapper)[0].find(".folder-details").trigger("click");

    expect(documentationStore.currentFolderId).toBe(1);
    expect(documentationStore.breadCrumbsArray).toEqual([{ folderId: 1, label: "Top" }]);
    expect(folderRows(wrapper).map((row) => row.text())).toEqual(["Child"]);
    expect(wrapper.find(".folder-item").attributes("style") ?? "").not.toContain("display: none");
  });

  test("clicking the folder icon also opens the folder", async () => {
    const wrapper = mountFolders();

    await folderRows(wrapper)[0].find(".folder-icon").trigger("click");

    expect(useDocumentationStore().currentFolderId).toBe(1);
  });

  test("the parent row goes up a folder and removes a bread crumb", async () => {
    const documentationStore = useDocumentationStore();
    documentationStore.currentFolderId = 2;
    documentationStore.breadCrumbsArray = [
      { folderId: 1, label: "Top" },
      { folderId: 2, label: "Child" },
    ];
    const wrapper = mountFolders();

    await wrapper.find(".folder-item").trigger("click");

    expect(documentationStore.currentFolderId).toBe(1);
    expect(documentationStore.breadCrumbsArray).toEqual([{ folderId: 1, label: "Top" }]);
  });

  test("deleting a folder sends its type and removes it", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200 } as Response);
    const documentationStore = useDocumentationStore();
    const wrapper = mountFolders();

    await folderRows(wrapper)[0].find(".folder-delete").trigger("click");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/31/documents/1/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("DELETE");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({ type: "folder" });
    expect(documentationStore.folders.map((f) => f.id)).toEqual([2]);
  });

  test("a failed delete is logged and keeps the folder", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });
    const documentationStore = useDocumentationStore();
    const wrapper = mountFolders();

    await folderRows(wrapper)[0].find(".folder-delete").trigger("click");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(documentationStore.folders).toHaveLength(2);
  });
});
