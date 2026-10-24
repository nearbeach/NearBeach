import { beforeEach, describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import {SmallLoadingSkeleton} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("SmallLoadingSkeleton", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("has correct styles", async () => {
    // Attach to the document so the scoped styles are applied
    const wrapper = mount(SmallLoadingSkeleton, {
      attachTo: document.body,
      global: {
        plugins: [router],
      },
    });

    // The styles live in the stylesheet, not the style attribute - check the computed values
    expect(wrapper.classes()).toContain("small-loading-skeleton");
    const style = getComputedStyle(wrapper.element);
    expect(style.textAlign).toBe("center");
    expect(style.fontFamily).toContain("Roboto");
    expect(style.fontWeight).toBe("100");
    expect(style.borderStyle).toBe("dashed");
    expect(style.borderWidth).toBe("1px");

    wrapper.unmount();
  });

  test("renders slot content", async () => {
    const wrapper = mount(SmallLoadingSkeleton, {
      slots: {
        default: "<div class='slot-content'>Slot Content</div>",
      },
      global: {
        plugins: [router],
      },
    });

    // Check if the slot content is rendered
    const slotContent = wrapper.find(".slot-content");
    expect(slotContent.exists()).toBe(true);
    expect(slotContent.text()).toBe("Slot Content");
  });
});