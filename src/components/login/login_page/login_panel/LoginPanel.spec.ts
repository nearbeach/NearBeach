import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import LoginPanel from "./LoginPanel.vue";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import i18n from "@/i18n.ts";
import { nextTick } from "vue";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    {
      path: "/login",
      component: defineComponent({ render: () => h("div") }),
    },
  ],
});

describe("LoginPanel", () => {
  beforeEach(async () => {
    setActivePinia(createPinia());
    await router.push("/login");
    await router.isReady();
  });

  test("renders login message", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: "enabled",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const loginMessage = wrapper.find("h1#main-title");
    expect(loginMessage.text()).toBe("NearBeach Login");
  });

  test("renders error message when provided", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: "enabled",
        errorMessage: "Invalid credentials",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const errorMessage = wrapper.find("p.error-message");
    expect(errorMessage.text()).toBe("Invalid credentials");
  });

  test("emits signIn event on form submission", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: "enabled",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const form = wrapper.find("form");
    await form.trigger("submit.prevent");

    expect(wrapper.emitted("signIn")).toBeTruthy();
  });

  test("validates username and password on form submission", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: "enabled",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const usernameInput = wrapper.find("input[type=text]");
    const passwordInput = wrapper.find("input[type=password]");

    await usernameInput.setValue("user");
    await usernameInput.trigger("blur");

    await passwordInput.setValue("pass");
    await passwordInput.trigger("blur");

    const form = wrapper.find("form");
    await form.trigger("submit.prevent");

    expect(wrapper.emitted("signIn")).toBeFalsy();
  });

  test("disables sign in button when buttonState is disabled", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: "disabled",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const signInButton = wrapper.find("button");
    expect(signInButton.attributes("disabled")).toBe("disabled");
  });

  test("enables sign in button when buttonState is enabled", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: "enabled",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const signInButton = wrapper.find("button");
    expect(signInButton.attributes("disabled")).toBeUndefined();
  });
});