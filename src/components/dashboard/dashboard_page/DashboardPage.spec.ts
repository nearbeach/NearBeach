// DashboardPage.spec.ts
import { describe, test, expect } from "vitest";
import DashboardPage from "./DashboardPage.vue";
import { flushPromises, mount } from "@vue/test-utils";

describe("DashboardPage", async () => {
  test("mounting component", async () => {
    // Dashboard Page exists
    expect(DashboardPage).toBeTruthy();
  });
});

describe("DashboardPage - A12Y checks", async () => {
  test("main title exists on page", async () => {
    // Mount the component
    const wrapper = mount(DashboardPage, {});

    // Wait for all promises to be completed
    await flushPromises();

    // Make sure there is only 1 <h1>, and one "main-title"
    const h1_elements = wrapper.findAll("h1");
    const main_title_elements = wrapper.findAll("#main-title");
    expect(h1_elements.length).toBe(1);
    expect(main_title_elements.length).toBe(1);

    // Unmount wrapper
    wrapper.unmount();
  });

  test("main title contains text", async () => {
    // Mount the component
    const wrapper = mount(DashboardPage, {});

    // Wait for all promises to be completed
    await flushPromises();

    // Make sure main-title contains text
    const main_title = wrapper.find("#main-title");
    expect(main_title.text()).not.toBe("");

    // Unmount wrapper
    wrapper.unmount();
  });
});
