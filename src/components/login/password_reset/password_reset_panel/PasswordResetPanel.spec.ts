import { beforeEach, afterEach, describe, expect, test } from "vitest";
import { mount, flushPromises, type VueWrapper } from "@vue/test-utils";
import {PasswordResetPanel} from ".";
import { createPinia, setActivePinia } from "pinia";
import loginRouter from "@/router/loginRouter.ts";
import { nextTick } from "vue";
import { vi } from "vitest";
import i18n from "@/i18n.ts";

// The component reads uid/token from the real query string
function setQueryString(query: string) {
  window.history.replaceState(null, "", `${window.location.pathname}${query}`);
}

function mountPasswordResetPanel() {
  return mount(PasswordResetPanel, {
    global: {
      plugins: [loginRouter, i18n],
    },
  });
}

async function submitPasswords(wrapper: VueWrapper, password1: string, password2: string) {
  const [password1Input, password2Input] = wrapper.findAll("input[type=password]");
  await password1Input?.setValue(password1);
  await password2Input?.setValue(password2);
  await wrapper.find("button").trigger("click");

  await flushPromises();
  await nextTick();
}

describe("PasswordResetPanel", () => {
  const originalSearch = window.location.search;

  beforeEach(() => {
    setActivePinia(createPinia());
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 200, json: () => Promise.resolve({}) } as Response);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    setQueryString(originalSearch);
  });

  test("renders the reset password title", () => {
    const wrapper = mountPasswordResetPanel();

    const title = wrapper.find("#main-title");
    expect(title.text()).toBe("Reset Password");
  });

  test("displays error message when passwords do not match", async () => {
    const wrapper = mountPasswordResetPanel();

    await submitPasswords(wrapper, "password123", "password456");

    const errorMessage = wrapper.find(".error-message");
    expect(errorMessage.text()).toBe("Passwords don't match");
    expect(globalThis.fetch).not.toHaveBeenCalled();
  });

  test("displays error message when query string is missing", async () => {
    setQueryString("");
    const wrapper = mountPasswordResetPanel();

    await submitPasswords(wrapper, "password123", "password123");

    const errorMessage = wrapper.find(".error-message");
    expect(errorMessage.text()).toBe("Query string missing");
    expect(globalThis.fetch).not.toHaveBeenCalled();
  });

  test("navigates to login page after successful password reset", async () => {
    setQueryString("?uid=abc&token=123");
    // The component pushes on the login router singleton - stub it so the
    // test page is not navigated
    const pushSpy = vi.spyOn(loginRouter, "push").mockResolvedValue(undefined);
    const wrapper = mountPasswordResetPanel();

    await submitPasswords(wrapper, "password123", "password123");

    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/v1/authentication/reset-password/",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ password: "password123", uid: "abc", token: "123" }),
      }),
    );
    expect(pushSpy).toHaveBeenCalledWith("/login");
  });
});

describe("PasswordResetPanel - backend errors", () => {
  const originalSearch = window.location.search;

  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    vi.restoreAllMocks();
    setQueryString(originalSearch);
  });

  test("shows the status text when the reset is rejected", async () => {
    setQueryString("?uid=abc&token=123");
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 400,
      statusText: "Bad Request",
    } as Response);
    const pushSpy = vi.spyOn(loginRouter, "push").mockResolvedValue(undefined);
    const wrapper = mountPasswordResetPanel();

    await submitPasswords(wrapper, "password123", "password123");

    expect(wrapper.find(".error-message").text()).toBe("Bad Request");
    expect(pushSpy).not.toHaveBeenCalled();
  });
});
