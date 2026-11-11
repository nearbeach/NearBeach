import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { defineComponent, h } from "vue";
import { WlkButton, WlkSelect, WlkTextInput } from "whelk-ui";
import { useErrorStore } from "@/stores/error/error.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import i18n from "@/i18n.ts";
import NewCustomer from "./NewCustomer.vue";

const { pushMock } = vi.hoisted(() => ({ pushMock: vi.fn() }));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));

const RouterLinkStub = defineComponent({
  props: ["to"],
  setup: (props, { slots }) => () => h("a", { href: props.to }, slots.default?.()),
});

function mockFetch(status: number, body: unknown = {}, statusText = "") {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    status,
    statusText,
    json: () => Promise.resolve(body),
  } as Response);
}

function mountForm() {
  return mount(NewCustomer, {
    props: { id: "3" },
    global: { plugins: [i18n], stubs: { RouterLink: RouterLinkStub } },
  });
}

// Fills the title select and the first name, last name and email inputs, and marks them valid
function fillForm(wrapper: ReturnType<typeof mountForm>) {
  const select = wrapper.findComponent(WlkSelect);
  const [first, last, email] = wrapper.findAllComponents(WlkTextInput);
  select.vm.$emit("update:modelValue", 2);
  first.vm.$emit("update:modelValue", "Ada");
  last.vm.$emit("update:modelValue", "Lovelace");
  email.vm.$emit("update:modelValue", "ada@example.com");
  for (const input of [select, first, last, email]) {
    input.vm.$emit("change", { isValid: true });
  }
}

describe("NewCustomer", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    useObjectMetaDataStore().customer_titles = [{ id: 1, title: "Mr" }, { id: 2, title: "Dr" }] as never;
    pushMock.mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders the heading, the title select and three inputs", () => {
    const wrapper = mountForm();

    expect(wrapper.find("h1").text()).toBe("Create Customer");
    expect(wrapper.findComponent(WlkSelect).props("options")).toHaveLength(2);
    expect(wrapper.findAllComponents(WlkTextInput)).toHaveLength(3);
  });

  test("the cancel button goes back to the organisation", () => {
    const wrapper = mountForm();

    const link = wrapper.find("a");
    expect(link.attributes("href")).toBe("/organisation/3/");
    expect(link.text()).toBe("Cancel");
  });

  test("the create button is disabled until every field is valid", async () => {
    const wrapper = mountForm();
    const button = wrapper.findComponent(".primary");
    expect(button.attributes("disabled")).toBeDefined();

    fillForm(wrapper);
    await wrapper.vm.$nextTick();

    expect(button.attributes("disabled")).toBeUndefined();
  });

  test("creating posts the details and redirects to the new customer", async () => {
    const fetchSpy = mockFetch(201, { id: 21 });
    const wrapper = mountForm();
    fillForm(wrapper);
    await wrapper.vm.$nextTick();

    await wrapper.findComponent(".primary").trigger("click");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/organisation/3/customer/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("POST");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
      title: 2,
      first_name: "Ada",
      last_name: "Lovelace",
      email: "ada@example.com",
    });
    expect(pushMock).toHaveBeenCalledWith("/organisation/3/customer/21/");
  });

  test("a 403 redirects to the forbidden page", async () => {
    mockFetch(403);
    const wrapper = mountForm();
    fillForm(wrapper);
    await wrapper.vm.$nextTick();

    await wrapper.findComponent(".primary").trigger("click");
    await flushPromises();

    expect(pushMock).toHaveBeenCalledWith({ name: "forbidden" });
  });

  test("any other failure records the error and redirects to the server error page", async () => {
    mockFetch(500, {}, "Internal Server Error");
    const wrapper = mountForm();
    fillForm(wrapper);
    await wrapper.vm.$nextTick();

    await wrapper.findComponent(".primary").trigger("click");
    await flushPromises();

    expect(useErrorStore().message).toBe("Internal Server Error");
    expect(pushMock).toHaveBeenCalledWith({ name: "server-error" });
  });
});
