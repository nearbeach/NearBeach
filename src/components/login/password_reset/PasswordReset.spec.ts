import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {PasswordReset} from ".";
import {LoginImage} from "../login_image";
import {PasswordResetPanel} from "./password_reset_panel";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import {nextTick} from "vue";

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
    // Attach to the document so the scoped styles are applied
    const wrapper = mount(PasswordReset, {
      attachTo: document.body,
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
    const style = getComputedStyle(passwordReset.element);
    expect(style.display).toBe("flex");
    expect(style.flexDirection).toBe("row");

    wrapper.unmount();
  });
});