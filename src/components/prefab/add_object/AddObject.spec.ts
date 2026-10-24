import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { mount } from "@vue/test-utils";
import {AddObject} from ".";
import { createPinia, setActivePinia } from "pinia";

const DEFAULT_PROPS = {
  label: "Test Label",
  options: [{ label: "Option 1", value: "1" }],
  modelValue: null,
};

function mountAddObject(
  props: Partial<typeof DEFAULT_PROPS> = {},
  options = {}
) {
  return mount(AddObject, {
    props: {
      ...DEFAULT_PROPS,
      ...props,
    },
    ...options,
  });
}

describe("AddObject", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // Never let the real showPicker() run - in a real browser it opens a native
  // popup, which can close the test page and crash the whole run.
  function mockShowPicker(isActive: boolean) {
    vi.spyOn(Navigator.prototype, "userActivation", "get").mockReturnValue({
      isActive,
    } as UserActivation);
    return vi
      .spyOn(HTMLSelectElement.prototype, "showPicker")
      .mockImplementation(() => {});
  }

  test("renders label correctly", async () => {
    const wrapper = mountAddObject();

    const label = wrapper.find("label");
    expect(label.text()).toBe("+Test Label");
  });

  test("renders options correctly", async () => {
    const wrapper = mountAddObject({
      options: [
        { label: "Option 1", value: "1" },
        { label: "Option 2", value: "2" },
      ],
    });

    const options = wrapper.findAll("option");
    expect(options.length).toBe(2);
    expect(options.at(0)?.text()).toBe("Option 1");
    expect(options.at(1)?.text()).toBe("Option 2");
  });

  test("select is disabled when options are empty", async () => {
    const wrapper = mountAddObject({
      options: [],
    });

    const select = wrapper.find("select");
    expect((select.element as HTMLSelectElement).disabled).toBe(true);
  });

  test("select is not disabled when options are present", async () => {
    const wrapper = mountAddObject();

    const select = wrapper.find("select");
    expect(select.attributes("disabled")).toBeUndefined();
  });

  test("emits update:modelValue on change", async () => {
    const wrapper = mountAddObject({
      options: [
        { label: "Option 1", value: "1" },
        { label: "Option 2", value: "2" },
      ],
    });

    const select = wrapper.find("select");
    await select.setValue("2");

    expect(wrapper.emitted()["update:modelValue"]).toBeTruthy();
    expect(wrapper.emitted()["update:modelValue"][0]).toEqual(["2"]);
  });

  test("calls showPicker on focus if user activation is active", async () => {
    const wrapper = mountAddObject();

    const showPicker = mockShowPicker(true);
    const select = wrapper.find("select");

    await select.trigger("focus");

    // Check if showPicker was called
    expect(showPicker).toHaveBeenCalled();
  });

  test("does not call showPicker on focus if user activation is not active", async () => {
    const wrapper = mountAddObject();

    const showPicker = mockShowPicker(false);
    const select = wrapper.find("select");

    await select.trigger("focus");

    // Check if showPicker was not called
    expect(showPicker).not.toHaveBeenCalled();
  });
});