import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { mount, flushPromises, type VueWrapper } from "@vue/test-utils";
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
  routes,
});

// Both panels are always rendered and toggled with v-show, so the wrapper is
// attached to the document to let isVisible() see the display style
function mountLoginPage() {
  return mount(LoginPage, {
    attachTo: document.body,
    global: {
      plugins: [router, i18n],
    },
  });
}

async function signIn(wrapper: VueWrapper, username = "testuser", password = "testpass") {
  const loginPanel = wrapper.find(".login-panel");
  await loginPanel.find("input[type=text]").setValue(username);
  await loginPanel.find("input[type=password]").setValue(password);
  await loginPanel.find("button").trigger("click");

  // Wait for fetch to resolve
  await flushPromises();
  await nextTick();
}

describe("LoginPage", () => {
  let wrapper: VueWrapper;

  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    wrapper?.unmount();
    vi.restoreAllMocks();
  });

  test("renders LoginImage and LoginPanel initially", async () => {
    wrapper = mountLoginPage();

    // Check LoginImage and LoginPanel are shown, TwoFactorPanel is hidden
    expect(wrapper.findComponent(LoginImage).exists()).toBe(true);
    expect(wrapper.findComponent(LoginPanel).isVisible()).toBe(true);
    expect(wrapper.findComponent(TwoFactorPanel).isVisible()).toBe(false);
  });

  test("renders TwoFactorPanel after successful login attempt", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ({ status: "default" }),
    } as Response);

    wrapper = mountLoginPage();
    await signIn(wrapper);

    // Check TwoFactorPanel is shown instead of the LoginPanel
    expect(wrapper.findComponent(LoginImage).exists()).toBe(true);
    expect(wrapper.findComponent(LoginPanel).isVisible()).toBe(false);
    expect(wrapper.findComponent(TwoFactorPanel).isVisible()).toBe(true);
  });

  test("displays validation error message when fields are empty", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    wrapper = mountLoginPage();

    // Trigger sign in without filling fields
    await wrapper.find(".login-panel button").trigger("click");

    // Check error message, and that we never tried to log in
    const errorMessage = wrapper.find(".login-panel .error-message");
    expect(errorMessage.text()).toBe("Please fill out all fields");
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  test("displays error message after failed login attempt", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 401,
    } as Response);

    wrapper = mountLoginPage();
    await signIn(wrapper);

    // Check error message
    const errorMessage = wrapper.find(".login-panel .error-message");
    expect(errorMessage.text()).toBe("Credentials have failed");
  });

  test("displays final error message after more than 5 failed login attempts", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 401,
    } as Response);

    wrapper = mountLoginPage();

    // The fields are cleared after every failure, so fill them in each time
    for (let i = 0; i < 5; i++) {
      await signIn(wrapper);
      expect(wrapper.find(".login-panel .error-message").text()).toBe("Credentials have failed");
    }
    await signIn(wrapper);

    // Check final error message
    const errorMessage = wrapper.find(".login-panel .error-message");
    expect(errorMessage.text()).toBe("Impostor detected, initiating self-destruction");
  });

  test("shows the response status text for an unexpected error", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 500,
      statusText: "Internal Server Error",
    } as Response);

    wrapper = mountLoginPage();
    await signIn(wrapper);

    expect(wrapper.find(".login-panel .error-message").text()).toBe("Internal Server Error");
    expect(wrapper.findComponent(LoginPanel).isVisible()).toBe(true);
  });

  test("a failed two factor attempt returns to the login panel and clears the fields", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: async () => ({ status: "default" }),
    } as Response);

    wrapper = mountLoginPage();
    await signIn(wrapper);
    expect(wrapper.findComponent(TwoFactorPanel).isVisible()).toBe(true);

    fetchSpy.mockResolvedValue({ status: 401 } as Response);
    wrapper.findComponent(TwoFactorPanel).vm.$emit("signIn");
    await flushPromises();
    await nextTick();

    expect(wrapper.findComponent(LoginPanel).isVisible()).toBe(true);
    expect(wrapper.findComponent(TwoFactorPanel).isVisible()).toBe(false);
    expect(wrapper.find(".login-panel .error-message").text()).toBe("Credentials have failed");
    expect((wrapper.find(".login-panel input[type=text]").element as HTMLInputElement).value).toBe("");
  });

  test("sends the credentials to the authentication endpoint", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 401 } as Response);

    wrapper = mountLoginPage();
    await signIn(wrapper, "luke", "secret");

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/authentication/");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
      username: "luke",
      password: "secret",
      otp_token: "",
    });
  });
});

describe("LoginPage - two factor token", () => {
  let wrapper: VueWrapper;

  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    wrapper?.unmount();
    vi.restoreAllMocks();
  });

  test("sends the token typed into the two factor panel", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 401 } as Response);
    wrapper = mountLoginPage();

    wrapper.findComponent(TwoFactorPanel).vm.$emit("update:otpToken", "123456");
    await nextTick();
    await signIn(wrapper, "luke", "secret");

    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
      username: "luke",
      password: "secret",
      otp_token: "123456",
    });
  });

});
