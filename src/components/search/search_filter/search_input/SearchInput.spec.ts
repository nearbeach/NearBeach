import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {SearchInput} from ".";
import { defineComponent, h } from "vue";

describe("SearchInput", () => {
  test("renders with custom placeholder", async () => {
    const placeholder = "Search for something";
    const wrapper = mount(SearchInput, {
      props: {
        placeholder,
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check the input has the correct placeholder
    const input = wrapper.find("input");
    expect(input.attributes("placeholder")).toBe(placeholder);
  });

  test("emits update:modelValue on input change", async () => {
    const wrapper = mount(SearchInput, {
      props: {
        modelValue: "",
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Change the input value
    const input = wrapper.find("input");
    await input.setValue("test");

    // Check the update:modelValue event is emitted
    expect(wrapper.emitted()["update:modelValue"]).toBeTruthy();
    expect(wrapper.emitted()["update:modelValue"][0]).toEqual(["test"]);
  });

  test("renders the search icon", async () => {
    const wrapper = mount(SearchInput, {
      props: {
        modelValue: "",
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check the search icon exists
    const searchIcon = wrapper.findComponent({ name: "Search" });
    expect(searchIcon.exists()).toBe(true);
  });
});