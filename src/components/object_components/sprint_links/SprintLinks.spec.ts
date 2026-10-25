import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import SprintLink from "@/components/object_components/sprint_links/sprint_link/SprintLink.vue";
import { SprintLinks } from ".";

const sprints = [
  { id: "s1", title: "Sprint 1", start_date: "2026-01-01T00:00:00", end_date: "2026-01-08T00:00:00", status: "Open", total_story_points: 0, completed_story_points: 0, requirement: [], project: [] },
  { id: "s2", title: "Sprint 2", start_date: "2026-01-09T00:00:00", end_date: "2026-01-16T00:00:00", status: "Open", total_story_points: 0, completed_story_points: 0, requirement: [], project: [] },
];

function mockFetch(handler: (url: string, init?: RequestInit) => { status: number; body: unknown }) {
  return vi.spyOn(globalThis, "fetch").mockImplementation(async (url, init) => {
    const { status, body } = handler(String(url), init);
    return { status, json: async () => structuredClone(body) } as Response;
  });
}

function mountSprintLinks() {
  return mount(SprintLinks, {
    global: { plugins: [i18n], stubs: { teleport: true } },
  });
}

const okList = (_url: string, init?: RequestInit) =>
  init?.method === "GET" || init === undefined
    ? { status: 200, body: sprints }
    : { status: 500, body: { error: "unexpected" } };

describe("SprintLinks", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 8;
    objectStore.is_loaded = true;
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  test("loads and renders the sprints when the object is loaded", async () => {
    const fetchSpy = mockFetch(okList);
    const wrapper = mountSprintLinks();
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/8/sprint/");
    expect(wrapper.findAllComponents(SprintLink)).toHaveLength(2);
    expect(wrapper.find(".empty-sprint-list").exists()).toBe(false);
  });

  test("shows the empty message when there are no sprints", async () => {
    mockFetch(() => ({ status: 200, body: [] }));
    const wrapper = mountSprintLinks();
    await flushPromises();

    expect(wrapper.find(".empty-sprint-list").text()).toBe("No sprint links connected to this object.");
  });

  test("waits for the object to load before fetching", async () => {
    const objectStore = useObjectStore();
    objectStore.is_loaded = false;
    const fetchSpy = mockFetch(okList);
    const wrapper = mountSprintLinks();
    await flushPromises();
    expect(fetchSpy).not.toHaveBeenCalled();

    objectStore.is_loaded = true;
    await flushPromises();

    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(wrapper.findAllComponents(SprintLink)).toHaveLength(2);
  });

  test("a failed load leaves the list empty", async () => {
    mockFetch(() => ({ status: 500, body: { error: "Server error" } }));
    const wrapper = mountSprintLinks();
    await flushPromises();

    expect(wrapper.findAllComponents(SprintLink)).toHaveLength(0);
  });

  test("create sprint opens the modal with default title and dates", async () => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(new Date("2026-03-01T12:00:00Z"));
    mockFetch(() => ({ status: 200, body: [] }));
    const wrapper = mountSprintLinks();
    await flushPromises();

    await wrapper.find(".sprint-buttons button").trigger("click");

    expect(wrapper.find(".open").exists()).toBe(true);
    const inputs = wrapper.findAll("input");
    expect((inputs[0].element as HTMLInputElement).value).toBe(
      "project-8: 2026-03-01 -> 2026-03-08",
    );
  });

  test("closing the modal hides it", async () => {
    mockFetch(() => ({ status: 200, body: [] }));
    const wrapper = mountSprintLinks();
    await flushPromises();
    await wrapper.find(".sprint-buttons button").trigger("click");

    await wrapper.find("button.secondary").trigger("click");
    expect(wrapper.find(".open").exists()).toBe(false);

    await wrapper.find(".sprint-buttons button").trigger("click");
    await wrapper.find('[aria-label="Cancel"]').trigger("click");
    expect(wrapper.find(".open").exists()).toBe(false);
  });

  test("creating a sprint posts it, adds it to the list and closes the modal", async () => {
    const created = { ...sprints[0], id: "s3", title: "New one" };
    const fetchSpy = mockFetch((_url, init) =>
      init?.method === "POST"
        ? { status: 201, body: created }
        : { status: 200, body: sprints },
    );
    const wrapper = mountSprintLinks();
    await flushPromises();

    await wrapper.find(".sprint-buttons button").trigger("click");
    await wrapper.find("button.primary:not(.sprint-buttons button)").trigger("click");
    await flushPromises();

    const post = fetchSpy.mock.calls.find(([, i]) => i?.method === "POST")!;
    expect(post[0]).toBe("/api/v1/project/8/sprint/");
    const body = JSON.parse(post[1]?.body as string);
    expect(Object.keys(body).sort()).toEqual(["end_date", "start_date", "title"]);
    expect(wrapper.findAllComponents(SprintLink)).toHaveLength(3);
    expect(wrapper.find(".open").exists()).toBe(false);
  });

  test("a rejected create keeps the modal open and the list unchanged", async () => {
    mockFetch((_url, init) =>
      init?.method === "POST"
        ? { status: 400, body: { error: "Bad dates" } }
        : { status: 200, body: sprints },
    );
    const wrapper = mountSprintLinks();
    await flushPromises();

    await wrapper.find(".sprint-buttons button").trigger("click");
    await wrapper.find("button.primary:not(.sprint-buttons button)").trigger("click");
    await flushPromises();

    expect(wrapper.findAllComponents(SprintLink)).toHaveLength(2);
    expect(wrapper.find(".open").exists()).toBe(true);
  });

  test("deleting removes the sprint optimistically and calls DELETE", async () => {
    const fetchSpy = mockFetch((_url, init) =>
      init?.method === "DELETE"
        ? { status: 204, body: {} }
        : { status: 200, body: sprints },
    );
    const wrapper = mountSprintLinks();
    await flushPromises();

    wrapper.findAllComponents(SprintLink)[0].vm.$emit("deleteSprint", "s1");
    await flushPromises();

    const del = fetchSpy.mock.calls.find(([, i]) => i?.method === "DELETE")!;
    expect(del[0]).toBe("/api/v1/project/8/sprint/s1/");
    const remaining = wrapper.findAllComponents(SprintLink);
    expect(remaining).toHaveLength(1);
    expect(remaining[0].props("sprint").id).toBe("s2");
  });

  test("a failed delete does not throw", async () => {
    mockFetch((_url, init) =>
      init?.method === "DELETE"
        ? { status: 403, body: { error: "Forbidden" } }
        : { status: 200, body: sprints },
    );
    const wrapper = mountSprintLinks();
    await flushPromises();

    wrapper.findAllComponents(SprintLink)[1].vm.$emit("deleteSprint", "s2");
    await flushPromises();

    expect(wrapper.exists()).toBe(true);
  });
});
