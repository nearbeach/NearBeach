import { beforeEach, describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import ObjectStatusTag from "./ObjectStatusTag.vue";

describe("ObjectStatusTag", () => {
  test("renders with correct class and text for valid higherOrderStatus", async () => {
    const wrapper = mount(ObjectStatusTag, {
      props: {
        higherOrderStatus: "normal",
        status: "Active",
      },
    });

    const span = wrapper.find("span");
    expect(span.classes()).toContain("object-status-tag");
    expect(span.classes()).toContain("normal");
    expect(span.text()).toBe("Active");
  });

  test("throws error for invalid higherOrderStatus", async () => {
    expect(() => {
      mount(ObjectStatusTag, {
        props: {
          higherOrderStatus: "invalid",
          status: "Active",
        },
      });
    }).toThrowErrorMatchingInlineSnapshot(
      `"Invalid prop: custom validator check failed for prop "higherOrderStatus"."`
    );
  });

  test("renders with correct class and text for different higherOrderStatus", async () => {
    const wrapper = mount(ObjectStatusTag, {
      props: {
        higherOrderStatus: "blocked",
        status: "Blocked",
      },
    });

    const span = wrapper.find("span");
    expect(span.classes()).toContain("object-status-tag");
    expect(span.classes()).toContain("blocked");
    expect(span.text()).toBe("Blocked");
  });

  test("renders with correct class and text for different higherOrderStatus", async () => {
    const wrapper = mount(ObjectStatusTag, {
      props: {
        higherOrderStatus: "closed",
        status: "Closed",
      },
    });

    const span = wrapper.find("span");
    expect(span.classes()).toContain("object-status-tag");
    expect(span.classes()).toContain("closed");
    expect(span.text()).toBe("Closed");
  });

  test("renders with correct class and text for different higherOrderStatus", async () => {
    const wrapper = mount(ObjectStatusTag, {
      props: {
        higherOrderStatus: "backlog",
        status: "Backlog",
      },
    });

    const span = wrapper.find("span");
    expect(span.classes()).toContain("object-status-tag");
    expect(span.classes()).toContain("backlog");
    expect(span.text()).toBe("Backlog");
  });
});