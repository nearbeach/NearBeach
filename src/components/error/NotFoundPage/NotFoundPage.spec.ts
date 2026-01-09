// NotFound.spec.ts
import { describe, test, expect } from "vitest";
import NotFoundPage from "./NotFoundPage.vue";
import { flushPromises, mount } from "@vue/test-utils";
import DashboardPage from "@/components/dashboard/dashboard_page/DashboardPage.vue";

describe("NotFound", async () => {
  // Mount the wrapper
  const wrapper = mount(NotFoundPage, {});

  test("mount component", async () => {
    // App exists
    expect(NotFoundPage).toBeTruthy();
  });

  test("make sure we have landed on the correct not found page", () => {
    const heading = wrapper.find("h1");
    expect(heading?.text()).toBe("404 Not Found");
  });
});

describe("NotFound - A12Y checks", async () => {
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
