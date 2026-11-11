import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { WlkTextInput } from "whelk-ui";
import { useErrorStore } from "@/stores/error/error.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import i18n from "@/i18n.ts";
import OrganisationInformation from "./OrganisationInformation.vue";

const { pushMock, route } = vi.hoisted(() => ({
  pushMock: vi.fn(),
  route: { params: {} as Record<string, unknown>, meta: {} as Record<string, unknown> },
}));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));
vi.mock("vue-router", async (importOriginal) => ({
  ...(await importOriginal<typeof import("vue-router")>()),
  useRoute: () => route,
}));

const organisation = { id: 12, name: "Acme", website: "https://acme.example.com", email: "hello@acme.example.com" };

function mockFetch(status: number, body: unknown = {}, statusText = "") {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    status,
    statusText,
    json: () => Promise.resolve(body),
  } as Response);
}

function mountInformation() {
  return mount(OrganisationInformation, { global: { plugins: [i18n] } });
}

async function mountLoaded() {
  const fetchSpy = mockFetch(200, organisation);
  const wrapper = mountInformation();
  await flushPromises();
  fetchSpy.mockClear();
  return { wrapper, fetchSpy };
}

describe("OrganisationInformation", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    pushMock.mockReset();
    route.params = { id: "12" };
    route.meta = { destination: "organisation" };
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  describe("loading the organisation", () => {
    test("fetches the organisation, fills in the name and marks the object loaded", async () => {
      const fetchSpy = mockFetch(200, organisation);
      const objectStore = useObjectStore();
      const wrapper = mountInformation();
      await flushPromises();

      expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/organisation/12/");
      expect(fetchSpy.mock.calls[0][1]?.method).toBe("GET");
      expect(objectStore.id).toBe(12);
      expect(objectStore.destination).toBe("organisation");
      expect(objectStore.is_loaded).toBe(true);
      expect(wrapper.find("h1").text()).toBe("Organisation Details");
      expect(wrapper.findAllComponents(WlkTextInput)[0].props("modelValue")).toBe("Acme");
      expect(wrapper.find("button.primary").text()).toBe("Update Organisation");
      expect(wrapper.find("button.primary").attributes("disabled")).toBeUndefined();
    });

    test.each([
      [403, "forbidden"],
      [404, "not-found"],
      [500, "server-error"],
    ])("a %i response redirects to %s", async (status, name) => {
      mockFetch(status);
      mountInformation();
      await flushPromises();

      expect(pushMock).toHaveBeenCalledWith({ name });
    });

    test.each([
      ["a non numeric id", { id: "abc" }, { destination: "organisation" }, "Invalid id"],
      ["a missing id", {}, { destination: "organisation" }, "Invalid id"],
      ["a decimal id", { id: "1.5" }, { destination: "organisation" }, "Invalid id - not set as an integer"],
      ["a missing destination", { id: "12" }, {}, "Invalid destination"],
    ])("%s redirects to bad request without fetching", async (_label, params, meta, message) => {
      const fetchSpy = mockFetch(200, organisation);
      route.params = params;
      route.meta = meta;

      mountInformation();
      await flushPromises();

      expect(fetchSpy).not.toHaveBeenCalled();
      expect(useErrorStore().message).toBe(message);
      expect(pushMock).toHaveBeenCalledWith({ name: "bad-request" });
    });
  });

  describe("updating", () => {
    test("an invalid field disables the update button", async () => {
      const { wrapper } = await mountLoaded();

      wrapper.findAllComponents(WlkTextInput)[0].vm.$emit("change", { isValid: false });
      await wrapper.vm.$nextTick();

      expect(wrapper.find("button.primary").attributes("disabled")).toBeDefined();
    });

    test("loads the website and email into their own inputs", async () => {
      const { wrapper } = await mountLoaded();

      const [name, website, email] = wrapper.findAllComponents(WlkTextInput);
      expect(name.props("modelValue")).toBe("Acme");
      expect(website.props("modelValue")).toBe("https://acme.example.com");
      expect(email.props("modelValue")).toBe("hello@acme.example.com");
    });

    test("editing the website and email does not change the name", async () => {
      const { wrapper, fetchSpy } = await mountLoaded();
      fetchSpy.mockResolvedValue({ status: 200 } as Response);

      const [, website, email] = wrapper.findAllComponents(WlkTextInput);
      website.vm.$emit("update:modelValue", "https://new.example.com");
      email.vm.$emit("update:modelValue", "new@example.com");
      await wrapper.find("button.primary").trigger("click");
      await flushPromises();

      expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
        name: "Acme",
        website: "https://new.example.com",
        email: "new@example.com",
      });
    });

    test("saves the details then resets the button after two seconds", async () => {
      const { wrapper, fetchSpy } = await mountLoaded();
      fetchSpy.mockResolvedValue({ status: 200 } as Response);
      vi.useFakeTimers({ toFake: ["setTimeout"] });

      wrapper.findAllComponents(WlkTextInput)[0].vm.$emit("update:modelValue", "Acme Ltd");
      await wrapper.find("button.primary").trigger("click");
      await flushPromises();

      expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/organisation/12/");
      expect(fetchSpy.mock.calls[0][1]?.method).toBe("PATCH");
      expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toMatchObject({ name: "Acme Ltd" });
      expect(wrapper.find("button.primary").text()).toBe("Organisation Updated");
      expect(wrapper.find("button.primary").attributes("disabled")).toBeDefined();

      await vi.advanceTimersByTimeAsync(2000);

      expect(wrapper.find("button.primary").text()).toBe("Update Organisation");
      expect(wrapper.find("button.primary").attributes("disabled")).toBeUndefined();
    });

    test("a 403 while saving redirects to the forbidden page", async () => {
      const { wrapper, fetchSpy } = await mountLoaded();
      fetchSpy.mockResolvedValue({ status: 403 } as Response);

      await wrapper.find("button.primary").trigger("click");
      await flushPromises();

      expect(pushMock).toHaveBeenCalledWith({ name: "forbidden" });
    });

    test("any other failure while saving records the error and redirects", async () => {
      const { wrapper, fetchSpy } = await mountLoaded();
      fetchSpy.mockResolvedValue({ status: 500, statusText: "Server error" } as Response);

      await wrapper.find("button.primary").trigger("click");
      await flushPromises();

      expect(useErrorStore().message).toBe("Server error");
      expect(pushMock).toHaveBeenCalledWith({ name: "server-error" });
    });
  });
});
