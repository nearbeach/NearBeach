import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { defineComponent, h } from "vue";
import { useObjectStore } from "@/stores/object/object.ts";
import i18n from "@/i18n.ts";
import ProfilePicture from "@/components/prefab/profile_picture/ProfilePicture.vue";
import CustomerList from "./CustomerList.vue";

const RouterLinkStub = defineComponent({
  props: ["to"],
  setup: (props, { slots }) => () => h("a", { href: props.to }, slots.default?.()),
});

const customers = [
  { id: 1, title: { id: 1, title: "Mr" }, first_name: "Ada", last_name: "Lovelace", email: "ada@example.com", profile_picture: null },
  { id: 2, title: { id: 2, title: "Dr" }, first_name: "Alan", last_name: "Turing", email: "alan@example.com", profile_picture: "/media/alan.png" },
];

function mockFetch(status: number, body: unknown = {}, statusText = "") {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    status,
    statusText,
    json: () => Promise.resolve(body),
  } as Response);
}

function mountList() {
  return mount(CustomerList, { global: { plugins: [i18n], stubs: { RouterLink: RouterLinkStub } } });
}

describe("CustomerList", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    useObjectStore().id = 5;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("does not fetch until the object is loaded", async () => {
    const fetchSpy = mockFetch(200, { results: customers });

    mountList();
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("shows the empty message when there are no customers", () => {
    const wrapper = mountList();

    expect(wrapper.find(".empty-customer-list").text()).toBe("No customers associated with organisation");
    expect(wrapper.find(".customer-list").exists()).toBe(false);
  });

  test("fetches and renders the customers when the object is already loaded", async () => {
    const objectStore = useObjectStore();
    objectStore.is_loaded = true;
    const fetchSpy = mockFetch(200, { results: customers });

    const wrapper = mountList();
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/organisation/5/customer/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("GET");
    expect(objectStore.customers).toEqual(customers);
    expect(wrapper.findAll(".customer-item")).toHaveLength(2);
    expect(wrapper.findAll(".customer-item .name a")[0].text()).toBe("Mr Ada Lovelace");
    expect(wrapper.findAll(".customer-item .name a")[0].attributes("href")).toBe("/organisation/5/customer/1/");
    expect(wrapper.findAll(".customer-item .email")[1].text()).toContain("alan@example.com");
    expect(wrapper.findAllComponents(ProfilePicture)[1].props("url")).toBe("/media/alan.png");
  });

  test("fetches once the object finishes loading", async () => {
    const objectStore = useObjectStore();
    const fetchSpy = mockFetch(200, { results: customers });
    const wrapper = mountList();

    objectStore.is_loaded = true;
    await flushPromises();

    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(wrapper.findAll(".customer-item")).toHaveLength(2);
  });

  test("does not refetch when the customers are already in the store", async () => {
    const objectStore = useObjectStore();
    objectStore.customers = customers as never;
    const fetchSpy = mockFetch(200, { results: [] });
    mountList();

    objectStore.is_loaded = true;
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("a response without results becomes an empty list", async () => {
    const objectStore = useObjectStore();
    objectStore.is_loaded = true;
    mockFetch(200, {});

    mountList();
    await flushPromises();

    expect(objectStore.customers).toEqual([]);
  });

  test("a failed fetch shows the error message", async () => {
    const objectStore = useObjectStore();
    objectStore.is_loaded = true;
    mockFetch(500, {}, "Server error");

    const wrapper = mountList();
    await flushPromises();

    expect(objectStore.customers).toEqual([]);
    expect(wrapper.find(".empty-customer-list").exists()).toBe(true);
    expect(wrapper.text()).toContain("Server error");
  });
});
