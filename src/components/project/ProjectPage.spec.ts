import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {ProjectPage} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import i18n from "@/i18n.ts";
import { WlkTabs } from "whelk-ui";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("ProjectPage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders GeneralDetailComponent", async () => {
    const wrapper = mount(ProjectPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const generalDetailComponent = wrapper.findComponent({ name: "GeneralDetailComponent" });
    expect(generalDetailComponent.exists()).toBe(true);
  });

  test("renders PropertiesComponent twice", async () => {
    const wrapper = mount(ProjectPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const propertiesComponents = wrapper.findAllComponents({ name: "PropertiesComponent" });
    expect(propertiesComponents.length).toBe(2);
  });

  test("renders WlkTabs with correct tab headers", async () => {
    const wrapper = mount(ProjectPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const wlkTabs = wrapper.findComponent(WlkTabs);
    expect(wlkTabs.exists()).toBe(true);

    const tabHeaders = wlkTabs.props("tabList");
    expect(tabHeaders.length).toBe(4);
    expect(tabHeaders[0].label).toBe("Linked Objects");
    expect(tabHeaders[1].label).toBe("Documentation");
    expect(tabHeaders[2].label).toBe("Notes & Comments");
    expect(tabHeaders[3].label).toBe("Misc");
  });

  test("renders LinkObjects when 'Linked Objects' tab is selected", async () => {
    const wrapper = mount(ProjectPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const wlkTabs = wrapper.findComponent(WlkTabs);
    expect(wlkTabs.exists()).toBe(true);

    const linkObjectsTab = wlkTabs.find("button");
    await linkObjectsTab.trigger("click");

    const linkObjectsComponent = wrapper.findComponent({ name: "LinkObjects" });
    expect(linkObjectsComponent.exists()).toBe(true);
  });

  test("renders DocumentComponent when 'Documentation' tab is selected", async () => {
    const wrapper = mount(ProjectPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const wlkTabs = wrapper.findComponent(WlkTabs);
    expect(wlkTabs.exists()).toBe(true);

    const documentationTab = wlkTabs.findAll("button").at(1);
    await documentationTab?.trigger("click");

    const documentComponent = wrapper.findComponent({ name: "DocumentComponent" });
    expect(documentComponent.exists()).toBe(true);
  });

  test("renders NotesComponent when 'Notes & Comments' tab is selected", async () => {
    const wrapper = mount(ProjectPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const wlkTabs = wrapper.findComponent(WlkTabs);
    expect(wlkTabs.exists()).toBe(true);

    const notesTab = wlkTabs.findAll("button").at(2);
    await notesTab?.trigger("click");

    const notesComponent = wrapper.findComponent({ name: "NotesComponent" });
    expect(notesComponent.exists()).toBe(true);
  });

  test("renders PublicLinks and StakeholderComponent when 'Misc' tab is selected", async () => {
    const wrapper = mount(ProjectPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const wlkTabs = wrapper.findComponent(WlkTabs);
    expect(wlkTabs.exists()).toBe(true);

    const miscTab = wlkTabs.findAll("button").at(3);
    await miscTab?.trigger("click");

    const publicLinksComponent = wrapper.findComponent({ name: "PublicLinks" });
    expect(publicLinksComponent.exists()).toBe(true);

    const stakeholderComponent = wrapper.findComponent({ name: "StakeholderComponent" });
    expect(stakeholderComponent.exists()).toBe(true);
  });
});