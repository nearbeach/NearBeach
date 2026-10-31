import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import NewFolder from "./NewFolder.vue";

function mountNewFolder() {
  return mount(NewFolder, { global: { plugins: [i18n] } });
}

describe("NewFolder", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 31;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("create is disabled until a name is entered", async () => {
    const wrapper = mountNewFolder();

    expect(wrapper.find("button.primary").attributes("disabled")).toBeDefined();

    await wrapper.find("input").setValue("Reports");

    expect(wrapper.find("button.primary").attributes("disabled")).toBeUndefined();
  });

  test("cancel emits closeModal", async () => {
    const wrapper = mountNewFolder();

    await wrapper.findAll("button")[0].trigger("click");

    expect(wrapper.emitted("closeModal")).toHaveLength(1);
  });

  test("creating a folder in a folder posts the parent id, stores it and closes", async () => {
    const documentationStore = useDocumentationStore();
    documentationStore.currentFolderId = 4;
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      json: () => Promise.resolve({ id: 8, description: "Reports", parent_folder_id: 4 }),
    } as Response);
    const wrapper = mountNewFolder();

    await wrapper.find("input").setValue("Reports");
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/31/documents/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("POST");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
      description: "Reports",
      type: "folder",
      parent_folder_id: 4,
    });
    expect(documentationStore.folders).toContainEqual({ id: 8, description: "Reports", parent_folder_id: 4 });
    expect(wrapper.emitted("closeModal")).toHaveLength(1);
    expect((wrapper.find("input").element as HTMLInputElement).value).toBe("");
  });

  test("creating a folder at the root sends a null parent", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      json: () => Promise.resolve({ id: 9, description: "Root", parent_folder_id: null }),
    } as Response);
    const wrapper = mountNewFolder();

    await wrapper.find("input").setValue("Root");
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string).parent_folder_id).toBeNull();
  });

  test("a failed request keeps the modal open and stores nothing", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
    const documentationStore = useDocumentationStore();
    const wrapper = mountNewFolder();

    await wrapper.find("input").setValue("Reports");
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    expect(documentationStore.folders).toHaveLength(0);
    expect(wrapper.emitted("closeModal")).toBeUndefined();
  });
});
