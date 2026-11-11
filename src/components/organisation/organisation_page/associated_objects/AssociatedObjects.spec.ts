import { describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import AssociatedObjects from "./AssociatedObjects.vue";

describe("AssociatedObjects", () => {
  test("renders its container", () => {
    const wrapper = mount(AssociatedObjects);

    expect(wrapper.find(".associated-objects").exists()).toBe(true);
  });
});
