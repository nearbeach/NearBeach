import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import i18n from "@/i18n.ts";
import { useErrorStore } from "@/stores/error/error.ts";
import { DocumentList } from ".";

function mountList() {
  return mount(DocumentList, { global: { plugins: [i18n] } });
}

const doc = (key: string, description: string, extra = {}) => ({
  key,
  description,
  parent_folder_id: null,
  url_location: null,
  document: null,
  folder: null,
  ...extra,
});

describe("DocumentList", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    usePermissionStore().currentObjectPermissions.currentObject = 2;
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 31;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("lists the documents in the current folder only", () => {
    const documentationStore = useDocumentationStore();
    documentationStore.documents = [
      doc("a", "root.pdf"),
      doc("b", "nested.pdf", { parent_folder_id: 5 }),
    ];

    const wrapper = mountList();
    expect(wrapper.findAll(".document-item")).toHaveLength(1);
    expect(wrapper.find(".document-details a").text()).toBe("root.pdf");
    expect(wrapper.find(".document-details a").attributes("href")).toBe("/private/a/");

    documentationStore.currentFolderId = 5;
    return wrapper.vm.$nextTick().then(() => {
      expect(wrapper.find(".document-details a").text()).toBe("nested.pdf");
    });
  });

  test("links get the link icon and other files the generic file icon", () => {
    useDocumentationStore().documents = [
      doc("a", "site", { url_location: "https://nearbeach.org/" }),
      doc("b", "report.pdf"),
    ];

    const wrapper = mountList();
    const icons = wrapper.findAll(".document-icon svg");

    expect(icons[0].classes()).toContain("lucide-link");
    expect(icons[1].classes()).toContain("lucide-file");
  });

  test.each([
    ["photo.image", "lucide-image"],
    ["notes.document", "lucide-file-text"],
    ["page.link", "lucide-link"],
    ["deck.powerpoint", "lucide-presentation"],
  ])("description %s uses the %s icon", (description, iconClass) => {
    useDocumentationStore().documents = [doc("a", description)];

    const wrapper = mountList();

    expect(wrapper.find(".document-icon svg").classes()).toContain(iconClass);
  });

  test("deleting a document sends its type and removes it", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 204 } as Response);
    const documentationStore = useDocumentationStore();
    documentationStore.documents = [doc("a", "root.pdf"), doc("b", "other.pdf")];
    const wrapper = mountList();

    await wrapper.find(".document-delete").trigger("click");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/31/documents/a/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("DELETE");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({ type: "document" });
    expect(documentationStore.documents.map((d) => d.key)).toEqual(["b"]);
  });

  test("deleting a link sends the link type", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 204 } as Response);
    useDocumentationStore().documents = [
      doc("a", "site", { url_location: "https://nearbeach.org/" }),
    ];
    const wrapper = mountList();

    await wrapper.find(".document-delete").trigger("click");
    await flushPromises();

    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({ type: "link" });
  });

  test("a forbidden delete shows the error modal and keeps the document", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 403 } as Response);
    const documentationStore = useDocumentationStore();
    documentationStore.documents = [doc("a", "root.pdf")];
    const wrapper = mountList();

    await wrapper.find(".document-delete").trigger("click");
    await flushPromises();

    expect(useErrorStore().showErrorModal).toBe(true);
    expect(documentationStore.documents).toHaveLength(1);
  });

  test("any other failed delete shows the status text and keeps the document", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 500, statusText: "Server Error" } as Response);
    const documentationStore = useDocumentationStore();
    documentationStore.documents = [doc("a", "root.pdf")];
    const wrapper = mountList();

    await wrapper.find(".document-delete").trigger("click");
    await flushPromises();

    const errorStore = useErrorStore();
    expect(errorStore.message).toBe("Server Error");
    expect(errorStore.showErrorModal).toBe(true);
    expect(documentationStore.documents).toHaveLength(1);
  });
});

describe("DocumentList - missing description", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    usePermissionStore().currentObjectPermissions.currentObject = 2;
  });

  test("a document without a description gets the generic file icon", () => {
    useDocumentationStore().documents = [doc("a", null as unknown as string)];

    const wrapper = mountList();

    expect(wrapper.find(".document-icon svg").classes()).toContain("lucide-file");
  });
});
