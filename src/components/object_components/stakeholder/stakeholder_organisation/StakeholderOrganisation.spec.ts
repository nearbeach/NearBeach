import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import { defineComponent, h } from "vue";
import { useObjectStore } from "@/stores/object/object.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import i18n from "@/i18n.ts";
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import { StakeholderOrganisation } from ".";

const organisation = {
  id: 3,
  name: "Acme",
  website: "",
  email: "",
  profile_picture_path: null,
  customers: null,
  potential_customers: null,
};

function mountOrganisation() {
  return mount(StakeholderOrganisation, {
    global: { plugins: [i18n], stubs: { RouterLink: defineComponent({ props: ["to"], setup: (props, { slots }) => () => h("a", { href: props.to }, slots.default?.()) }) } },
  });
}

async function choose(wrapper: ReturnType<typeof mountOrganisation>, id: number | null) {
  const add = wrapper.findComponent(AddObject);
  add.vm.$emit("update:modelValue", id);
  add.vm.$emit("change");
  await flushPromises();
}

describe("StakeholderOrganisation", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    usePermissionStore().currentObjectPermissions.currentObject = 2;
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 9;
    objectStore.organisation = null;
    useObjectMetaDataStore().potential_organisations = [
      { ...organisation, id: 3, name: "Acme" },
      { ...organisation, id: 4, name: "Globex" },
    ];
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("shows the organisation picker when none is set", () => {
    const wrapper = mountOrganisation();

    expect(wrapper.findComponent(AddObject).exists()).toBe(true);
    expect(wrapper.find(".organisation-name").exists()).toBe(false);
  });

  test("shows a link to the organisation when one is set", () => {
    useObjectStore().organisation = organisation;

    const wrapper = mountOrganisation();

    expect(wrapper.findComponent(AddObject).exists()).toBe(false);
    expect(wrapper.find(".organisation-name a").text()).toBe("Acme");
    expect(wrapper.find(".organisation-name a").attributes("href")).toBe("organisation/3");
  });

  test("choosing an organisation posts it and updates the stores", async () => {
    const customers = [{ id: 1 }];
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 201,
      json: () => Promise.resolve({ organisation, potential_customers: customers }),
    } as Response);
    const objectStore = useObjectStore();
    objectStore.customers = [{ id: 99 }] as never;
    const wrapper = mountOrganisation();

    await choose(wrapper, 3);

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/9/organisation/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("POST");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({ id: 3 });
    expect(objectStore.organisation).toEqual(organisation);
    expect(objectStore.customers).toEqual([]);
    expect(useObjectMetaDataStore().potential_customers).toEqual(customers);
    expect(wrapper.find(".organisation-name").exists()).toBe(true);
  });

  test("missing potential customers become an empty list", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 201,
      json: () => Promise.resolve({ organisation }),
    } as Response);
    useObjectMetaDataStore().potential_customers = [{ id: 1 }] as never;
    const wrapper = mountOrganisation();

    await choose(wrapper, 3);

    expect(useObjectMetaDataStore().potential_customers).toEqual([]);
  });

  test.each([[0], [null]])("choosing %s does nothing", async (value) => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const wrapper = mountOrganisation();

    await choose(wrapper, value);

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("a failed add shows the status text and leaves the organisation unset", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 500, statusText: "Server exploded" } as Response);
    const wrapper = mountOrganisation();

    await choose(wrapper, 3);

    expect(wrapper.text()).toContain("Server exploded");
    expect(useObjectStore().organisation).toBeNull();
  });

  test("a forbidden add shows the forbidden message", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 403 } as Response);
    const wrapper = mountOrganisation();

    await choose(wrapper, 3);

    expect(wrapper.text()).toContain(i18n.global.t("general_detail_component.error_forbidden"));
    expect(useObjectStore().organisation).toBeNull();
  });

  test("removing the organisation clears it and calls DELETE", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 204 } as Response);
    useObjectStore().organisation = organisation;
    const wrapper = mountOrganisation();

    await wrapper.find(".organisation-name svg").trigger("click");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/9/organisation/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("DELETE");
    expect(useObjectStore().organisation).toBeNull();
    expect(wrapper.findComponent(AddObject).exists()).toBe(true);
  });

  test("a failed removal restores the organisation and shows the status text", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 500, statusText: "Server exploded" } as Response);
    useObjectStore().organisation = organisation;
    const wrapper = mountOrganisation();

    await wrapper.find(".organisation-name svg").trigger("click");
    await flushPromises();

    expect(useObjectStore().organisation).toEqual(organisation);
    expect(wrapper.text()).toContain("Server exploded");
  });
});
