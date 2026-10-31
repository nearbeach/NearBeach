import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { vi } from "vitest";
import {AssignedUsers} from ".";
import { useObjectStore } from "@/stores/object/object.ts";
import { nextTick } from "vue";

// The backend adds full_name to the users it sends - it is used as the option label
const user1 = { id: 1, username: "user1", first_name: "First", last_name: "Last", full_name: "First Last", email: "user1@example.com", profile_picture: "", profile_picture_path: "" };
const user2 = { id: 2, username: "user2", first_name: "Second", last_name: "User", full_name: "Second User", email: "user2@example.com", profile_picture: "", profile_picture_path: "" };

describe("AssignedUsers", () => {
  let objectStore: ReturnType<typeof useObjectStore>;

  beforeEach(() => {
    setActivePinia(createPinia());
    objectStore = useObjectStore();
    objectStore.destination = "project";
    objectStore.id = 1;

    // Mock fetch
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ({
        group_list: [],
        potential_user_list: [user1, user2],
        user_list: [],
      }),
    } as Response);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders assigned users", async () => {
    objectStore.user_list = [user1];

    const wrapper = mount(AssignedUsers);

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if the user is rendered
    const users = wrapper.findAll(".user-access-item");
    expect(users.length).toBe(1);
    expect(users.at(0)?.text()).toContain("First Last");
  });

  test("fetches the potential users once the object has loaded", async () => {
    const wrapper = mount(AssignedUsers);
    await flushPromises();

    // Nothing to add until the object has loaded
    expect(wrapper.find("select").exists()).toBe(false);

    objectStore.is_loaded = true;
    await flushPromises();
    await nextTick();

    expect(globalThis.fetch).toHaveBeenCalledWith("/api/v1/project/1/groups/", expect.any(Object));
    expect(objectStore.potential_user_list).toEqual([user1, user2]);
    expect(wrapper.findAll("option").map((option) => option.attributes("value"))).toEqual(["1", "2"]);
  });

  test("adds a user", async () => {
    objectStore.potential_user_list = [user1, user2];
    objectStore.user_list = [user1];

    const wrapper = mount(AssignedUsers);
    await flushPromises();

    // Only users who are not assigned yet can be picked
    expect(wrapper.findAll("option").map((option) => option.text())).toEqual(["Second User"]);

    // Pick user 2 from the AddObject select
    await wrapper.find("select").setValue("2");

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if the user is added to the list
    expect(objectStore.user_list.map((user) => user.id)).toEqual([1, 2]);
    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/v1/project/1/users/",
      expect.objectContaining({ body: JSON.stringify({ user_list: [2] }) }),
    );
  });

  test("removes a user", async () => {
    // Seed the store with a user
    objectStore.user_list = [user1];

    const wrapper = mount(AssignedUsers);
    await flushPromises();

    // Trigger the remove user event
    const removeIcon = wrapper.find(".user-access-item svg");
    await removeIcon.trigger("click");

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if the user is removed from the list
    expect(objectStore.user_list).toEqual([]);
    expect(wrapper.find(".user-access-list").exists()).toBe(false);
    expect(globalThis.fetch).toHaveBeenCalledWith("/api/v1/project/1/users/1/", expect.any(Object));
  });

  test("picking nothing does not call the backend", async () => {
    objectStore.potential_user_list = [user1, user2];
    const wrapper = mount(AssignedUsers);
    await flushPromises();
    vi.mocked(globalThis.fetch).mockClear();

    await wrapper.findComponent({ name: "AddObject" }).vm.$emit("change");
    await flushPromises();

    expect(globalThis.fetch).not.toHaveBeenCalled();
  });

  test("picking a user that is not in the potential list does nothing", async () => {
    objectStore.potential_user_list = [user1];
    const wrapper = mount(AssignedUsers);
    await flushPromises();
    vi.mocked(globalThis.fetch).mockClear();

    const addObject = wrapper.findComponent({ name: "AddObject" });
    addObject.vm.$emit("update:modelValue", 99);
    await addObject.vm.$emit("change");
    await flushPromises();

    expect(globalThis.fetch).not.toHaveBeenCalled();
    expect(objectStore.user_list).toEqual([]);
  });

  test("fetches the potential users when the object finishes loading", async () => {
    objectStore.is_loaded = false;
    mount(AssignedUsers);
    await flushPromises();
    expect(globalThis.fetch).not.toHaveBeenCalled();

    objectStore.is_loaded = true;
    await flushPromises();

    expect(globalThis.fetch).toHaveBeenCalledWith("/api/v1/project/1/groups/", expect.any(Object));
  });

  test("a failed add is logged", async () => {
    objectStore.potential_user_list = [user1, user2];
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });
    const wrapper = mount(AssignedUsers);
    await flushPromises();
    vi.mocked(globalThis.fetch).mockRejectedValue(new Error("offline"));

    await wrapper.find("select").setValue("2");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
  });

  test("a failed fetch of potential users is logged", async () => {
    vi.mocked(globalThis.fetch).mockRejectedValue(new Error("offline"));
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });
    mount(AssignedUsers);

    objectStore.is_loaded = true;
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
  });

  test("a failed remove is logged and the user is still removed locally", async () => {
    objectStore.user_list = [user1];
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => { /* Intentionally left empty */ });
    const wrapper = mount(AssignedUsers);
    await flushPromises();
    vi.mocked(globalThis.fetch).mockRejectedValue(new Error("offline"));

    await wrapper.find(".user-access-item svg").trigger("click");
    await flushPromises();

    expect(consoleError).toHaveBeenCalled();
    expect(objectStore.user_list).toEqual([]);
  });
});
