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
    const wrapper = mount(SmallLoadingSkeleton, {
      global: {
        plugins: [router],
      },
    });

    // Check if the component has the correct styles
    expect(wrapper.classes()).toContain("small-loading-skeleton");
    expect(wrapper.attributes("style")).toContain("text-align: center");
    expect(wrapper.attributes("style")).toContain("font-family: \"Roboto\", sans-serif");
    expect(wrapper.attributes("style")).toContain("font-weight: 100");
    expect(wrapper.attributes("style")).toContain("padding: 2rem 0");
    expect(wrapper.attributes("style")).toContain("border: 1px black dashed");
    expect(wrapper.attributes("style")).toContain("margin: 0 2rem 3rem 2rem");
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