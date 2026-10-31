import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { useObjectStore } from "@/stores/object/object.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import { GroupAccess } from ".";

const groupA = { id: 1, name: "Group A", parent_group: null };
const groupB = { id: 2, name: "Group B", parent_group: null };
const groupC = { id: 3, name: "Group C", parent_group: null };

function mockFetch(status: number, body: unknown) {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    status,
    json: () => Promise.resolve(body),
  } as Response);
}

describe("GroupAccess", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    const objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 5;
    objectStore.group_list = [groupA, groupB];
    useObjectMetaDataStore().all_groups = [groupA, groupB, groupC];
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("lists the object's groups", () => {
    const wrapper = mount(GroupAccess);

    const names = wrapper.findAll(".group-access-item p").map((p) => p.text());
    expect(names).toEqual(["Group A", "Group B"]);
  });

  test("hides the list when there are no groups", () => {
    useObjectStore().group_list = [];

    const wrapper = mount(GroupAccess);

    expect(wrapper.find(".group-access-list").exists()).toBe(false);
  });

  test("only offers the groups that are not already added", () => {
    const wrapper = mount(GroupAccess);

    expect(wrapper.findComponent(AddObject).props("options")).toEqual([groupC]);
  });

  test("shows a spacer instead of the picker when every group is added", () => {
    useObjectMetaDataStore().all_groups = [groupA, groupB];

    const wrapper = mount(GroupAccess);

    expect(wrapper.findComponent(AddObject).exists()).toBe(false);
    expect(wrapper.find(".space").exists()).toBe(true);
  });

  test("the last remaining group cannot be removed", () => {
    useObjectStore().group_list = [groupA];

    const wrapper = mount(GroupAccess);

    expect(wrapper.find('[aria-label="Remove group"]').exists()).toBe(false);
  });

  test("adding a group posts it and refreshes the users", async () => {
    const fetchSpy = mockFetch(201, {
      potential_user_list: [{ id: 7 }],
      user_list: [{ id: 8 }],
    });
    const objectStore = useObjectStore();
    const wrapper = mount(GroupAccess);

    wrapper.findComponent(AddObject).vm.$emit("update:modelValue", 3);
    await wrapper.findComponent(AddObject).vm.$emit("change");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/5/groups/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("POST");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({ group_list: [3] });
    expect(objectStore.group_list.map((g) => g.id)).toEqual([1, 2, 3]);
    expect(objectStore.potential_user_list).toEqual([{ id: 7 }]);
    expect(objectStore.user_list).toEqual([{ id: 8 }]);
  });

  test("adding with nothing selected does nothing", async () => {
    const fetchSpy = mockFetch(201, {});
    const wrapper = mount(GroupAccess);

    await wrapper.findComponent(AddObject).vm.$emit("change");
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("adding an unknown group does nothing", async () => {
    const fetchSpy = mockFetch(201, {});
    const wrapper = mount(GroupAccess);

    wrapper.findComponent(AddObject).vm.$emit("update:modelValue", 99);
    await wrapper.findComponent(AddObject).vm.$emit("change");
    await flushPromises();

    expect(fetchSpy).not.toHaveBeenCalled();
    expect(useObjectStore().group_list).toHaveLength(2);
  });

  test("a failed add shows the error message", async () => {
    mockFetch(400, "Group could not be added");
    const wrapper = mount(GroupAccess);

    wrapper.findComponent(AddObject).vm.$emit("update:modelValue", 3);
    await wrapper.findComponent(AddObject).vm.$emit("change");
    await flushPromises();

    expect(wrapper.text()).toContain("Group could not be added");
  });

  test("removing a group deletes it and refreshes the users", async () => {
    const fetchSpy = mockFetch(200, {
      potential_user_list: [{ id: 1 }],
      user_list: [{ id: 2 }],
    });
    const objectStore = useObjectStore();
    const wrapper = mount(GroupAccess);

    await wrapper.findAll('[aria-label="Remove group"]')[0].trigger("click");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/project/5/groups/1/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("DELETE");
    expect(objectStore.group_list.map((g) => g.id)).toEqual([2]);
    expect(objectStore.user_list).toEqual([{ id: 2 }]);
    expect(objectStore.potential_user_list).toEqual([{ id: 1 }]);
  });

  test("a failed removal shows the error message", async () => {
    mockFetch(403, "Not allowed");
    const wrapper = mount(GroupAccess);

    await wrapper.findAll('[aria-label="Remove group"]')[0].trigger("click");
    await flushPromises();

    expect(wrapper.text()).toContain("Not allowed");
  });
});
