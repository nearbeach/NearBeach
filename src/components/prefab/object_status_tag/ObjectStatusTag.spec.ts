import { describe, expect, test, vi } from "vitest";
import { mount } from "@vue/test-utils";
import {ObjectStatusTag} from ".";

describe("ObjectStatusTag", () => {
  test("renders with correct class and text for valid higherOrderStatus", () => {
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

  test("warns for invalid higherOrderStatus", () => {
    // Vue prop validators only warn, they never throw
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => { /* Intentionally left empty */ });

    mount(ObjectStatusTag, {
      props: {
        higherOrderStatus: "invalid",
        status: "Active",
      },
    });

    const warnings = warnSpy.mock.calls.map((call) => String(call[0]));
    expect(warnings).toContainEqual(
      expect.stringContaining('Invalid prop: custom validator check failed for prop "higherOrderStatus"'),
    );
    warnSpy.mockRestore();
  });

  test("renders with correct class and text for different higherOrderStatus", () => {
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

  test("renders with correct class and text for different higherOrderStatus", () => {
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

  test("renders with correct class and text for different higherOrderStatus", () => {
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