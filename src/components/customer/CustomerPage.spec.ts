import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { defineComponent, h } from "vue";
import { WlkSelect, WlkTextInput } from "whelk-ui";
import { useErrorStore } from "@/stores/error/error.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import i18n from "@/i18n.ts";
import CustomerPage from "./CustomerPage.vue";

const { pushMock } = vi.hoisted(() => ({ pushMock: vi.fn() }));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));

const RouterLinkStub = defineComponent({
  props: ["to"],
  setup: (props, { slots }) => () => h("a", { href: props.to }, slots.default?.()),
});

const customer = {
  id: 9,
  title: { id: 2, title: "Dr" },
  first_name: "Ada",
  last_name: "Lovelace",
  email: "ada@example.com",
  profile_picture: null,
};

function mockFetch(status: number, body: unknown = {}, statusText = "") {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    status,
    statusText,
    json: () => Promise.resolve(body),
  } as Response);
}

async function mountLoaded() {
  const fetchSpy = mockFetch(200, customer);
  const wrapper = mount(CustomerPage, {
    props: { id: "3", customerId: "9" },
    global: { plugins: [i18n], stubs: { RouterLink: RouterLinkStub } },
  });
  await flushPromises();
  fetchSpy.mockClear();
  return { wrapper, fetchSpy };
}

describe("CustomerPage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    useObjectMetaDataStore().customer_titles = [{ id: 1, title: "Mr" }, { id: 2, title: "Dr" }] as never;
    pushMock.mockReset();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  describe("loading the customer", () => {
    test("fetches the customer and fills in the form", async () => {
      const fetchSpy = mockFetch(200, customer);
      const wrapper = mount(CustomerPage, {
        props: { id: "3", customerId: "9" },
        global: { plugins: [i18n], stubs: { RouterLink: RouterLinkStub } },
      });
      await flushPromises();

      expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/organisation/3/customer/9/");
      expect(fetchSpy.mock.calls[0][1]?.method).toBe("GET");
      expect(wrapper.findComponent(WlkSelect).props("modelValue")).toBe(2);
      const [first, last, email] = wrapper.findAllComponents(WlkTextInput);
      expect(first.props("modelValue")).toBe("Ada");
      expect(last.props("modelValue")).toBe("Lovelace");
      expect(email.props("modelValue")).toBe("ada@example.com");
      expect(wrapper.find("button.primary").text()).toBe("Update Customer");
      expect(wrapper.find("button.primary").attributes("disabled")).toBeUndefined();
    });

    test("links back to the organisation", async () => {
      const { wrapper } = await mountLoaded();

      expect(wrapper.find("a").attributes("href")).toBe("/organisation/3/");
    });

    test("a 404 redirects to the not found page", async () => {
      mockFetch(404);
      mount(CustomerPage, {
        props: { id: "3", customerId: "9" },
        global: { plugins: [i18n], stubs: { RouterLink: RouterLinkStub } },
      });
      await flushPromises();

      expect(pushMock).toHaveBeenCalledWith({ name: "not-found" });
    });

    test("any other failure records the error and redirects to the server error page", async () => {
      mockFetch(500);
      mount(CustomerPage, {
        props: { id: "3", customerId: "9" },
        global: { plugins: [i18n], stubs: { RouterLink: RouterLinkStub } },
      });
      await flushPromises();

      expect(useErrorStore().message).not.toBe("");
      expect(pushMock).toHaveBeenCalledWith({ name: "server-error" });
    });
  });

  describe("updating", () => {
    test("an invalid field disables the update button", async () => {
      const { wrapper } = await mountLoaded();

      wrapper.findAllComponents(WlkTextInput)[0].vm.$emit("change", { isValid: false });
      await wrapper.vm.$nextTick();

      expect(wrapper.find("button.primary").attributes("disabled")).toBeDefined();
    });

    test("fixing the field enables the update button again", async () => {
      const { wrapper } = await mountLoaded();
      const first = wrapper.findAllComponents(WlkTextInput)[0];

      first.vm.$emit("change", { isValid: false });
      first.vm.$emit("change", { isValid: true });
      await wrapper.vm.$nextTick();

      expect(wrapper.find("button.primary").attributes("disabled")).toBeUndefined();
    });

    test("saves the edited details then resets the button after two seconds", async () => {
      const { wrapper, fetchSpy } = await mountLoaded();
      fetchSpy.mockResolvedValue({ status: 200 } as Response);
      vi.useFakeTimers({ toFake: ["setTimeout"] });

      wrapper.findAllComponents(WlkTextInput)[0].vm.$emit("update:modelValue", "Augusta");
      await wrapper.find("button.primary").trigger("click");
      await flushPromises();

      expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/organisation/3/customer/9/");
      expect(fetchSpy.mock.calls[0][1]?.method).toBe("PATCH");
      expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
        title: 2,
        first_name: "Augusta",
        last_name: "Lovelace",
        email: "ada@example.com",
      });
      expect(wrapper.find("button.primary").text()).toBe("Customer updated");
      expect(wrapper.find("button.primary").attributes("disabled")).toBeDefined();

      await vi.advanceTimersByTimeAsync(2000);

      expect(wrapper.find("button.primary").text()).toBe("Update Customer");
      expect(wrapper.find("button.primary").attributes("disabled")).toBeUndefined();
    });

    test("a failed save shows the error modal and stays disabled", async () => {
      const { wrapper, fetchSpy } = await mountLoaded();
      fetchSpy.mockResolvedValue({ status: 500, statusText: "Server error" } as Response);

      await wrapper.find("button.primary").trigger("click");
      await flushPromises();

      const errorStore = useErrorStore();
      expect(errorStore.message).toBe("Server error");
      expect(errorStore.showErrorModal).toBe(true);
      expect(wrapper.find("button.primary").attributes("disabled")).toBeDefined();
    });
  });
});
