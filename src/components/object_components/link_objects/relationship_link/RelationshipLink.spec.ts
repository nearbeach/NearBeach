import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { WlkSelect } from "whelk-ui";
import i18n from "@/i18n.ts";
import { useObjectStore } from "@/stores/object/object.ts";
import { RelationshipLink } from ".";

function mountLink(props: Record<string, unknown> = {}) {
  return mount(RelationshipLink, {
    props: {
      index: 1,
      objectAssignmentId: 40,
      objectId: 7,
      objectType: "task",
      relationship: "relates",
      reverseRelationship: false,
      ...props,
    },
    global: { plugins: [i18n] },
  });
}

describe("RelationshipLink", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 2;
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  test.each([
    ["block", false, "blocking"],
    ["block", true, "blocked_by"],
    ["Block", true, "blocked_by"],
    ["duplicate", false, "duplicate_object"],
    ["duplicate", true, "duplicate_object"],
    ["subobject", false, "parent_object_of"],
    ["subobject", true, "sub_object_of"],
    ["relates", false, "relates"],
    ["something else", true, "relates"],
  ])("relationship %s (reverse=%s) selects %s", async (relationship, reverseRelationship, expected) => {
    const wrapper = mountLink({ relationship, reverseRelationship });
    await wrapper.vm.$nextTick();

    expect(wrapper.findComponent(WlkSelect).props("modelValue")).toBe(expected);
  });

  test("offers all seven relationships", () => {
    const wrapper = mountLink();

    expect(wrapper.findComponent(WlkSelect).props("options")).toHaveLength(7);
  });

  test("changing the relationship PATCHes it, emits and clears the status", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout"] });
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200 } as Response);
    const wrapper = mountLink();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("update:modelValue", "blocking");
    select.vm.$emit("change");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/2/link_list/40/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("PATCH");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
      object_id: 7,
      object_relation: "blocking",
      object_type: "task",
    });
    expect(wrapper.emitted("updateRelationship")).toEqual([
      [{ index: 1, link_relationship: "blocking" }],
    ]);
    expect(select.props("status")).toBe("Successfully updated priority");

    vi.advanceTimersByTime(5000);
    await flushPromises();

    expect(select.props("status")).toBe("");
  });

  test("shows an error and does not emit when the request fails", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});
    const wrapper = mountLink();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("change");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(select.props("status")).toBe("Error Updating");
    expect(wrapper.emitted("updateRelationship")).toBeUndefined();
  });

  test("does nothing when the relationship is empty", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const wrapper = mountLink();
    const select = wrapper.findComponent(WlkSelect);

    select.vm.$emit("update:modelValue", "");
    select.vm.$emit("change");
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("does nothing for a negative index", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const wrapper = mountLink({ index: -1 });

    wrapper.findComponent(WlkSelect).vm.$emit("change");
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
