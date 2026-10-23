import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {PasswordReset} from ".";
import {LoginImage} from "../login_image";
import {PasswordResetPanel} from "./password_reset_panel";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";

describe("PasswordReset", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders LoginImage component", async () => {
    const wrapper = mount(PasswordReset, {
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if LoginImage component is rendered
    const loginImage = wrapper.findComponent(LoginImage);
    expect(loginImage.exists()).toBe(true);
  });

  test("renders PasswordResetPanel component", async () => {
    const wrapper = mount(PasswordReset, {
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if PasswordResetPanel component is rendered
    const passwordResetPanel = wrapper.findComponent(PasswordResetPanel);
    expect(passwordResetPanel.exists()).toBe(true);
  });

  test("layout is flex row", async () => {
    const wrapper = mount(PasswordReset, {
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if the layout is flex row
    const passwordReset = wrapper.find(".password-reset");
    expect(passwordReset.classes()).toContain("password-reset");
    expect(passwordReset.attributes("style")).toContain("display: flex");
    expect(passwordReset.attributes("style")).toContain("flex-direction: row");
    expect(passwordReset.attributes("style")).toContain("height: 100%");
  });
});