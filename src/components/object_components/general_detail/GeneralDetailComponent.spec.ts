import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { useErrorStore } from "@/stores/error/error.ts";
import { GeneralDetailComponent } from ".";

const { pushMock, route } = vi.hoisted(() => ({
  pushMock: vi.fn(),
  route: { params: {} as Record<string, unknown>, meta: {} as Record<string, unknown> },
}));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));
vi.mock("vue-router", async (importOriginal) => ({
  ...(await importOriginal<typeof import("vue-router")>()),
  useRoute: () => route,
}));

function mockFetch(status: number, body: unknown = {}) {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    status,
    json: async () => body,
  } as Response);
}

function mountDetails() {
  return mount(GeneralDetailComponent, { global: { plugins: [i18n] } });
}

describe("GeneralDetailComponent", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    pushMock.mockReset();
    route.params = { id: "12" };
    route.meta = { destination: "project" };
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  describe("loading the object", () => {
    test("fetches the object and patches the store", async () => {
      const fetchSpy = mockFetch(200, { id: 12, title: "My project", description: "About" });
      const objectStore = useObjectStore();
      const wrapper = mountDetails();
      await flushPromises();

      expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/12/");
      expect(objectStore.id).toBe(12);
      expect(objectStore.title).toBe("My project");
      expect(objectStore.destination).toBe("project");
      expect(objectStore.is_loaded).toBe(true);
      expect(wrapper.find("h1").text()).toBe("Project Details");
    });

    test.each([
      ["a missing id", undefined],
      ["an array id", ["1", "2"]],
      ["a non-numeric id", "abc"],
      ["a decimal id", "1.5"],
    ])("does not fetch with %s", async (_label, id) => {
      route.params = { id };
      const fetchSpy = mockFetch(200);
      mountDetails();
      await flushPromises();

      expect(fetchSpy).not.toHaveBeenCalled();
    });

    test("does not fetch without a destination", async () => {
      route.meta = {};
      const fetchSpy = mockFetch(200);
      mountDetails();
      await flushPromises();

      expect(fetchSpy).not.toHaveBeenCalled();
    });

    test.each([
      [403, "forbidden"],
      [404, "not-found"],
      [500, "server-error"],
    ])("a %i response redirects to %s", async (status, name) => {
      mockFetch(status);
      mountDetails();
      await flushPromises();

      expect(pushMock).toHaveBeenCalledWith({ name });
    });

    test("a network failure records the error and redirects", async () => {
      vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
      const errorStore = useErrorStore();
      mountDetails();
      await flushPromises();

      expect(errorStore.message).toBe("offline");
      expect(pushMock).toHaveBeenCalledWith({ name: "server-error" });
    });
  });

  describe("updating", () => {
    async function mountLoaded() {
      const fetchSpy = mockFetch(200, { id: 12, title: "My project", description: "About" });
      const wrapper = mountDetails();
      await flushPromises();
      fetchSpy.mockClear();
      return { wrapper, fetchSpy };
    }

    test("the button starts enabled with the default label", async () => {
      const { wrapper } = await mountLoaded();

      const button = wrapper.find("button.primary");
      expect(button.text()).toBe("Update description and title");
      expect(button.attributes("disabled")).toBeUndefined();
    });

    test("saves the title and description then resets after two seconds", async () => {
      const { wrapper, fetchSpy } = await mountLoaded();
      vi.useFakeTimers({ toFake: ["setTimeout"] });

      // Hold the response so the in-progress state can be observed
      let release: (value: Response) => void = () => {};
      fetchSpy.mockReturnValue(new Promise<Response>((resolve) => (release = resolve)));

      await wrapper.find("button.primary").trigger("click");
      expect(wrapper.find("button.primary").text()).toBe("Please wait");
      expect(wrapper.find("button.primary").attributes("disabled")).toBeDefined();

      release({ status: 200, json: async () => ({}) } as Response);
      await flushPromises();

      expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/12/");
      expect(fetchSpy.mock.calls[0][1]?.method).toBe("PATCH");
      expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
        title: "My project",
        description: "About",
      });
      expect(wrapper.find("button.primary").text()).toBe("Your updates have been processed");

      vi.advanceTimersByTime(2000);
      await flushPromises();

      expect(wrapper.find("button.primary").text()).toBe("Update description and title");
    });

    test("shows an error and stays disabled when saving fails", async () => {
      const { wrapper, fetchSpy } = await mountLoaded();
      fetchSpy.mockRejectedValue(new Error("offline"));
      const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});

      await wrapper.find("button.primary").trigger("click");
      await flushPromises();

      expect(consoleError).toHaveBeenCalled();
      expect(wrapper.find("button.primary").text()).toBe("There was a problem updating");
      expect(wrapper.find("button.primary").attributes("disabled")).toBeDefined();
    });
  });
});
