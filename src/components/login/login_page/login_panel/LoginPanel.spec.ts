import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {LoginPanel} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import i18n from "@/i18n.ts";
import {ObjectStateEnum} from "whelk-ui";
import {defineComponent, h, nextTick} from "vue";

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
        buttonState: ObjectStateEnum.NoAction,
        username: "",
        password: "",
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
        buttonState: ObjectStateEnum.NoAction,
        username: "",
        password: "",
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
        buttonState: ObjectStateEnum.NoAction,
        username: "",
        password: "",
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

  test("shows validation errors when the password is too short", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        username: "",
        password: "",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    await wrapper.find("input[type=text]").setValue("user");
    await wrapper.find("input[type=password]").setValue("pass");

    await wrapper.find("button").trigger("click");

    // Password must be at least 8 characters - the field reports the error,
    // and validation of the credentials themselves is left to the parent
    const passwordError = wrapper.find(".wlk-password-input .render-error-message");
    expect(passwordError.text()).not.toBe("");
    expect(wrapper.emitted("signIn")).toHaveLength(1);
  });

  test("disables sign in button when buttonState is disabled", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: ObjectStateEnum.Disable,
        username: "",
        password: "",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const signInButton = wrapper.find("button");
    expect((signInButton.element as HTMLButtonElement).disabled).toBe(true);
  });

  test("enables sign in button when buttonState is enabled", async () => {
    const wrapper = mount(LoginPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        username: "",
        password: "",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const signInButton = wrapper.find("button");
    expect((signInButton.element as HTMLButtonElement).disabled).toBe(false);
  });
});