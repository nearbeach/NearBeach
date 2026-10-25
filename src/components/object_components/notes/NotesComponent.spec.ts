import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import NoteList from "@/components/object_components/notes/note_list/NoteList.vue";
import { NotesComponent } from ".";

const notes = [
  { id: 1, note: "First", date_created: "2026-01-01", user: "a" },
  { id: 2, note: "Second", date_created: "2026-01-02", user: "b" },
];

function mockFetch(handler?: (url: string, init?: RequestInit) => unknown) {
  return vi.spyOn(globalThis, "fetch").mockImplementation(
    async (url, init) =>
      ({
        status: 200,
        json: async () => structuredClone(handler ? handler(String(url), init) : notes),
      }) as Response,
  );
}

function mountNotes() {
  return mount(NotesComponent, {
    global: { plugins: [i18n], stubs: { teleport: true } },
  });
}

describe("NotesComponent", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 3;
    objectStore.is_loaded = true;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  const noteList = (w: ReturnType<typeof mountNotes>) =>
    w.findComponent(NoteList).props("noteList") as typeof notes;

  test("loads notes on mount when the object is already loaded", async () => {
    const fetchSpy = mockFetch();
    const wrapper = mountNotes();
    await flushPromises();

    expect(fetchSpy).toHaveBeenCalledWith(
      "/api/v1/project/3/notes/",
      expect.objectContaining({ method: "GET" }),
    );
    expect(noteList(wrapper)).toHaveLength(2);
  });

  test("waits for the object to load before fetching", async () => {
    const objectStore = useObjectStore();
    objectStore.is_loaded = false;
    const fetchSpy = mockFetch();

    const wrapper = mountNotes();
    await flushPromises();
    expect(fetchSpy).not.toHaveBeenCalled();

    objectStore.is_loaded = true;
    await flushPromises();

    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(noteList(wrapper)).toHaveLength(2);
  });

  test("logs an error when loading fails", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("boom"));
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});

    mountNotes();
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
  });

  test("create button opens an empty modal in create mode", async () => {
    mockFetch();
    const wrapper = mountNotes();
    await flushPromises();

    await wrapper.find("button.create-note").trigger("click");

    expect(wrapper.find(".open").exists()).toBe(true);
    expect(wrapper.find("h3").text()).toBe("Submit note");
    expect(wrapper.find("textarea").element.value).toBe("");
  });

  test("creating a note posts it and puts it at the top of the list", async () => {
    const fetchSpy = mockFetch((url, init) =>
      init?.method === "POST" ? { id: 9, note: "New" } : notes,
    );
    const wrapper = mountNotes();
    await flushPromises();

    await wrapper.find("button.create-note").trigger("click");
    await wrapper.find("textarea").setValue("New");
    await wrapper.find(".modal-footer-row button.primary").trigger("click");
    await flushPromises();

    const post = fetchSpy.mock.calls.find(([, i]) => i?.method === "POST")!;
    expect(post[0]).toBe("/api/v1/project/3/notes/");
    expect(JSON.parse(post[1]?.body as string)).toEqual({ note: "New" });
    expect(noteList(wrapper)[0]).toEqual({ id: 9, note: "New" });
    expect(noteList(wrapper)).toHaveLength(3);
    expect(wrapper.find(".open").exists()).toBe(false);
  });

  test("logs an error when creating fails", async () => {
    let first = true;
    vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
      if (first) {
        first = false;
        return { json: async () => structuredClone(notes) } as Response;
      }
      throw new Error("fail");
    });
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});

    const wrapper = mountNotes();
    await flushPromises();
    await wrapper.find("button.create-note").trigger("click");
    await wrapper.find(".modal-footer-row button.primary").trigger("click");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(noteList(wrapper)).toHaveLength(2);
  });

  test("editing a note opens the modal pre-filled and PATCHes the change", async () => {
    const fetchSpy = mockFetch();
    const wrapper = mountNotes();
    await flushPromises();

    wrapper.findComponent(NoteList).vm.$emit("editNote", 1);
    await flushPromises();

    expect(wrapper.find("h3").text()).toBe("Edit note");
    expect(wrapper.find("textarea").element.value).toBe("Second");

    await wrapper.find("textarea").setValue("Second (edited)");
    await wrapper.find(".modal-footer-row button.primary").trigger("click");
    await flushPromises();

    const patch = fetchSpy.mock.calls.find(([, i]) => i?.method === "PATCH")!;
    expect(patch[0]).toBe("/api/v1/project/3/notes/2/");
    expect(JSON.parse(patch[1]?.body as string)).toEqual({ note: "Second (edited)" });
    expect(noteList(wrapper)[1].note).toBe("Second (edited)");
    expect(wrapper.find(".open").exists()).toBe(false);
  });

  test("editing an index that does not exist does nothing", async () => {
    mockFetch();
    const wrapper = mountNotes();
    await flushPromises();

    wrapper.findComponent(NoteList).vm.$emit("editNote", 10);
    await flushPromises();

    expect(wrapper.find(".open").exists()).toBe(false);
  });

  test("logs an error when updating fails", async () => {
    let calls = 0;
    vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
      if (calls++ === 0) return { json: async () => structuredClone(notes) } as Response;
      throw new Error("fail");
    });
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});

    const wrapper = mountNotes();
    await flushPromises();
    wrapper.findComponent(NoteList).vm.$emit("editNote", 0);
    await flushPromises();
    await wrapper.find(".modal-footer-row button.primary").trigger("click");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(noteList(wrapper)[0].note).toBe("First");
  });

  test("deleting a note sends DELETE and removes it from the list", async () => {
    const fetchSpy = mockFetch();
    const wrapper = mountNotes();
    await flushPromises();

    wrapper.findComponent(NoteList).vm.$emit("deleteNote", 1);
    await flushPromises();

    const del = fetchSpy.mock.calls.find(([, i]) => i?.method === "DELETE")!;
    expect(del[0]).toBe("/api/v1/project/3/notes/1/");
    expect(noteList(wrapper).map((n) => n.id)).toEqual([2]);
  });

  test("logs an error and keeps the note when deleting fails", async () => {
    let calls = 0;
    vi.spyOn(globalThis, "fetch").mockImplementation(async () => {
      if (calls++ === 0) return { json: async () => structuredClone(notes) } as Response;
      throw new Error("fail");
    });
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});

    const wrapper = mountNotes();
    await flushPromises();
    wrapper.findComponent(NoteList).vm.$emit("deleteNote", 1);
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(noteList(wrapper)).toHaveLength(2);
  });

  test("cancel closes the modal and clears the text", async () => {
    mockFetch();
    const wrapper = mountNotes();
    await flushPromises();

    wrapper.findComponent(NoteList).vm.$emit("editNote", 0);
    await flushPromises();
    await wrapper.find("button.danger").trigger("click");

    expect(wrapper.find(".open").exists()).toBe(false);
    expect(wrapper.find("textarea").element.value).toBe("");
  });
});
