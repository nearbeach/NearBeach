import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {ForgottenPasswordPanel} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import i18n from "@/i18n.ts";
import {defineComponent, h, nextTick} from "vue";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    {
      path: "/login",
      component: defineComponent({ render: () => h("div") }),
    },
    {
      path: "/forgotten-password",
      component: ForgottenPasswordPanel,
    },
  ],
});

describe("ForgottenPasswordPanel", () => {
  beforeEach(async () => {
    setActivePinia(createPinia());
    await router.push("/forgotten-password");
    await router.isReady();
  });

  test("disables submit button when email is invalid", async () => {
    const wrapper = mount(ForgottenPasswordPanel, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Set an invalid email
    const emailInput = wrapper.find("input[type=text]");
    await emailInput.setValue("invalid-email");
    await emailInput.trigger("blur");

    // Wait for the input to report its validity
    await nextTick();

    const submitButton = wrapper.find("button");
    expect((submitButton.element as HTMLButtonElement).disabled).toBe(true);
  });

  test("enables submit button when email is valid", async () => {
    const wrapper = mount(ForgottenPasswordPanel, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Set a valid email
    const emailInput = wrapper.find("input[type=text]");
    await emailInput.setValue("valid-email@example.com");
    await emailInput.trigger("blur");

    // Wait for the input to report its validity
    await nextTick();

    const submitButton = wrapper.find("button");
    expect((submitButton.element as HTMLButtonElement).disabled).toBe(false);
  });

  test("emits passwordReset event on form submit", async () => {
    const wrapper = mount(ForgottenPasswordPanel, {
      global: {
        plugins: [router, i18n],
      },
    });

    // Set a valid email
    const emailInput = wrapper.find("input[type=text]");
    await emailInput.setValue("valid-email@example.com");
    await emailInput.trigger("blur");

    // Wait for the input to report its validity
    await nextTick();

    const form = wrapper.find("form");
    await form.trigger("submit.prevent");

    expect(wrapper.emitted()).toHaveProperty("passwordReset");
  });

  test("renders correct translations", async () => {
    const wrapper = mount(ForgottenPasswordPanel, {
      global: {
        plugins: [router, i18n],
      },
    });

    expect(wrapper.text()).toContain("Forgotten password");
    expect(wrapper.text()).toContain("Email");
    expect(wrapper.text()).toContain("Submit");
    expect(wrapper.text()).toContain("Go back to login");
  });
});