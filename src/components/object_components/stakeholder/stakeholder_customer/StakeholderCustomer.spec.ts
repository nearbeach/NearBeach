import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {StakeholderCustomer} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import { vi } from "vitest";
import { nextTick } from "vue";
import { useObjectStore } from "@/stores/object/object.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: "/", component: defineComponent({ render: () => h("div") }) }],
});

describe("StakeholderCustomer", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    router.push("/");
    router.isReady();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders customer list", async () => {
    const objectStore = useObjectStore();
    const objectMetaDataStore = useObjectMetaDataStore();

    objectStore.customers = [
      { id: 1, first_name: "John", last_name: "Doe", email: "john@example.com" },
      { id: 2, first_name: "Jane", last_name: "Smith", email: "jane@example.com" },
    ];

    const wrapper = mount(StakeholderCustomer, {
      global: {
        plugins: [router],
      },
    });

    await flushPromises();
    await nextTick();

    const customerList = wrapper.findAll(".customer-list-item");
    expect(customerList.length).toBe(2);
    expect(customerList.at(0)?.text()).toContain("John Doe");
    expect(customerList.at(1)?.text()).toContain("Jane Smith");
  });

  test("adds new customer", async () => {
    const objectStore = useObjectStore();
    const objectMetaDataStore = useObjectMetaDataStore();

    objectMetaDataStore.potential_customers = [
      { id: 1, first_name: "Alice", last_name: "Johnson", email: "alice@example.com" },
    ];

    const wrapper = mount(StakeholderCustomer, {
      global: {
        plugins: [router],
      },
    });

    await flushPromises();
    await nextTick();

    const addCustomerButton = wrapper.find(".add-customer-button");
    await addCustomerButton.trigger("click");

    await flushPromises();
    await nextTick();

    const customerList = wrapper.findAll(".customer-list-item");
    expect(customerList.length).toBe(1);
    expect(customerList.at(0)?.text()).toContain("Alice Johnson");
  });

  test("fetches customers on mount", async () => {
    const objectStore = useObjectStore();
    const objectMetaDataStore = useObjectMetaDataStore();

    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ({
        customers: [
          { id: 1, first_name: "John", last_name: "Doe", email: "john@example.com" },
        ],
      }),
    } as Response);

    const wrapper = mount(StakeholderCustomer, {
      global: {
        plugins: [router],
      },
    });

    await flushPromises();
    await nextTick();

    expect(fetch).toHaveBeenCalledWith("/api/customers");
    expect(objectStore.customers.length).toBe(1);
  });
});