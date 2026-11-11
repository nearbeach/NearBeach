import { describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import PublicLinkPage from "./PublicLinkPage.vue";

describe("PublicLinkPage", () => {
  test("mounts without error", () => {
    const wrapper = mount(PublicLinkPage);

    expect(wrapper.exists()).toBe(true);
  });
});
