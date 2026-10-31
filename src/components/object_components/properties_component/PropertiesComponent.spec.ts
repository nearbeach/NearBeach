import { beforeEach, describe, expect, test, afterEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { vi } from "vitest";
import {PropertiesComponent} from ".";
import { useErrorStore } from "@/stores/error/error.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import i18n from "@/i18n.ts";

// Mock the router
const { pushMock } = vi.hoisted(() => ({ pushMock: vi.fn() }));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));

describe("PropertiesComponent", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
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
            json: () => Promise.resolve({}),
        } as Response);
    }

    function lastBody(fetchSpy: ReturnType<typeof mockStatus>) {
        const calls = fetchSpy.mock.calls;
        return JSON.parse(calls[calls.length - 1][1]?.body as string);
    }

    beforeEach(() => {
        setActivePinia(createPinia());
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
        [403, "You do not have access to the object", false],
        [404, "Could not find the object", false],
        [500, "Server returned an error: ", true],
    ])("a %i response sets the error message", async (status, message, showModal) => {
        mockStatus(status);
        const errorStore = useErrorStore();
        const objectStore = useObjectStore();
        mountProperties();

        objectStore.end_date = "2026-05-10T10:00";
        await flushPromises();

        expect(errorStore.message).toBe(message);
        expect(errorStore.showErrorModal).toBe(showModal);
    });

    test("a network failure redirects to the server error page", async () => {
        vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
        const errorStore = useErrorStore();
        const objectStore = useObjectStore();
        mountProperties();

        objectStore.end_date = "2026-05-10T10:00";
        await flushPromises();

        expect(errorStore.message).toBe("offline");
        expect(pushMock).toHaveBeenCalledWith({ name: "server-error" });
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

    test("a story point error status is reported", async () => {
        vi.useFakeTimers();
        mockStatus(403);
        const errorStore = useErrorStore();
        const wrapper = mountProperties();

        wrapper.findComponent({ name: "WlkNumberInput" }).vm.$emit("change", { isValid: true });
        await vi.advanceTimersByTimeAsync(500);

        expect(errorStore.message).toBe("You do not have access to the object");
    });

    test("a story point network failure opens the error modal", async () => {
        vi.useFakeTimers();
        vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
        const errorStore = useErrorStore();
        const wrapper = mountProperties();

        wrapper.findComponent({ name: "WlkNumberInput" }).vm.$emit("change", { isValid: true });
        await vi.advanceTimersByTimeAsync(500);

        expect(errorStore.message).toBe("offline");
        expect(errorStore.showErrorModal).toBe(true);
    });
});

describe("PropertiesComponent - story point model", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
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
