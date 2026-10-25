import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useRoute } from "vue-router";
import { WlkCheckBox } from "whelk-ui";
import i18n from "@/i18n.ts";
import { useSearchStore } from "@/stores/search/search.ts";
import { useErrorStore } from "@/stores/error/error.ts";
import SearchFilter from "./SearchFilter.vue";

const { pushMock, route } = vi.hoisted(() => ({
  pushMock: vi.fn(),
  route: { meta: { destination: "project" } } as { meta: { destination: string } },
}));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));
vi.mock("vue-router", async (importOriginal) => {
  const actual = await importOriginal<typeof import("vue-router")>();
  const { reactive } = await import("vue");
  const reactiveRoute = reactive(route);
  return { ...actual, useRoute: () => reactiveRoute };
});

const results = { previous: null, next: 2, results: [{ id: 1, title: "Found" }] };

function mockFetch(status = 200, body: unknown = results, statusText = "") {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    status,
    statusText,
    json: async () => body,
  } as Response);
}

function mountFilter() {
  return mount(SearchFilter, { global: { plugins: [i18n] } });
}

describe("SearchFilter", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    pushMock.mockReset();
    route.meta.destination = "project";
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  test("searches on mount and stores the results", async () => {
    const fetchSpy = mockFetch();
    mountFilter();
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/?search=&show_closed=false");
    const store = useSearchStore();
    expect(store.searchResults).toEqual(results.results);
    expect(store.next).toBe(2);
    expect(store.previous).toBeNull();
  });

  test("the title and placeholder follow the destination", async () => {
    mockFetch();
    const wrapper = mountFilter();
    await flushPromises();

    expect(wrapper.find("h1").text()).toBe("Search Project");
    expect(wrapper.find("input[type=search]").attributes("placeholder")).toBe("Search for a project");
  });

  test("typing searches after a short pause", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout", "clearTimeout"] });
    const fetchSpy = mockFetch();
    const wrapper = mountFilter();
    await flushPromises();
    fetchSpy.mockClear();

    const input = wrapper.find("input[type=search]");
    await input.setValue("report");
    await input.trigger("keydown");
    vi.advanceTimersByTime(499);
    expect(fetchSpy).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1);
    await flushPromises();

    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/?search=report&show_closed=false");
  });

  test("another keypress restarts the pause", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout", "clearTimeout"] });
    const fetchSpy = mockFetch();
    const wrapper = mountFilter();
    await flushPromises();
    fetchSpy.mockClear();

    const input = wrapper.find("input[type=search]");
    await input.setValue("repo");
    await input.trigger("keydown");
    vi.advanceTimersByTime(400);
    await input.trigger("keydown");
    vi.advanceTimersByTime(400);
    expect(fetchSpy).not.toHaveBeenCalled();

    vi.advanceTimersByTime(100);
    await flushPromises();

    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  test("a short text search does not run", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout", "clearTimeout"] });
    const fetchSpy = mockFetch();
    const wrapper = mountFilter();
    await flushPromises();
    fetchSpy.mockClear();

    const input = wrapper.find("input[type=search]");
    await input.setValue("ab");
    await input.trigger("keydown");
    vi.advanceTimersByTime(500);
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("a short numeric search does run", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout", "clearTimeout"] });
    const fetchSpy = mockFetch();
    const wrapper = mountFilter();
    await flushPromises();
    fetchSpy.mockClear();

    const input = wrapper.find("input[type=search]");
    await input.setValue("12");
    await input.trigger("keydown");
    vi.advanceTimersByTime(500);
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/?search=12&show_closed=false");
  });

  test("ticking show closed searches straight away", async () => {
    const fetchSpy = mockFetch();
    const wrapper = mountFilter();
    await flushPromises();
    fetchSpy.mockClear();

    const checkbox = wrapper.findComponent(WlkCheckBox);
    checkbox.vm.$emit("update:modelValue", true);
    checkbox.vm.$emit("change");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/?search=&show_closed=true");
  });

  test("changing destination clears the search and results then searches again", async () => {
    const fetchSpy = mockFetch();
    const wrapper = mountFilter();
    await flushPromises();
    await wrapper.find("input[type=search]").setValue("report");
    fetchSpy.mockClear();
    useSearchStore().searchResults = [{ id: 9 }] as never;
    fetchSpy.mockResolvedValue({
      status: 200,
      json: async () => ({ previous: null, next: null, results: [] }),
    } as Response);

    // Change it through the mocked (reactive) route so the watcher fires
    useRoute().meta.destination = "task";
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/task/?search=&show_closed=false");
    expect((wrapper.find("input[type=search]").element as HTMLInputElement).value).toBe("");
    expect(useSearchStore().searchResults).toEqual([]);
    expect(wrapper.find("h1").text()).toBe("Search Task");
  });

  test("a failed search records the error and shows the server error page", async () => {
    mockFetch(500, {}, "Internal Server Error");
    mountFilter();
    await flushPromises();

    expect(useErrorStore().message).toBe("Internal Server Error");
    expect(pushMock).toHaveBeenCalledWith({ name: "server-error" });
  });
});
