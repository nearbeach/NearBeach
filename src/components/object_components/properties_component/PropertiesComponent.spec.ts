import { beforeEach, describe, expect, test, afterEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import { vi } from "vitest";
import {PropertiesComponent} from ".";
import { useObjectStore } from "@/stores/object/object.ts";
import i18n from "@/i18n.ts";

// Mock the router
const { pushMock } = vi.hoisted(() => ({ pushMock: vi.fn() }));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));

describe("PropertiesComponent", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        usePermissionStore().currentObjectPermissions.currentObject = 2;
        vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200, json: () => Promise.resolve({}) } as Response);
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    test("mounting component", () => {
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
describe("PropertiesComponent - updating", () => {
    function mountProperties() {
        return mount(PropertiesComponent, { global: { plugins: [i18n] } });
    }

    function mockStatus(status: number) {
        return vi.spyOn(globalThis, "fetch").mockResolvedValue({
            status,
            statusText: "Server exploded",
            json: () => Promise.resolve({}),
        } as Response);
    }

    function lastBody(fetchSpy: ReturnType<typeof mockStatus>) {
        const calls = fetchSpy.mock.calls;
        return JSON.parse(calls[calls.length - 1][1]?.body as string);
    }

    beforeEach(() => {
        setActivePinia(createPinia());
        usePermissionStore().currentObjectPermissions.currentObject = 2;
        pushMock.mockReset();
        const objectStore = useObjectStore();
        objectStore.destination = "project";
        objectStore.id = 4;
    });

    afterEach(() => {
        vi.useRealTimers();
        vi.restoreAllMocks();
    });

    test("setting only an end date copies it to the start date and saves", async () => {
        const fetchSpy = mockStatus(200);
        const objectStore = useObjectStore();
        mountProperties();

        objectStore.end_date = "2026-05-10T10:00";
        await flushPromises();

        expect(objectStore.start_date).toBe("2026-05-10T10:00");
        expect(fetchSpy).toHaveBeenCalledTimes(1);
        expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/4/");
        expect(fetchSpy.mock.calls[0][1]?.method).toBe("PATCH");
        expect(lastBody(fetchSpy)).toEqual({
            end_date: "2026-05-10T10:00",
            start_date: "2026-05-10T10:00",
        });
    });

    test("setting only a start date copies it to the end date and saves", async () => {
        const fetchSpy = mockStatus(200);
        const objectStore = useObjectStore();
        mountProperties();

        objectStore.start_date = "2026-05-01T09:00";
        await flushPromises();

        expect(objectStore.end_date).toBe("2026-05-01T09:00");
        expect(lastBody(fetchSpy)).toEqual({
            end_date: "2026-05-01T09:00",
            start_date: "2026-05-01T09:00",
        });
    });

    test("an end date before the start date pulls the start date back", async () => {
        const objectStore = useObjectStore();
        objectStore.start_date = "2026-05-10T10:00";
        objectStore.end_date = "2026-05-20T10:00";
        const fetchSpy = mockStatus(200);
        mountProperties();

        objectStore.end_date = "2026-05-05T10:00";
        await flushPromises();

        expect(objectStore.start_date).toBe("2026-05-05T10:00");
        expect(lastBody(fetchSpy).start_date).toBe("2026-05-05T10:00");
    });

    test("a start date after the end date pushes the end date forward", async () => {
        const objectStore = useObjectStore();
        objectStore.start_date = "2026-05-10T10:00";
        objectStore.end_date = "2026-05-20T10:00";
        const fetchSpy = mockStatus(200);
        mountProperties();

        objectStore.start_date = "2026-06-01T10:00";
        await flushPromises();

        expect(objectStore.end_date).toBe("2026-06-01T10:00");
        expect(lastBody(fetchSpy).end_date).toBe("2026-06-01T10:00");
    });

    test("an invalid date is ignored", async () => {
        const fetchSpy = mockStatus(200);
        const objectStore = useObjectStore();
        mountProperties();

        objectStore.end_date = "not a date";
        objectStore.start_date = "also not a date";
        await flushPromises();

        expect(fetchSpy).not.toHaveBeenCalled();
    });

    test("the date status clears two seconds after saving", async () => {
        vi.useFakeTimers();
        mockStatus(200);
        const objectStore = useObjectStore();
        const wrapper = mountProperties();

        objectStore.end_date = "2026-05-10T10:00";
        await flushPromises();
        expect(wrapper.text()).toContain("Date updated");

        vi.advanceTimersByTime(2000);
        await flushPromises();

        expect(wrapper.text()).not.toContain("Date updated");
    });

    test.each([
        [403, i18n.global.t("general_detail_component.error_forbidden")],
        [404, "Server exploded"],
        [500, "Server exploded"],
    ])("a %i response shows the date status message", async (status, message) => {
        mockStatus(status);
        const objectStore = useObjectStore();
        const wrapper = mountProperties();

        objectStore.end_date = "2026-05-10T10:00";
        await flushPromises();

        expect(wrapper.text()).toContain(message);
        expect(wrapper.text()).not.toContain("Date updated");
    });

    test("a network failure while saving dates shows the error message", async () => {
        vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
        const objectStore = useObjectStore();
        const wrapper = mountProperties();

        objectStore.end_date = "2026-05-10T10:00";
        await flushPromises();

        expect(wrapper.text()).toContain("offline");
    });

    test("a network failure while saving story points shows the error message", async () => {
        vi.useFakeTimers();
        vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
        const wrapper = mountProperties();

        wrapper.findComponent({ name: "WlkNumberInput" }).vm.$emit("change", { isValid: true });
        await vi.advanceTimersByTimeAsync(500);

        expect(wrapper.text()).toContain("offline");
    });

    test("valid story points are saved after a short delay", async () => {
        vi.useFakeTimers();
        const fetchSpy = mockStatus(200);
        const objectStore = useObjectStore();
        objectStore.story_point = 3;
        const wrapper = mountProperties();
        const input = wrapper.findComponent({ name: "WlkNumberInput" });

        input.vm.$emit("change", { isValid: true });
        await flushPromises();
        expect(wrapper.text()).toContain("Updating story points");
        expect(fetchSpy).not.toHaveBeenCalled();

        await vi.advanceTimersByTimeAsync(500);

        expect(fetchSpy).toHaveBeenCalledTimes(1);
        expect(lastBody(fetchSpy)).toEqual({ story_point: 3 });
        expect(wrapper.text()).toContain("Story points updated");

        await vi.advanceTimersByTimeAsync(2000);
        expect(wrapper.text()).not.toContain("Story points updated");
    });

    test("quick story point changes are saved once", async () => {
        vi.useFakeTimers();
        const fetchSpy = mockStatus(200);
        const wrapper = mountProperties();
        const input = wrapper.findComponent({ name: "WlkNumberInput" });

        input.vm.$emit("change", { isValid: true });
        await vi.advanceTimersByTimeAsync(300);
        input.vm.$emit("change", { isValid: true });
        await vi.advanceTimersByTimeAsync(300);
        expect(fetchSpy).not.toHaveBeenCalled();

        await vi.advanceTimersByTimeAsync(200);

        expect(fetchSpy).toHaveBeenCalledTimes(1);
    });

    test("an invalid change cancels the pending story point save", async () => {
        vi.useFakeTimers();
        const fetchSpy = mockStatus(200);
        const wrapper = mountProperties();
        const input = wrapper.findComponent({ name: "WlkNumberInput" });

        input.vm.$emit("change", { isValid: true });
        await vi.advanceTimersByTimeAsync(200);
        input.vm.$emit("change", { isValid: false });
        await vi.advanceTimersByTimeAsync(1000);

        expect(fetchSpy).not.toHaveBeenCalled();
        expect(wrapper.text()).toContain("Invalid story points");
    });

    test("invalid story points show a message and are not saved", async () => {
        vi.useFakeTimers();
        const fetchSpy = mockStatus(200);
        const wrapper = mountProperties();
        const input = wrapper.findComponent({ name: "WlkNumberInput" });

        input.vm.$emit("change", { isValid: false });
        await vi.advanceTimersByTimeAsync(1000);

        expect(wrapper.text()).toContain("Invalid story points");
        expect(fetchSpy).not.toHaveBeenCalled();
    });

    test.each([
        [403, i18n.global.t("general_detail_component.error_forbidden")],
        [500, "Server exploded"],
    ])("a story point %i response shows the status message", async (status, message) => {
        vi.useFakeTimers();
        mockStatus(status);
        const wrapper = mountProperties();

        wrapper.findComponent({ name: "WlkNumberInput" }).vm.$emit("change", { isValid: true });
        await vi.advanceTimersByTimeAsync(500);

        expect(wrapper.text()).toContain(message);
        expect(wrapper.text()).not.toContain("Story points updated");
    });
});

describe("PropertiesComponent - story point model", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
        usePermissionStore().currentObjectPermissions.currentObject = 2;
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    test("the story points input is bound to the object store", async () => {
        vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200, json: () => Promise.resolve({}) } as Response);
        const wrapper = mount(PropertiesComponent, { global: { plugins: [i18n] } });
        const input = wrapper.findComponent({ name: "WlkNumberInput" });

        input.vm.$emit("update:modelValue", 4);
        await flushPromises();

        expect(useObjectStore().story_point).toBe(4);
    });
});
