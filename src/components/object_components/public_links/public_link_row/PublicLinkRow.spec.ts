import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {PublicLinkRow} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("PublicLinkRow", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders the link id when not copied", async () => {
    const wrapper = mount(PublicLinkRow, {
      props: {
        id: "123",
        isActive: false,
        index: 0,
      },
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check that the link id is rendered
    const linkElement = wrapper.find(".link");
    expect(linkElement.text()).toBe("123");
  });

  test("displays copied status after copying the link", async () => {
    const wrapper = mount(PublicLinkRow, {
      props: {
        id: "123",
        isActive: false,
        index: 0,
      },
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Click to copy the link
    const linkElement = wrapper.find(".link");
    await linkElement.trigger("click");

    // Check that the copied status is displayed
    const copiedStatusElement = wrapper.find(".copied-status");
    expect(copiedStatusElement.text()).toBe("Copied Public Link");

    // Wait for the status to disappear
    await nextTick();
    expect(copiedStatusElement.exists()).toBe(false);
  });

  test("emits updateActive when the active status icon is clicked", async () => {
    const wrapper = mount(PublicLinkRow, {
      props: {
        id: "123",
        isActive: false,
        index: 0,
      },
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Click the active status icon
    const activeStatusElement = wrapper.find("td:nth-child(2)");
    await activeStatusElement.trigger("click");

    // Check that the updateActive event is emitted
    expect(wrapper.emitted("updateActive")).toBeTruthy();
    expect(wrapper.emitted("updateActive")[0]).toEqual([{ id: "123", index: 0 }]);
  });

  test("emits deleteLink when the delete icon is clicked", async () => {
    const wrapper = mount(PublicLinkRow, {
      props: {
        id: "123",
        isActive: false,
        index: 0,
      },
      global: {
        plugins: [router, i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Click the delete icon
    const deleteElement = wrapper.find("td:nth-child(3)");
    await deleteElement.trigger("click");

    // Check that the deleteLink event is emitted
    expect(wrapper.emitted("deleteLink")).toBeTruthy();
    expect(wrapper.emitted("deleteLink")[0]).toEqual([{ id: "123" }]);
  });
});