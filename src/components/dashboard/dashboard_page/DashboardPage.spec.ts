// DashboardPage.spec.ts
import {describe, test, expect} from "vitest";
import {DashboardPage} from ".";
import {flushPromises, mount} from "@vue/test-utils";
import {nextTick} from "vue";

describe("DashboardPage", () => {
    test("mounting component", () => {
        // Dashboard Page exists
        expect(DashboardPage).toBeTruthy();
    });
});

describe("DashboardPage - A11Y checks", () => {
    test("main title exists on page", async () => {
        // Mount the component
        const wrapper = mount(DashboardPage, {});

        // Wait for all promises to be completed
        await flushPromises();
        await nextTick();

        // Make sure there is only 1 <h1>, and one "main-title"
        const h1_elements = wrapper.findAll("h1");
        const main_title_elements = wrapper.findAll("#main-title");
        expect(h1_elements.length).toBe(1);
        expect(main_title_elements.length).toBe(1);
    });

    test("main title contains text", async () => {
        // Mount the component
        const wrapper = mount(DashboardPage, {});

        // Wait for all promises to be completed
        await flushPromises();
        await nextTick();

        // Make sure main-title contains text
        const main_title = wrapper.find("#main-title");
        expect(main_title.text()).not.toBe("");
    });
});
