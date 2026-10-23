import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import i18n from "@/i18n.ts";
import {BreadCrumbs} from ".";
import {nextTick} from "vue";

describe("BreadCrumbs", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders root label when breadCrumbsArray is empty", async () => {
    const wrapper = mount(BreadCrumbs, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const rootLabel = wrapper.find(".root-label");
    expect(rootLabel.text()).toBe("Root");
  });

  test("renders navigation buttons when breadCrumbsArray is not empty", async () => {
    const store = useDocumentationStore();
    store.breadCrumbsArray = [
      { label: "Folder 1", folderId: 1 },
      { label: "Folder 2", folderId: 2 },
    ];

    const wrapper = mount(BreadCrumbs, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const navigationButtons = wrapper.findAll(".navigation-button");
    expect(navigationButtons.length).toBe(2);
    expect(navigationButtons.at(0)?.text()).toBe("Folder 1");
    expect(navigationButtons.at(1)?.text()).toBe("Folder 2");
  });

  test("goes back to previous folder when navigation button is clicked", async () => {
    const store = useDocumentationStore();
    store.breadCrumbsArray = [
      { label: "Folder 1", folderId: 1 },
      { label: "Folder 2", folderId: 2 },
    ];

    const wrapper = mount(BreadCrumbs, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const navigationButton = wrapper.find(".navigation-button");
    await navigationButton.trigger("click");

    await flushPromises();
    await nextTick();

    expect(store.breadCrumbsArray.length).toBe(1);
    expect(store.breadCrumbsArray[0].label).toBe("Folder 1");
  });

  test("goes back to root when root label is clicked", async () => {
    const store = useDocumentationStore();
    store.breadCrumbsArray = [
      { label: "Folder 1", folderId: 1 },
      { label: "Folder 2", folderId: 2 },
    ];

    const wrapper = mount(BreadCrumbs, {
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const rootLabel = wrapper.find(".root-label");
    await rootLabel.trigger("click");

    await flushPromises();
    await nextTick();

    expect(store.breadCrumbsArray.length).toBe(0);
  });
});