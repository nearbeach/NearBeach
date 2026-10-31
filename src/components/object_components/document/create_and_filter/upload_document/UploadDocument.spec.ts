import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { WlkFileUpload } from "whelk-ui";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import UploadDocument from "./UploadDocument.vue";

function mountUpload() {
  return mount(UploadDocument, { global: { plugins: [i18n] } });
}

function makeFile(name = "report.pdf") {
  return new File(["content"], name, { type: "application/pdf" });
}

// Put files into the file upload and let the component react to the change
async function selectFiles(wrapper: ReturnType<typeof mountUpload>, files: File[]) {
  const upload = wrapper.findComponent(WlkFileUpload);
  upload.vm.$emit("update:modelValue", files);
  upload.vm.$emit("change");
  await flushPromises();
}

describe("UploadDocument", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 9;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("upload is disabled until a file and name exist", async () => {
    const wrapper = mountUpload();
    const upload = () => wrapper.find("button.primary");

    expect(upload().attributes("disabled")).toBeDefined();

    await selectFiles(wrapper, [makeFile()]);

    expect(upload().attributes("disabled")).toBeUndefined();
  });

  test("selecting a file fills in the document name", async () => {
    const wrapper = mountUpload();

    await selectFiles(wrapper, [makeFile("plan.pdf")]);

    expect((wrapper.find("input[type=text], input:not([type=file])").element as HTMLInputElement).value).toBe("plan.pdf");
  });

  test("cancel emits closeModal", async () => {
    const wrapper = mountUpload();

    await wrapper.findAll("button")[0].trigger("click");

    expect(wrapper.emitted("closeModal")).toHaveLength(1);
  });

  test("uploads from the root folder without a parent folder id", async () => {
    const documentationStore = useDocumentationStore();
    documentationStore.currentFolderId = 0;
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      json: () => Promise.resolve([
        { description: "report.pdf", key: "k1", parent_folder_id: null },
      ]),
    } as Response);

    const wrapper = mountUpload();
    await selectFiles(wrapper, [makeFile()]);
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    const [url, options] = fetchSpy.mock.calls[0];
    expect(url).toBe("/api/v1/project/9/documents/");
    expect(options?.method).toBe("POST");
    const body = options?.body as FormData;
    expect(body.get("type")).toBe("document");
    expect(body.get("description")).toBe("report.pdf");
    expect(body.getAll("document")).toHaveLength(1);
    expect(body.has("parent_folder_id")).toBe(false);

    expect(documentationStore.documents).toContainEqual({
      description: "report.pdf",
      key: "k1",
      parent_folder_id: null,
      url_location: null,
      document: null,
      folder: null,
    });
    expect(wrapper.emitted("closeModal")).toHaveLength(1);
  });

  test("includes the parent folder id when inside a folder", async () => {
    const documentationStore = useDocumentationStore();
    documentationStore.currentFolderId = 12;
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      json: () => Promise.resolve([]),
    } as Response);

    const wrapper = mountUpload();
    await selectFiles(wrapper, [makeFile()]);
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    const body = fetchSpy.mock.calls[0][1]?.body as FormData;
    expect(body.get("parent_folder_id")).toBe("12");
  });

  test("logs the error and keeps the modal open when the upload fails", async () => {
    const documentationStore = useDocumentationStore();
    const before = documentationStore.documents.length;
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("network"));
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });

    const wrapper = mountUpload();
    await selectFiles(wrapper, [makeFile()]);
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(documentationStore.documents).toHaveLength(before);
    expect(wrapper.emitted("closeModal")).toBeUndefined();
  });
});

describe("UploadDocument - custom name", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 9;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("a name typed by the user is what gets uploaded", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      json: () => Promise.resolve([]),
    } as Response);
    const wrapper = mountUpload();

    await selectFiles(wrapper, [makeFile("report.pdf")]);
    await wrapper.find("input:not([type=file])").setValue("Quarterly report");
    await wrapper.find("button.primary").trigger("click");
    await flushPromises();

    expect((fetchSpy.mock.calls[0][1]?.body as FormData).get("description")).toBe("Quarterly report");
  });
});
