import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import { useErrorStore } from "@/stores/error/error.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { AuditComponent } from ".";

const firstPage = {
  count: 3,
  next: "http://localhost/api/v1/project/3/audit/?page=2",
  previous: null,
  results: [
    {
      id: 3,
      date_created: "2026-01-03T10:00:00Z",
      username: "admin",
      action: "close",
      summary: "Closed",
      changes: { status: { old: "New", new: "Closed" } },
    },
    {
      id: 2,
      date_created: "2026-01-02T10:00:00Z",
      username: "team_leader",
      action: "update",
      summary: "Updated",
      changes: { description: { old: "", new: "Now described" } },
    },
  ],
};

const secondPage = {
  count: 3,
  next: null,
  previous: "http://localhost/api/v1/project/3/audit/",
  results: [
    {
      id: 1,
      date_created: "2026-01-01T10:00:00Z",
      username: "admin",
      action: "create",
      summary: "Created",
      changes: {},
    },
  ],
};

function mockFetch(pages: unknown[] = [firstPage, secondPage], status = 200) {
  let call = 0;
  return vi.spyOn(globalThis, "fetch").mockImplementation(() =>
    Promise.resolve({
      status,
      statusText: "Server exploded",
      json: () => Promise.resolve(structuredClone(pages[Math.min(call++, pages.length - 1)])),
    } as Response),
  );
}

describe("AuditComponent", () => {
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

  test("loads the first page of activity on mount", async () => {
    const fetchSpy = mockFetch();
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    expect(fetchSpy).toHaveBeenCalledWith(
      "/api/v1/project/3/audit/?page=1",
      expect.objectContaining({ method: "GET" }),
    );
    expect(wrapper.findAll(".audit-entry")).toHaveLength(2);
  });

  test("shows who, what happened and the old and new value", async () => {
    mockFetch();
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    const text = wrapper.find(".audit-entry").text();
    expect(text).toContain("Closed");
    expect(text).toContain("admin");
    expect(text).toContain("status");
    expect(text).toContain("New");
  });

  test("shows an empty value as a placeholder", async () => {
    mockFetch();
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    expect(wrapper.findAll(".audit-entry")[1]?.find(".old").text()).toBe("(empty)");
  });

  test("waits for the object to load before fetching", async () => {
    useObjectStore().is_loaded = false;
    const fetchSpy = mockFetch();

    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();
    expect(fetchSpy).not.toHaveBeenCalled();

    useObjectStore().is_loaded = true;
    await flushPromises();
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(wrapper.findAll(".audit-entry")).toHaveLength(2);
  });

  test("load more appends the next page and then hides the button", async () => {
    const fetchSpy = mockFetch();
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    await wrapper.find("button").trigger("click");
    await flushPromises();

    expect(fetchSpy).toHaveBeenLastCalledWith(
      "/api/v1/project/3/audit/?page=2",
      expect.anything(),
    );
    expect(wrapper.findAll(".audit-entry")).toHaveLength(3);
    expect(wrapper.find("button").exists()).toBe(false);
  });

  test("shows the empty message when nothing was recorded", async () => {
    mockFetch([{ count: 0, next: null, previous: null, results: [] }]);
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    expect(wrapper.find(".empty").exists()).toBe(true);
  });

  test("a forbidden response opens the error modal", async () => {
    mockFetch([{}], 403);
    mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    expect(useErrorStore().showErrorModal).toBe(true);
  });

  test("shows loading until the first request resolves", async () => {
    let resolveResponse!: (response: Response) => void;
    vi.spyOn(globalThis, "fetch").mockReturnValue(new Promise<Response>((resolve) => {
      resolveResponse = resolve;
    }));
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain(i18n.global.t("audit_component.loading"));
    expect(wrapper.find(".empty").exists()).toBe(false);
    resolveResponse({ status: 200, json: async () => structuredClone(secondPage) } as Response);
    await flushPromises();
    expect(wrapper.findAll(".audit-entry")).toHaveLength(1);
    expect(wrapper.text()).not.toContain(i18n.global.t("audit_component.loading"));
  });

  test("unknown actions and anonymous actors render without a changes list", async () => {
    const page = structuredClone(secondPage);
    page.results[0]!.action = "future_action";
    page.results[0]!.username = "";
    mockFetch([page]);
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    expect(wrapper.find("strong").text()).toBe("future_action");
    expect(wrapper.find(".audit-header > span").exists()).toBe(false);
    expect(wrapper.find(".audit-changes").exists()).toBe(false);
    expect(wrapper.find("time").attributes("datetime")).toBe(page.results[0]!.date_created);
  });

  test.each([
    [null, "(empty)"],
    ["", "(empty)"],
    [0, "0"],
    [false, "false"],
    [{ name: "Example" }, '{"name":"Example"}'],
    [[1, 2], "[1,2]"],
  ])("formats changed value %j as %s", async (value, expected) => {
    mockFetch([{
      ...secondPage,
      results: [{ ...secondPage.results[0], changes: { value: { old: value, new: value } } }],
    }]);
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    expect(wrapper.find(".old").text()).toBe(expected);
    expect(wrapper.find(".new").text()).toBe(expected);
  });

  test("server errors show their status text in the error store", async () => {
    mockFetch([{}], 500);
    const wrapper = mount(AuditComponent, { global: { plugins: [i18n] } });
    await flushPromises();

    expect(useErrorStore().showErrorModal).toBe(true);
    expect(useErrorStore().message).toBe("Server exploded");
    expect(wrapper.findAll(".audit-entry")).toHaveLength(0);
    expect(wrapper.text()).not.toContain(i18n.global.t("audit_component.loading"));
  });

});
