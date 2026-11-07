import { beforeEach, afterEach, describe, expect, test } from "vitest";
import i18n from "@/i18n.ts";
import { mount, flushPromises } from "@vue/test-utils";
import {StakeholderCustomer} from ".";
import { createPinia, setActivePinia } from "pinia";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import { createRouter, createMemoryHistory } from "vue-router";
import { vi } from "vitest";
import {defineComponent, h, nextTick} from "vue";
import { useObjectStore } from "@/stores/object/object.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: "/:catchAll(.*)*", component: defineComponent({ render: () => h("div") }) }],
});

const john = { id: 1, first_name: "John", last_name: "Doe", email: "john@example.com", title: { id: 0, title: "Mr"}};
const jane = { id: 2, first_name: "Jane", last_name: "Smith", email: "jane@example.com", title: { id: 1, title: "Mrs"}};

function mountStakeholderCustomer() {
  return mount(StakeholderCustomer, {
    global: {
      plugins: [router, i18n],
    },
  });
}

describe("StakeholderCustomer", () => {
  beforeEach(async () => {
    setActivePinia(createPinia());
    usePermissionStore().currentObjectPermissions.currentObject = 2;
    await router.push("/");
    await router.isReady();

    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 1;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders customer list", async () => {
    const objectStore = useObjectStore();
    objectStore.customers = [john, jane];

    const wrapper = mountStakeholderCustomer();

    await flushPromises();
    await nextTick();

    const customerList = wrapper.findAll(".customer-name");
    expect(customerList.length).toBe(2);
    expect(customerList.at(0)?.text()).toContain("John Doe");
    expect(customerList.at(1)?.text()).toContain("Jane Smith");
  });

  test("adds new customer", async () => {
    const objectStore = useObjectStore();
    const objectMetaDataStore = useObjectMetaDataStore();
    objectMetaDataStore.potential_customers = [john, jane];

    // The backend responds with the object's updated customer list
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 201,
      json: () => Promise.resolve([jane]),
    } as Response);

    const wrapper = mountStakeholderCustomer();

    await flushPromises();
    await nextTick();

    // Pick Jane from the AddObject select
    await wrapper.find("select").setValue("2");

    await flushPromises();
    await nextTick();

    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/v1/project/1/customer/",
      expect.objectContaining({ body: JSON.stringify({ id: 2 }) }),
    );
    expect(objectStore.customers).toEqual([jane]);

    const customerList = wrapper.findAll(".customer-name");
    expect(customerList.length).toBe(1);
    expect(customerList.at(0)?.text()).toContain("Jane Smith");
  });

  test("removes a customer", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 204 } as Response);
    const objectStore = useObjectStore();
    objectStore.customers = [john, jane];

    const wrapper = mountStakeholderCustomer();

    await flushPromises();
    await nextTick();

    // Click the trash icon next to John
    await wrapper.findAll(".customer-name").at(0)?.find("svg").trigger("click");

    await flushPromises();
    await nextTick();

    expect(globalThis.fetch).toHaveBeenCalledWith("/api/v1/project/1/customer/1/", expect.any(Object));
    const customerList = wrapper.findAll(".customer-name");
    expect(customerList.length).toBe(1);
    expect(customerList.at(0)?.text()).toContain("Jane Smith");
  });
});

describe("StakeholderCustomer - edge cases", () => {
  beforeEach(async () => {
    setActivePinia(createPinia());
    usePermissionStore().currentObjectPermissions.currentObject = 2;
    await router.push("/");
    await router.isReady();

    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 1;
    useObjectMetaDataStore().potential_customers = [john, jane];
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("choosing nothing does not call the backend", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const wrapper = mountStakeholderCustomer();
    await flushPromises();

    await wrapper.findComponent({ name: "AddObject" }).vm.$emit("change");
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test.each([
    [500, "Server exploded"],
    [403, i18n.global.t("general_detail_component.error_forbidden")],
  ])("a failed add (%s) leaves the customers unchanged and shows the message", async (status, message) => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status, statusText: "Server exploded" } as Response);
    useObjectStore().customers = [john];
    const wrapper = mountStakeholderCustomer();
    await flushPromises();

    await wrapper.find("select").setValue("2");
    await flushPromises();

    expect(useObjectStore().customers).toEqual([john]);
    expect(wrapper.text()).toContain(message);
  });

  test.each([
    [500, "Server exploded"],
    [403, i18n.global.t("general_detail_component.error_forbidden")],
  ])("a failed remove (%s) restores the customer and shows the message", async (status, message) => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status, statusText: "Server exploded" } as Response);
    useObjectStore().customers = [john, jane];
    const wrapper = mountStakeholderCustomer();
    await flushPromises();

    await wrapper.findAll(".customer-name").at(0)?.find("svg").trigger("click");
    await flushPromises();

    expect(useObjectStore().customers).toHaveLength(2);
    expect(wrapper.text()).toContain(message);
  });

  test("a network failure on remove restores the customer and shows the error", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
    useObjectStore().customers = [john, jane];
    const wrapper = mountStakeholderCustomer();
    await flushPromises();

    await wrapper.findAll(".customer-name").at(0)?.find("svg").trigger("click");
    await flushPromises();

    expect(useObjectStore().customers).toHaveLength(2);
    expect(wrapper.text()).toContain("offline");
  });
});
