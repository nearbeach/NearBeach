// FormGroup.spec.ts
import { describe, test, expect } from "vitest";
import FormGroup from "./FormGroup.vue";
import { mount } from "@vue/test-utils";

describe("FormGroup", async () => {
  test("form group slot renders main content", () => {
    const wrapper = mount(FormGroup, {
      slots: {
        default: "Main Content",
      },
    });
    expect(wrapper.html()).toContain("Main Content");
    expect(wrapper.find(".form-group").text()).toContain("Main Content");
  });
});
