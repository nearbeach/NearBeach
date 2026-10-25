import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useObjectStore } from "@/stores/object/object.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import StakeholderOrganisation from "./stakeholder_organisation/StakeholderOrganisation.vue";
import StakeholderCustomer from "./stakeholder_customer/StakeholderCustomer.vue";
import StakeholderComponent from "./StakeholderComponent.vue";

const data = {
  customers: [{ id: 1 }],
  organisation: { id: 3, name: "Acme" },
  potential_customers: [{ id: 2 }],
  potential_organisations: [{ id: 4 }],
};

function mountStakeholders() {
  return mount(StakeholderComponent, {
    global: { stubs: { StakeholderOrganisation: true, StakeholderCustomer: true } },
  });
}

describe("StakeholderComponent", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 12;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders the organisation and customer sections", () => {
    const wrapper = mountStakeholders();

    expect(wrapper.find("h3").text()).toBe("Stakeholders");
    expect(wrapper.findComponent(StakeholderOrganisation).exists()).toBe(true);
    expect(wrapper.findComponent(StakeholderCustomer).exists()).toBe(true);
  });

  test("loads the stakeholders on mount when the object is loaded", async () => {
    useObjectStore().is_loaded = true;
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      json: async () => data,
    } as Response);
    mountStakeholders();
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/12/organisation/");
    expect(useObjectStore().customers).toEqual(data.customers);
    expect(useObjectStore().organisation).toEqual(data.organisation);
    expect(useObjectMetaDataStore().potential_customers).toEqual(data.potential_customers);
    expect(useObjectMetaDataStore().potential_organisations).toEqual(data.potential_organisations);
  });

  test("waits for the object to load before fetching", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      json: async () => data,
    } as Response);
    mountStakeholders();
    await flushPromises();
    expect(fetchSpy).not.toHaveBeenCalled();

    useObjectStore().is_loaded = true;
    await flushPromises();

    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(useObjectStore().organisation).toEqual(data.organisation);
  });

  test("missing potential lists become empty lists", async () => {
    useObjectStore().is_loaded = true;
    useObjectMetaDataStore().potential_customers = [{ id: 9 }] as never;
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      json: async () => ({ customers: [], organisation: null }),
    } as Response);
    mountStakeholders();
    await flushPromises();

    expect(useObjectMetaDataStore().potential_customers).toEqual([]);
    expect(useObjectMetaDataStore().potential_organisations).toEqual([]);
  });

  test("a failed load is logged", async () => {
    useObjectStore().is_loaded = true;
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});
    mountStakeholders();
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
  });
});
