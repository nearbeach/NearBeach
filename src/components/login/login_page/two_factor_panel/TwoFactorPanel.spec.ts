import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {TwoFactorPanel} from ".";
import { createPinia, setActivePinia } from "pinia";
import i18n from "@/i18n.ts";
import { nextTick } from "vue";
import { ObjectStateEnum } from "@/utils/enums/ObjectStateEnum";

describe("TwoFactorPanel", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders correct translation for login_message", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        otpToken: "",
      },
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check login message text
    const loginMessage = wrapper.find("h1");
    expect(loginMessage.text()).toBe("NearBeach Login");
  });

  test("renders correct translation for submit_tfa", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        otpToken: "",
      },
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check submit tfa button text
    const submitButton = wrapper.find("button");
    expect(submitButton.text()).toBe("Submit 2FA");
  });

  test("renders correct translation for tfa", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        otpToken: "",
      },
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check tfa label text
    const tfaLabel = wrapper.find("label");
    expect(tfaLabel.text()).toContain("Two Factor Password");
  });

  test("renders correct translation for tfa_placeholder", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        otpToken: "",
      },
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check tfa placeholder text
    const tfaInput = wrapper.find("input");
    expect(tfaInput.attributes("placeholder")).toBe("Please insert the two factor password");
  });

  test("emits signIn event when button is clicked", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        otpToken: "",
      },
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Click the submit button
    const submitButton = wrapper.find("button");
    await submitButton.trigger("click");

    // Check if signIn event is emitted
    expect(wrapper.emitted("signIn")).toBeTruthy();
  });

  test("displays error message when provided", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        errorMessage: "Invalid 2FA code",
        otpToken: "",
      },
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check error message text
    const errorMessage = wrapper.find(".error-message");
    expect(errorMessage.text()).toBe("Invalid 2FA code");
  });

  test("validates input and displays error if input is invalid", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: {
        buttonState: ObjectStateEnum.NoAction,
        otpToken: "",
      },
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Enter invalid input (empty for required validation)
    const tfaInput = wrapper.find("input");
    await tfaInput.setValue("");
    await tfaInput.trigger("blur");

    // Check if error message is displayed
    const errorMessage = wrapper.find(".render-error-message");
    expect(errorMessage.text()).toBe("This field is required");
  });

  test("button is disabled when buttonState is disabled", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: {
        buttonState: ObjectStateEnum.Disable,
        otpToken: "",
      },
      global: {
        plugins: [i18n],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check if button is disabled
    const submitButton = wrapper.find("button");
    expect(submitButton.attributes("disabled")).toBeDefined();
  });
});

describe("TwoFactorPanel - token model", () => {
  test("typing a token updates the otpToken model", async () => {
    const wrapper = mount(TwoFactorPanel, {
      props: { buttonState: ObjectStateEnum.NoAction, otpToken: "" },
      global: { plugins: [i18n] },
    });

    await wrapper.find("input").setValue("654321");

    expect(wrapper.emitted("update:otpToken")?.at(-1)).toEqual(["654321"]);
  });
});
