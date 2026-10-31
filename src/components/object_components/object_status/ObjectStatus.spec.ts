import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { WlkSelect } from "whelk-ui";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import ObjectStatus from "./ObjectStatus.vue";

const open = { id: 5, status: "Open", higher_order_status: { value: "open", label: "Open" } };
const done = { id: 6, status: "Done", higher_order_status: { value: "closed", label: "Closed" } };

function mountStatus() {
  return mount(ObjectStatus, { global: { plugins: [i18n] } });
}

describe("ObjectStatus", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 21;
    useObjectMetaDataStore().status = [open, done];
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  test("offers the statuses from the meta data store", () => {
    const wrapper = mountStatus();

    expect(wrapper.findComponent(WlkSelect).props("options")).toEqual([open, done]);
  });

  test("follows the status held in the object store without saving", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const wrapper = mountStatus();

    useObjectStore().status = open;
    await flushPromises();

    expect(wrapper.findComponent(WlkSelect).props("modelValue")).toBe("5");
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("choosing a status updates the store, PATCHes it and clears the message", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout"] });
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200 } as Response);
    const wrapper = mountStatus();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("update:modelValue", "6");
    await flushPromises();

    expect(useObjectStore().status).toEqual(done);
    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/21/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("PATCH");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({ status: "6" });
    expect(select.props("status")).toBe("Successfully updated status");

    vi.advanceTimersByTime(5000);
    await flushPromises();

    expect(select.props("status")).toBe("");
  });

  test("an unknown status is logged and not saved", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });
    const wrapper = mountStatus();

    wrapper.findComponent(WlkSelect).vm.$emit("update:modelValue", "99");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("a failed save shows an error", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });
    const wrapper = mountStatus();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("update:modelValue", "5");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(select.props("status")).toBe("Error Updating");
  });

  test("choosing the status already in the store does not save", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    useObjectStore().status = done;
    const wrapper = mountStatus();

    wrapper.findComponent(WlkSelect).vm.$emit("update:modelValue", "6");
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });
});

describe("ObjectStatus - no status chosen", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    useObjectMetaDataStore().status = [open, done];
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("going back to no status does not save", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200 } as Response);
    const wrapper = mountStatus();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("update:modelValue", "5");
    await flushPromises();
    fetchSpy.mockClear();

    select.vm.$emit("update:modelValue", "0");
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
