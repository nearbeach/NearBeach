import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import AddObject from "./AddObject.vue";
import { createPinia, setActivePinia } from "pinia";
import { nextTick } from "vue";

describe("AddObject", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders label correctly", async () => {
    const wrapper = mount(AddObject, {
      props: {
        label: "Test Label",
        options: [{ label: "Option 1", value: "1" }],
      },
    });

    const label = wrapper.find("label");
    expect(label.text()).toBe("+Test Label");
  });

  test("renders options correctly", async () => {
    const wrapper = mount(AddObject, {
      props: {
        label: "Test Label",
        options: [
          { label: "Option 1", value: "1" },
          { label: "Option 2", value: "2" },
        ],
      },
    });

    const options = wrapper.findAll("option");
    expect(options.length).toBe(2);
    expect(options.at(0)?.text()).toBe("Option 1");
    expect(options.at(1)?.text()).toBe("Option 2");
  });

  test("select is disabled when options are empty", async () => {
    const wrapper = mount(AddObject, {
      props: {
        label: "Test Label",
        options: [],
      },
    });

    const select = wrapper.find("select");
    expect(select.attributes("disabled")).toBe("disabled");
  });

  test("select is not disabled when options are present", async () => {
    const wrapper = mount(AddObject, {
      props: {
        label: "Test Label",
        options: [{ label: "Option 1", value: "1" }],
      },
    });

    const select = wrapper.find("select");
    expect(select.attributes("disabled")).toBeUndefined();
  });

  test("emits update:modelValue on change", async () => {
    const wrapper = mount(AddObject, {
      props: {
        label: "Test Label",
        options: [
          { label: "Option 1", value: "1" },
          { label: "Option 2", value: "2" },
        ],
      },
    });

    const select = wrapper.find("select");
    await select.setValue("2");

    expect(wrapper.emitted()["update:modelValue"]).toBeTruthy();
    expect(wrapper.emitted()["update:modelValue"][0]).toEqual(["2"]);
  });

  test("calls showPicker on focus if user activation is active", async () => {
    const wrapper = mount(AddObject, {
      props: {
        label: "Test Label",
        options: [{ label: "Option 1", value: "1" }],
      },
    });

    const select = wrapper.find("select");
    const focusEvent = new FocusEvent("focus");
    Object.defineProperty(focusEvent, "target", {
      writable: false,
      value: select.element,
    });

    // Mock user activation
    Object.defineProperty(navigator, "userActivation", {
      writable: true,
      value: { isActive: true },
    });

    await select.trigger("focus");

    // Check if showPicker was called
    expect(select.element.showPicker).toHaveBeenCalled();
  });

  test("does not call showPicker on focus if user activation is not active", async () => {
    const wrapper = mount(AddObject, {
      props: {
        label: "Test Label",
        options: [{ label: "Option 1", value: "1" }],
      },
    });

    const select = wrapper.find("select");
    const focusEvent = new FocusEvent("focus");
    Object.defineProperty(focusEvent, "target", {
      writable: false,
      value: select.element,
    });

    // Mock user activation
    Object.defineProperty(navigator, "userActivation", {
      writable: true,
      value: { isActive: false },
    });

    await select.trigger("focus");

    // Check if showPicker was not called
    expect(select.element.showPicker).not.toHaveBeenCalled();
  });
});