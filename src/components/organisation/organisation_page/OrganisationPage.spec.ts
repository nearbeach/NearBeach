import { beforeEach, describe, expect, test, vi } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { WlkTabs } from "whelk-ui";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import i18n from "@/i18n.ts";
import OrganisationPage from "./OrganisationPage.vue";
import OrganisationInformation from "./organisation_information/OrganisationInformation.vue";

function mountPage() {
  return mount(OrganisationPage, {
    global: {
      plugins: [i18n],
      stubs: {
        OrganisationInformation: true,
        AssociatedCustomers: true,
        AssociatedObjects: true,
        DocumentComponent: true,
        NotesComponent: true,
      },
    },
  });
}

describe("OrganisationPage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("refreshes the organisation status options on mount", () => {
    const store = useObjectMetaDataStore();
    const updateSpy = vi.spyOn(store, "updateObjectStatus").mockImplementation(() => undefined);

    mountPage();

    expect(updateSpy).toHaveBeenCalledWith("organisation");
  });

  test("shows the organisation information", () => {
    const wrapper = mountPage();

    expect(wrapper.findComponent(OrganisationInformation).exists()).toBe(true);
  });

  test("offers the contacts, objects, documentation and notes tabs", () => {
    const wrapper = mountPage();

    const tabList = wrapper.findComponent(WlkTabs).props("tabList") as { label: string; for: string }[];
    expect(tabList.map((tab) => tab.for)).toEqual(["contacts", "associated_objects", "documentation", "notes"]);
    expect(tabList.map((tab) => tab.label)).toEqual(["Contacts", "Associated Objects", "Documentation", "Notes"]);
  });
});
