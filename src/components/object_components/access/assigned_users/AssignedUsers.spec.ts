import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { vi } from "vitest";
import AssignedUsers from "@/components/AssignedUsers.vue";
import { useObjectStore } from "@/stores/object/object.ts";
import { getCsrfToken } from "@/composables/getCsrfToken.ts";
import AddObject from "@/components/prefab/add_object/AddObject.vue";

describe("AssignedUsers", () => {
  let wrapper: any;
  let objectStore: any;

  beforeEach(() => {
    setActivePinia(createPinia());
    objectStore = useObjectStore();

    // Mock fetch
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ({
        group_list: [],
        potential_user_list: [
          { id: 1, username: "user1", first_name: "First", last_name: "Last", email: "user1@example.com", profile_picture: "", profile_picture_path: "" },
        ],
        user_list: [],
      }),
    } as Response);

    // Seed the store
    objectStore.is_loaded = true;
    objectStore.potential_user_list = [
      { id: 1, username: "user1", first_name: "First", last_name: "Last", email: "user1@example.com", profile_picture: "", profile_picture_path: "" },
    ];

    wrapper = mount(AssignedUsers, {
      global: {
        components: {
          AddObject,
        },
      },
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders assigned users", async () => {
    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if the user is rendered
    const user = wrapper.find(".user-list");
    expect(user.exists()).toBe(true);
    expect(user.text()).toContain("First Last");
  });

  test("adds a user", async () => {
    // Mock CSRF token
    Object.defineProperty(document, "cookie", {
      writable: true,
      value: "csrftoken=mockedtoken",
    });

    // Mock fetch for adding a user
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ({
        id: 1,
        username: "user1",
        first_name: "First",
        last_name: "Last",
        email: "user1@example.com",
        profile_picture: "",
        profile_picture_path: "",
      }),
    } as Response);

    // Trigger the add user event
    const addObject = wrapper.findComponent(AddObject);
    await addObject.vm.$emit("add", { id: 1, username: "user1", first_name: "First", last_name: "Last", email: "user1@example.com", profile_picture: "", profile_picture_path: "" });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if the user is added to the list
    const user = wrapper.find(".user-list");
    expect(user.exists()).toBe(true);
    expect(user.text()).toContain("First Last");
  });

  test("removes a user", async () => {
    // Mock CSRF token
    Object.defineProperty(document, "cookie", {
      writable: true,
      value: "csrftoken=mockedtoken",
    });

    // Seed the store with a user
    objectStore.user_list = [
      { id: 1, username: "user1", first_name: "First", last_name: "Last", email: "user1@example.com", profile_picture: "", profile_picture_path: "" },
    ];

    // Trigger the remove user event
    const user = wrapper.find(".user-list .remove-user");
    await user.trigger("click");

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if the user is removed from the list
    const userList = wrapper.find(".user-list");
    expect(userList.exists()).toBe(false);
  });
});