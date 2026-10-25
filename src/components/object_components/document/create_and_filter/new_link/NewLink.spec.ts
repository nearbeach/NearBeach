import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import { NewLink } from ".";

function mountNewLink() {
  return mount(NewLink, { global: { plugins: [i18n] } });
}

function mockResponse(overrides = {}) {
  return {
    json: async () => ({
      description: "My link",
      key: 7,
      parent_folder_id: "4",
      url_location: "https://nearbeach.org/",
      ...overrides,
    }),
  } as Response;
}

async function fillIn(wrapper: ReturnType<typeof mountNewLink>) {
  const inputs = wrapper.findAll("input");
  await inputs[0].setValue("https://nearbeach.org/");
  await inputs[1].setValue("My link");
}

describe("NewLink", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 55;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("create button is disabled until a url is entered", async () => {
    const wrapper = mountNewLink();
    const create = () => wrapper.find("button.primary");

    expect(create().attributes("disabled")).toBeDefined();

    await wrapper.findAll("input")[0].setValue("https://nearbeach.org/");

    expect(create().attributes("disabled")).toBeUndefined();
  });

  test("cancel emits closeModal", async () => {
    const wrapper = mountNewLink();

    await wrapper.findAll("button")[0].trigger("click");

    expect(wrapper.emitted("closeModal")).toHaveLength(1);
  });

  test("posts the link, stores it and closes the modal", async () => {
    const documentationStore = useDocumentationStore();
    documentationStore.currentFolderId = 4;
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(mockResponse());

    const wrapper = mountNewLink();
    await fillIn(wrapper);
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    const [url, options] = fetchSpy.mock.calls[0];
    expect(url).toBe("/api/v1/project/55/documents/");
    expect(options?.method).toBe("POST");
    expect(JSON.parse(options?.body as string)).toEqual({
      description: "My link",
      type: "link",
      url_location: "https://nearbeach.org/",
      parent_folder_id: 4,
    });

    expect(documentationStore.documents).toContainEqual({
      description: "My link",
      key: "7",
      parent_folder_id: 4,
      url_location: "https://nearbeach.org/",
      document: null,
      folder: null,
    });
    expect(wrapper.emitted("closeModal")).toHaveLength(1);

    // The form is cleared
    const inputs = wrapper.findAll("input");
    expect((inputs[0].element as HTMLInputElement).value).toBe("");
    expect((inputs[1].element as HTMLInputElement).value).toBe("");
  });

  test("sends a null parent folder when at the root", async () => {
    const documentationStore = useDocumentationStore();
    documentationStore.currentFolderId = 0;
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      mockResponse({ parent_folder_id: "0" }),
    );

    const wrapper = mountNewLink();
    await fillIn(wrapper);
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    const body = JSON.parse(fetchSpy.mock.calls[0][1]?.body as string);
    expect(body.parent_folder_id).toBeNull();
  });

  test("keeps the modal open and stores nothing when the request fails", async () => {
    const documentationStore = useDocumentationStore();
    const before = documentationStore.documents.length;
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("network"));

    const wrapper = mountNewLink();
    await fillIn(wrapper);
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    expect(documentationStore.documents).toHaveLength(before);
    expect(wrapper.emitted("closeModal")).toBeUndefined();
  });
});
