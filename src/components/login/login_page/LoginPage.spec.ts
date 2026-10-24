import { beforeEach, describe, expect, test, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {LoginPage} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import i18n from "@/i18n.ts";
import {LoginPanel} from "@/components/login/login_page/login_panel";
import {LoginImage} from "@/components/login/login_image";
import {TwoFactorPanel} from "@/components/login/login_page/two_factor_panel";
import {nextTick} from "vue";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("LoginPage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders LoginImage and LoginPanel initially", async () => {
    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Check LoginImage and LoginPanel are rendered
    expect(wrapper.findComponent(LoginImage).exists()).toBe(true);
    expect(wrapper.findComponent(LoginPanel).exists()).toBe(true);
    expect(wrapper.findComponent(TwoFactorPanel).exists()).toBe(false);
  });

  test("renders TwoFactorPanel after successful login attempt", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ({ status: "default" }),
    } as Response);

    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Fill in credentials
    await wrapper.find("[data-testid='username']").setValue("testuser");
    await wrapper.find("[data-testid='password']").setValue("testpass");

    // Trigger sign in
    await wrapper.find("[data-testid='sign-in-button']").trigger("click");

    // Wait for fetch to resolve
    await flushPromises();
    await nextTick();

    // Check TwoFactorPanel is rendered
    expect(wrapper.findComponent(LoginImage).exists()).toBe(true);
    expect(wrapper.findComponent(LoginPanel).exists()).toBe(false);
    expect(wrapper.findComponent(TwoFactorPanel).exists()).toBe(true);

    vi.restoreAllMocks();
  });

  test("displays validation error message when fields are empty", async () => {
    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Trigger sign in without filling fields
    await wrapper.find("[data-testid='sign-in-button']").trigger("click");

    // Check error message
    const errorMessage = wrapper.find("[data-testid='error-message']");
    expect(errorMessage.text()).toBe("Please fill out all fields");
  });

  test("displays error message after failed login attempt", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue({
      status: 401,
    } as Response);

    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Fill in credentials
    await wrapper.find("[data-testid='username']").setValue("testuser");
    await wrapper.find("[data-testid='password']").setValue("testpass");

    // Trigger sign in
    await wrapper.find("[data-testid='sign-in-button']").trigger("click");

    // Wait for fetch to resolve
    await flushPromises();
    await nextTick();

    // Check error message
    const errorMessage = wrapper.find("[data-testid='error-message']");
    expect(errorMessage.text()).toBe("Credentials have failed");

    vi.restoreAllMocks();
  });

  test("displays final error message after 5 failed login attempts", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue({
      status: 401,
    } as Response);

    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Fill in credentials
    await wrapper.find("[data-testid='username']").setValue("testuser");
    await wrapper.find("[data-testid='password']").setValue("testpass");

    // Trigger sign in 5 times
    for (let i = 0; i < 5; i++) {
      await wrapper.find("[data-testid='sign-in-button']").trigger("click");
      await flushPromises();
      await nextTick();
    }

    // Check final error message
    const errorMessage = wrapper.find("[data-testid='error-message']");
    expect(errorMessage.text()).toBe("Impostor detected, initiating self-destruction");

    vi.restoreAllMocks();
  });
});