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

    test("calls removeCustomer action", async () => {
        const wrapper = mount(PropertiesComponent, {
            global: {
                plugins: [i18n],
            },
        });

        // Flush all promises
        await flushPromises();

        // Mock the removeCustomer action
        const store = useErrorStore();
        const removeCustomerSpy = vi.spyOn(store, "removeCustomer");

        // Trigger the removeCustomer action
        const customer_id = 1;
        wrapper.vm.removeCustomer(customer_id);

        // Check if the action was called with the correct customer_id
        expect(removeCustomerSpy).toHaveBeenCalledWith(customer_id);
    });

    test("calls removeGroup action", async () => {
        const wrapper = mount(PropertiesComponent, {
            global: {
                plugins: [i18n],
            },
        });

        // Flush all promises
        await flushPromises();

        // Mock the removeGroup action
        const store = useErrorStore();
        const removeGroupSpy = vi.spyOn(store, "removeGroup");

        // Trigger the removeGroup action
        const group_id = 1;
        wrapper.vm.removeGroup(group_id);

        // Check if the action was called with the correct group_id
        expect(removeGroupSpy).toHaveBeenCalledWith(group_id);
    });

    test("calls removeUser action", async () => {
        const wrapper = mount(PropertiesComponent, {
            global: {
                plugins: [i18n],
            },
        });

        // Flush all promises
        await flushPromises();

        // Mock the removeUser action
        const store = useErrorStore();
        const removeUserSpy = vi.spyOn(store, "removeUser");

        // Trigger the removeUser action
        const user_id = 1;
        wrapper.vm.removeUser(user_id);

        // Check if the action was called with the correct user_id
        expect(removeUserSpy).toHaveBeenCalledWith(user_id);
    });

    test("calls resetObject action", async () => {
        const wrapper = mount(PropertiesComponent, {
            global: {
                plugins: [i18n],
            },
        });

        // Flush all promises
        await flushPromises();

        // Mock the resetObject action
        const store = useErrorStore();
        const resetObjectSpy = vi.spyOn(store, "resetObject");

        // Trigger the resetObject action
        wrapper.vm.resetObject();

        // Check if the action was called
        expect(resetObjectSpy).toHaveBeenCalled();
    });

    test("getters availableUsersToAdd and fetchArrayOfGroupIds", async () => {
        const wrapper = mount(PropertiesComponent, {
            global: {
                plugins: [i18n],
            },
        });

        // Flush all promises
        await flushPromises();

        // Check availableUsersToAdd getter
        const availableUsers = wrapper.vm.availableUsersToAdd;
        expect(availableUsers).toBeInstanceOf(Array);

        // Check fetchArrayOfGroupIds getter
        const groupIds = wrapper.vm.fetchArrayOfGroupIds;
        expect(groupIds).toBeInstanceOf(Array);
    });
});