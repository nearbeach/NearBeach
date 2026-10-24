import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {PasswordResetDone} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import i18n from "@/i18n.ts";
import {defineComponent, h, nextTick} from "vue";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    {
      path: "/password-reset-done",
      component: defineComponent({ render: () => h("div") }),
    },
  ],
});

describe("PasswordResetDone", () => {
  beforeEach(async () => {
    setActivePinia(createPinia());
    await router.push("/password-reset-done");
    await router.isReady();
  });

  test("renders success message when no error", async () => {
    const wrapper = mount(PasswordResetDone, {
      props: {
        errorMessage: "",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const title = wrapper.find("#main-title");
    expect(title.text()).toBe("Password Reset Sent");

    const message = wrapper.find("p");
    expect(message.text()).toBe("Please check your inbox for the password reset, and any further instructions");

    const link = wrapper.find("a");
    expect(link.text()).toBe("Click here to return to login page.");
    expect(link.attributes("href")).toBe("/login");
  });

  test("renders error message when error", async () => {
    const wrapper = mount(PasswordResetDone, {
      props: {
        errorMessage: "An error occurred",
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const title = wrapper.find("#main-title");
    expect(title.text()).toBe("Password Reset Failed");

    const errorMessage = wrapper.find("p");
    expect(errorMessage.text()).toBe("An error occurred");

    const link = wrapper.find("a");
    expect(link.text()).toBe("Click here to return to login page.");
    expect(link.attributes("href")).toBe("/login");
  });
});