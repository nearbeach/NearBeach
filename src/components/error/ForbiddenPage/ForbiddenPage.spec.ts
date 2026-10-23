import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {ForbiddenPage} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import { WlkCard, WlkCardHeader } from "whelk-ui";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("ForbiddenPage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders Forbidden title", async () => {
    const wrapper = mount(ForbiddenPage, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check the title is rendered correctly
    const title = wrapper.find("#main-title");
    expect(title.text()).toBe("Forbidden");
  });

  test("renders permission message", async () => {
    const wrapper = mount(ForbiddenPage, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check the permission message is rendered correctly
    const message = wrapper.find("p");
    expect(message.text()).toBe("Sorry, you do not have permission to view that object");
  });

  test("uses WlkCard component", async () => {
    const wrapper = mount(ForbiddenPage, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check WlkCard component is used
    const card = wrapper.findComponent(WlkCard);
    expect(card.exists()).toBe(true);
  });

  test("uses WlkCardHeader component", async () => {
    const wrapper = mount(ForbiddenPage, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check WlkCardHeader component is used
    const cardHeader = wrapper.findComponent(WlkCardHeader);
    expect(cardHeader.exists()).toBe(true);
  });
});