import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { WlkSelect } from "whelk-ui";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import ObjectPriority from "./ObjectPriority.vue";

function mountPriority() {
  return mount(ObjectPriority, { global: { plugins: [i18n] } });
}

describe("ObjectPriority", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "task";
    objectStore.id = 14;
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  test("offers the five priorities", () => {
    const wrapper = mountPriority();

    const options = wrapper.findComponent(WlkSelect).props("options") as { value: number; label: string }[];
    expect(options.map((o) => o.label)).toEqual(["Highest", "High", "Normal", "Low", "Lowest"]);
  });

  test("follows the priority held in the object store without saving", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const wrapper = mountPriority();

    useObjectStore().priority = { value: 2, label: "Normal" };
    await flushPromises();

    expect(wrapper.findComponent(WlkSelect).props("modelValue")).toBe("2");
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("choosing a priority updates the store, PATCHes it and clears the status", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout"] });
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200 } as Response);
    const wrapper = mountPriority();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("update:modelValue", "3");
    await flushPromises();

    expect(useObjectStore().priority).toEqual({ value: 3, label: "Low" });
    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/task/14/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("PATCH");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({ priority: "3" });
    expect(select.props("status")).toBe("Successfully updated priority");

    vi.advanceTimersByTime(5000);
    await flushPromises();

    expect(select.props("status")).toBe("");
  });

  test("an unknown priority shows an error and does not save", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});
    const wrapper = mountPriority();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("update:modelValue", "9");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(select.props("status")).toBe("Error Updating");
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("a failed save shows an error", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});
    const wrapper = mountPriority();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("update:modelValue", "1");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(select.props("status")).toBe("Error Updating");
  });

  test("choosing the priority already in the store does not save", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    useObjectStore().priority = { value: 4, label: "Lowest" };
    const wrapper = mountPriority();

    wrapper.findComponent(WlkSelect).vm.$emit("update:modelValue", "4");
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
