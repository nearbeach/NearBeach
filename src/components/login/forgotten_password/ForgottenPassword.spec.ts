import { beforeEach, describe, expect, test, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {ForgottenPassword} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("ForgottenPassword", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders ForgottenPasswordPanel initially", async () => {
    const wrapper = mount(ForgottenPassword, {
      global: {
        plugins: [router, i18n],
      },
    });

    // ForgottenPasswordPanel should be rendered
    const forgottenPasswordPanel = wrapper.findComponent({ name: "ForgottenPasswordPanel" });
    expect(forgottenPasswordPanel.exists()).toBe(true);

    // PasswordResetDone should not be rendered
    const passwordResetDone = wrapper.findComponent({ name: "PasswordResetDone" });
    expect(passwordResetDone.exists()).toBe(false);
  });

  test("submits password reset and renders PasswordResetDone", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200, json: async () => ({}) } as Response);

    const wrapper = mount(ForgottenPassword, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Set email address
    const forgottenPasswordPanel = wrapper.findComponent({ name: "ForgottenPasswordPanel" });
    await forgottenPasswordPanel.vm.$emit("update:email-address", "test@example.com");

    // Trigger password reset
    await forgottenPasswordPanel.vm.$emit("passwordReset");

    // Wait for the fetch call to complete
    await flushPromises();
    await nextTick();

    // ForgottenPasswordPanel should not be rendered
    expect(forgottenPasswordPanel.exists()).toBe(false);

    // PasswordResetDone should be rendered
    const passwordResetDone = wrapper.findComponent({ name: "PasswordResetDone" });
    expect(passwordResetDone.exists()).toBe(true);

    // Error message should be empty
    const errorMessage = wrapper.vm.errorMessage;
    expect(errorMessage).toBe("");

    vi.restoreAllMocks();
  });

  test("submits password reset with error and shows error message", async () => {
    const errorMessage = "An error occurred";
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error(errorMessage));

    const wrapper = mount(ForgottenPassword, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Set email address
    const forgottenPasswordPanel = wrapper.findComponent({ name: "ForgottenPasswordPanel" });
    await forgottenPasswordPanel.vm.$emit("update:email-address", "test@example.com");

    // Trigger password reset
    await forgottenPasswordPanel.vm.$emit("passwordReset");

    // Wait for the fetch call to complete
    await flushPromises();
    await nextTick();

    // ForgottenPasswordPanel should still be rendered
    expect(forgottenPasswordPanel.exists()).toBe(true);

    // PasswordResetDone should not be rendered
    const passwordResetDone = wrapper.findComponent({ name: "PasswordResetDone" });
    expect(passwordResetDone.exists()).toBe(false);

    // Error message should be set
    expect(wrapper.vm.errorMessage).toBe(errorMessage);

    vi.restoreAllMocks();
  });
});