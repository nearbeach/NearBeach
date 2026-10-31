import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import router, { routes } from "@/router/router.ts";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import { useObjectMetaDataStore } from "@/stores/object_meta_data/object_meta_data.ts";
import { useUserStore } from "@/stores/user/user.ts";
import { useErrorStore } from "@/stores/error/error.ts";
import { useDocumentationStore } from "@/stores/documentation/documentation.ts";
import { useObjectStore } from "@/stores/object/object.ts";

const initialData = {
  permissions: [
    {
      group_id: 1,
      group_name: "Everyone",
      project: 2,
      administration_create_user: 1,
    },
  ],
  all_groups: [{ id: 1, name: "Everyone", parent_group: null }],
  object_status: { project: [] },
  object_types: { requirement: [] },
  tags: [{ id: 1, name: "tag" }],
  id: 11,
  username: "luke",
  first_name: "Luke",
  last_name: "Skywalker",
  email: "luke@example.com",
  profile_picture: "pic.png",
  profile_picture_path: "/media/pic.png",
};

function mockInitialData(ok = true, status = 200) {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    ok,
    status,
    json: () => Promise.resolve(initialData),
  } as Response);
}

describe("router", () => {
  beforeEach(async () => {
    setActivePinia(createPinia());
    // Start every test from a known page that skips the fetch
    await router.push({ name: "not-found" });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("defines the main object routes", () => {
    const paths = routes.map((route) => route.path);

    expect(paths).toEqual(
      expect.arrayContaining(["/", "/project", "/task", "/requirement", "/kanban_board", "/request_for_change"]),
    );
    expect(paths[paths.length - 1]).toBe("/:catchAll(.*)*");
  });

  test("the first navigation loads the initial data into the stores", async () => {
    const fetchSpy = mockInitialData();

    await router.push("/project");

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/user/initial_data/");
    expect(usePermissionStore().is_loaded).toBe(true);
    expect(usePermissionStore().maximumPermissions.project).toBe(2);
    expect(useObjectMetaDataStore().all_groups).toEqual(initialData.all_groups);
    expect(useObjectMetaDataStore().tags).toEqual(initialData.tags);
    expect(useUserStore().username).toBe("luke");
    expect(useUserStore().email).toBe("luke@example.com");
    expect(router.currentRoute.value.path).toBe("/project");
  });

  test("the initial data is not fetched again once loaded", async () => {
    const fetchSpy = mockInitialData();

    await router.push("/project");
    await router.push("/project/new");

    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  test("a failed fetch redirects to the server error page", async () => {
    mockInitialData(false, 500);

    await router.push("/project");

    expect(router.currentRoute.value.name).toBe("server-error");
    expect(useErrorStore().message).toBe("Response status: 500");
    expect(usePermissionStore().is_loaded).toBe(false);
  });

  test("error pages do not fetch initial data", async () => {
    const fetchSpy = mockInitialData();

    await router.push({ name: "forbidden" });
    await router.push({ name: "server-error" });

    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("an individual project loads the project page", async () => {
    mockInitialData();

    await router.push("/project/5");

    expect(router.currentRoute.value.name).toBe("Project");
    expect(router.currentRoute.value.params.id).toBe("5");
  });

  test("a destination the user has no permission for goes to forbidden", async () => {
    mockInitialData();

    await router.push("/task");

    expect(router.currentRoute.value.name).toBe("forbidden");
  });

  test("a destination the user can access is allowed", async () => {
    mockInitialData();

    await router.push("/project/new");

    expect(router.currentRoute.value.name).toBe("NewProject");
  });

  test("unknown paths fall back to the not found page", async () => {
    mockInitialData();

    await router.push("/does/not/exist");

    expect(router.currentRoute.value.matched.length).toBeGreaterThan(0);
    expect(router.currentRoute.value.name).toBeUndefined();
  });

  test("changing route resets the documentation and object stores", async () => {
    mockInitialData();
    await router.push("/project");

    useDocumentationStore().currentFolderId = 9;
    useObjectStore().title = "Stale";

    await router.push("/project/new");

    expect(useDocumentationStore().currentFolderId).toBe(0);
    expect(useObjectStore().title).toBe("");
  });
});
