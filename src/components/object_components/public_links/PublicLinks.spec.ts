import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useObjectStore } from "@/stores/object/object.ts";
import {PublicLinks} from ".";
import PublicLinkRow from "./public_link_row/PublicLinkRow.vue";
import { vi } from "vitest";
import {nextTick} from "vue";
import i18n from "@/i18n.ts";

function mountPublicLinks() {
  return mount(PublicLinks, {
    global: {
      plugins: [i18n],
    },
  });
}

describe("PublicLinks", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.is_loaded = true;
    objectStore.destination = "test-destination";
    objectStore.id = 123;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("mounting component", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: () => Promise.resolve([]),
    } as Response);

    const wrapper = mountPublicLinks();
    await flushPromises();

    expect(wrapper.exists()).toBe(true);
    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/v1/test-destination/123/public_link/",
      expect.any(Object),
    );
  });

  test("does not render the links table when the fetch fails", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 500,
      json: () => Promise.resolve({ error: "Server error" }),
    } as Response);

    const wrapper = mountPublicLinks();

    await flushPromises();
    await nextTick();

    // The component keeps the error, but does not display it yet
    expect(wrapper.find("table").exists()).toBe(false);
  });
});

describe("PublicLinks - managing links", () => {
  const links = [
    { id: "a", is_active: true },
    { id: "b", is_active: false },
  ];

  // Respond to each request by method so loading and mutating can differ
  function mockFetch(responses: Record<string, { status: number; body: unknown }>) {
    return vi.spyOn(globalThis, "fetch").mockImplementation((_url, init) => {
      const { status, body } = responses[init?.method ?? "GET"] ?? { status: 200, body: {} };
      return Promise.resolve({ status, json: () => Promise.resolve(structuredClone(body)) } as Response);
    });
  }

  async function mountLoaded(responses: Parameters<typeof mockFetch>[0]) {
    const fetchSpy = mockFetch({ GET: { status: 200, body: links }, ...responses });
    const wrapper = mountPublicLinks();
    await flushPromises();
    return { wrapper, fetchSpy };
  }

  const rows = (wrapper: ReturnType<typeof mountPublicLinks>) => wrapper.findAllComponents(PublicLinkRow);

  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.is_loaded = true;
    objectStore.destination = "project";
    objectStore.id = 6;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders a row for each loaded link", async () => {
    const { wrapper } = await mountLoaded({});

    expect(wrapper.find("table").exists()).toBe(true);
    expect(rows(wrapper).map((row) => row.props("id"))).toEqual(["a", "b"]);
    expect(rows(wrapper)[1].props("isActive")).toBe(false);
  });

  test("waits for the object to load before fetching", async () => {
    useObjectStore().is_loaded = false;
    const fetchSpy = mockFetch({ GET: { status: 200, body: links } });
    const wrapper = mountPublicLinks();
    await flushPromises();
    expect(fetchSpy).not.toHaveBeenCalled();

    useObjectStore().is_loaded = true;
    await flushPromises();

    expect(rows(wrapper)).toHaveLength(2);
  });

  test("creating a link posts it and adds a row", async () => {
    const { wrapper, fetchSpy } = await mountLoaded({
      POST: { status: 201, body: { id: "c", is_active: true } },
    });

    await wrapper.find(".public-link-buttons button").trigger("click");
    await flushPromises();

    const post = fetchSpy.mock.calls.find(([, i]) => i?.method === "POST");
    expect(post?.[0]).toBe("/api/v1/project/6/public_link/");
    expect(rows(wrapper).map((row) => row.props("id"))).toEqual(["a", "b", "c"]);
  });

  test("a failed create adds nothing", async () => {
    const { wrapper } = await mountLoaded({
      POST: { status: 400, body: { error: "Nope" } },
    });

    await wrapper.find(".public-link-buttons button").trigger("click");
    await flushPromises();

    expect(rows(wrapper)).toHaveLength(2);
  });

  test("deleting removes the row and calls DELETE", async () => {
    const { wrapper, fetchSpy } = await mountLoaded({});

    rows(wrapper)[0].vm.$emit("deleteLink", { id: "a" });
    await flushPromises();

    const del = fetchSpy.mock.calls.find(([, i]) => i?.method === "DELETE");
    expect(del?.[0]).toBe("/api/v1/project/6/public_link/a/");
    expect(rows(wrapper).map((row) => row.props("id"))).toEqual(["b"]);
  });

  test("a failed delete request is logged", async () => {
    const { wrapper, fetchSpy } = await mountLoaded({});
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });
    fetchSpy.mockRejectedValueOnce(new Error("offline"));

    rows(wrapper)[0].vm.$emit("deleteLink", { id: "a" });
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
  });

  test("toggling active flips the flag and PATCHes it", async () => {
    const { wrapper, fetchSpy } = await mountLoaded({});

    rows(wrapper)[1].vm.$emit("updateActive", { id: "b", index: 1 });
    await flushPromises();

    const patch = fetchSpy.mock.calls.find(([, i]) => i?.method === "PATCH");
    expect(patch?.[0]).toBe("/api/v1/project/6/public_link/b/");
    expect(JSON.parse(patch?.[1]?.body as string)).toEqual({ is_active: true });
    expect(rows(wrapper)[1].props("isActive")).toBe(true);
  });

  test("toggling an index that does not exist does nothing", async () => {
    const { wrapper, fetchSpy } = await mountLoaded({});

    rows(wrapper)[0].vm.$emit("updateActive", { id: "x", index: 9 });
    await flushPromises();

    expect(fetchSpy.mock.calls.some(([, i]) => i?.method === "PATCH")).toBe(false);
  });

  test("a failed toggle request is logged", async () => {
    const { wrapper, fetchSpy } = await mountLoaded({});
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });
    fetchSpy.mockRejectedValueOnce(new Error("offline"));

    rows(wrapper)[0].vm.$emit("updateActive", { id: "a", index: 0 });
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
  });
});
