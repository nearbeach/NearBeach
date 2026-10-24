import { beforeEach, describe, expect, test, afterEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { vi } from "vitest";
import {PropertiesComponent} from ".";
import { useErrorStore } from "@/stores/error/error.ts";
import i18n from "@/i18n.ts";

// Mock the router
const { pushMock } = vi.hoisted(() => ({ pushMock: vi.fn() }));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));

describe("PropertiesComponent", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200, json: async () => ({}) } as Response);
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    test("mounting component", async () => {
        // Properties component exists
        expect(PropertiesComponent).toBeTruthy();
    });

    test("renders ObjectStatus and ObjectPriority components", async () => {
        const wrapper = mount(PropertiesComponent, {
            global: {
                plugins: [i18n],
            },
        });

        // Flush all promises
        await flushPromises();

        // Check if ObjectStatus and ObjectPriority components are rendered
        expect(wrapper.findComponent({ name: "ObjectStatus" }).exists()).toBe(true);
        expect(wrapper.findComponent({ name: "ObjectPriority" }).exists()).toBe(true);
    });
});