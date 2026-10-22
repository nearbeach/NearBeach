import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import PasswordResetPanel from "./PasswordResetPanel.vue";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { loginRoutes } from "@/router/loginRouter.ts";
import { nextTick } from "vue";
import { vi } from "vitest";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: loginRoutes,
});

describe("PasswordResetPanel", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200, json: async () => ({}) } as Response);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders the reset password title", async () => {
    const wrapper = mount(PasswordResetPanel, {
      global: {
        plugins: [router, i18n],
      },
    });

    const title = wrapper.find("#main-title");
    expect(title.text()).toBe("Reset Password");
  });

  test("displays error message when passwords do not match", async () => {
    const wrapper = mount(PasswordResetPanel, {
      global: {
        plugins: [router, i18n],
      },
    });

    const password1Input = wrapper.findComponent({ ref: "password1" });
    const password2Input = wrapper.findComponent({ ref: "password2" });
    const submitButton = wrapper.findComponent({ ref: "submitButton" });

    await password1Input.setValue("password123");
    await password2Input.setValue("password456");
    await submitButton.trigger("click");

    await flushPromises();
    await nextTick();

    const errorMessage = wrapper.find(".error-message");
    expect(errorMessage.text()).toBe("Passwords don't match");
  });

  test("displays error message when query string is missing", async () => {
    const wrapper = mount(PasswordResetPanel, {
      global: {
        plugins: [router, i18n],
      },
    });

    const password1Input = wrapper.findComponent({ ref: "password1" });
    const password2Input = wrapper.findComponent({ ref: "password2" });
    const submitButton = wrapper.findComponent({ ref: "submitButton" });

    await password1Input.setValue("password123");
    await password2Input.setValue("password123");
    await submitButton.trigger("click");

    await flushPromises();
    await nextTick();

    const errorMessage = wrapper.find(".error-message");
    expect(errorMessage.text()).toBe("Query string missing");
  });

  test("navigates to login page after successful password reset", async () => {
    const wrapper = mount(PasswordResetPanel, {
      global: {
        plugins: [router, i18n],
      },
    });

    const password1Input = wrapper.findComponent({ ref: "password1" });
    const password2Input = wrapper.findComponent({ ref: "password2" });
    const submitButton = wrapper.findComponent({ ref: "submitButton" });

    await password1Input.setValue("password123");
    await password2Input.setValue("password123");
    await submitButton.trigger("click");

    await flushPromises();
    await nextTick();

    expect(router.currentRoute.value.path).toBe("/login");
  });
});