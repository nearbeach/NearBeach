import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { createMemoryHistory, createRouter } from "vue-router";
import { defineComponent, h } from "vue";
import {NewObject} from ".";
import i18n from "@/i18n.ts";
import { useErrorStore } from "@/stores/error/error.ts";
import { usePermissionStore } from "@/stores/permissions/permission.ts";

// NewObject calls router.push() on the app's own router singleton (not the router
// installed as a plugin). That router has a beforeEach guard which makes network
// requests, so we replace it with a spy and assert on the calls instead.
const { pushMock } = vi.hoisted(() => ({ pushMock: vi.fn() }));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));

// useRoute() reads route.meta.destination, so the component must be mounted on a real route.
async function mountForDestination(destination: string) {
  const router = createRouter({
    history: createMemoryHistory(),
    routes: [
      {
        path: `/${destination}/new`,
        component: defineComponent({ render: () => h("div") }),
        meta: { destination },
      },
    ],
  });
  await router.push(`/${destination}/new`);
  await router.isReady();

  return mount(NewObject, {
    global: { plugins: [router, i18n] },
  });
}

// Fills the form the way a user would. The whelk-ui text input only reports its
// validity on blur (the user leaving the field), so setValue alone is not enough.
async function fillForm(wrapper: Awaited<ReturnType<typeof mountForDestination>>, title: string) {
  const titleInput = wrapper.find("input[type=text]");
  await titleInput.setValue(title);
  await titleInput.trigger("blur");
  await wrapper.find("select").setValue("1");
  await flushPromises();
}

describe("NewObject", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    pushMock.mockClear();

    // The permission store has no setter for groups - seed its state directly.
    const permissionStore = usePermissionStore();
    permissionStore.userGroups = [{ value: "1", label: "Group1", optGroup: "" }];
  });

  afterEach(() => {
    vi.restoreAllMocks();
    document.cookie = "csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  });

  describe("title", () => {
    test.each([
      ["project", "Create your new Project"],
      ["task", "Create your new Task"],
      ["requirement", "Create you new Requirement"],
    ])("shows the right heading for the %s route", async (destination, expectedTitle) => {
      const wrapper = await mountForDestination(destination);

      expect(wrapper.find("#main-title").text()).toBe(expectedTitle);
    });
  });

  describe("create button", () => {
    test("is disabled while the form is empty", async () => {
      const wrapper = await mountForDestination("project");

      expect(wrapper.find<HTMLButtonElement>(".primary").element.disabled).toBe(true);
    });

    test("is enabled once a valid title and a group are provided", async () => {
      const wrapper = await mountForDestination("project");

      await fillForm(wrapper, "My new project");

      expect(wrapper.find<HTMLButtonElement>(".primary").element.disabled).toBe(false);
    });

    test("stays disabled when the title is shorter than 5 characters", async () => {
      const wrapper = await mountForDestination("project");

      await fillForm(wrapper, "abc");

      expect(wrapper.find<HTMLButtonElement>(".primary").element.disabled).toBe(true);
    });
  });

  describe("submitting", () => {
    test("does not call the API when the form is empty", async () => {
      const fetchSpy = vi.spyOn(globalThis, "fetch");
      const wrapper = await mountForDestination("project");

      await wrapper.find(".primary").trigger("click");
      await flushPromises();

      expect(fetchSpy).not.toHaveBeenCalled();
      expect(pushMock).not.toHaveBeenCalled();
    });

    test("posts the title and selected group to the API for the current destination", async () => {
      const fetchSpy = vi
        .spyOn(globalThis, "fetch")
        .mockResolvedValue({ status: 201, json: async () => ({ id: "123" }) } as Response);
      const wrapper = await mountForDestination("project");

      await fillForm(wrapper, "My new project");
      await wrapper.find(".primary").trigger("click");
      await flushPromises();

      expect(fetchSpy).toHaveBeenCalledTimes(1);
      expect(fetchSpy).toHaveBeenCalledWith("/api/v1/project/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFTOKEN": "",
        },
        body: JSON.stringify({ title: "My new project", group_list: ["1"] }),
      });
    });

    test("sends the CSRF token from the cookie", async () => {
      document.cookie = "csrftoken=abc123";
      const fetchSpy = vi
        .spyOn(globalThis, "fetch")
        .mockResolvedValue({ status: 201, json: async () => ({ id: "123" }) } as Response);
      const wrapper = await mountForDestination("project");

      await fillForm(wrapper, "My new project");
      await wrapper.find(".primary").trigger("click");
      await flushPromises();

      const requestInit = fetchSpy.mock.calls[0]![1] as RequestInit;
      expect((requestInit.headers as Record<string, string>)["X-CSRFTOKEN"]).toBe("abc123");
    });

    test("redirects to the new object after a 201 response", async () => {
      vi.spyOn(globalThis, "fetch").mockResolvedValue({
        status: 201,
        json: async () => ({ id: "123" }),
      } as Response);
      const wrapper = await mountForDestination("project");

      await fillForm(wrapper, "My new project");
      await wrapper.find(".primary").trigger("click");
      await flushPromises();

      expect(pushMock).toHaveBeenCalledWith("/project/123");
    });

    test("records an error and redirects to the server error page on failure", async () => {
      vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 500 } as Response);
      const errorStore = useErrorStore();
      const wrapper = await mountForDestination("project");

      await fillForm(wrapper, "My new project");
      await wrapper.find(".primary").trigger("click");
      await flushPromises();

      expect(errorStore.message).not.toBe("");
      expect(pushMock).toHaveBeenCalledWith({ name: "server-error" });
      expect(pushMock).not.toHaveBeenCalledWith(expect.stringContaining("/project/"));
    });
  });
});

describe("NewObject - validation guard", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    pushMock.mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("createObject does nothing while the form is invalid", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    const wrapper = await mountForDestination("project");

    // The button is disabled, so call the handler directly
    await (wrapper.vm as unknown as { createObject: () => Promise<void> }).createObject();

    expect(fetchSpy).not.toHaveBeenCalled();
    expect(pushMock).not.toHaveBeenCalled();
  });
});
