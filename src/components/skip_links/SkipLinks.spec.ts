import { afterEach } from "vitest";
import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {SkipLinks} from ".";
import { createRouter, createMemoryHistory } from "vue-router";
import {defineComponent, h, nextTick} from "vue";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: "/test", component: defineComponent({ render: () => h("div") }) },
  ],
});

describe("SkipLinks", () => {
  beforeEach(async () => {
    await router.push("/test");
    await router.isReady();
  });

  test("skip link exists", async () => {
    const wrapper = mount(SkipLinks, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // There exists only one skip link
    const skipLink = wrapper.find(".skip-link");
    expect(skipLink.exists()).toBe(true);
  });

  test("skip link focuses main content on click", async () => {
    const wrapper = mount(SkipLinks, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Mock main content element
    const mainContent = document.createElement("div");
    mainContent.id = "main";
    document.body.appendChild(mainContent);

    // Click on the skip link
    const skipLink = wrapper.find(".skip-link");
    await skipLink.trigger("click");

    // Check if main content is focused and scrolled into view
    expect(mainContent).toBe(document.activeElement);
    expect(mainContent.getBoundingClientRect().top).toBe(0);

    // Clean up
    document.body.removeChild(mainContent);
  });

  test("skip link makes main content focusable if not already", async () => {
    const wrapper = mount(SkipLinks, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Mock main content element without tabindex
    const mainContent = document.createElement("div");
    mainContent.id = "main";
    document.body.appendChild(mainContent);

    // Click on the skip link
    const skipLink = wrapper.find(".skip-link");
    await skipLink.trigger("click");

    // Check if main content is focusable
    expect(mainContent.hasAttribute("tabindex")).toBe(true);

    // Clean up
    document.body.removeChild(mainContent);
  });

  test("skip link removes tabindex after blur", async () => {
    const wrapper = mount(SkipLinks, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Mock main content element
    const mainContent = document.createElement("div");
    mainContent.id = "main";
    document.body.appendChild(mainContent);

    // Click on the skip link
    const skipLink = wrapper.find(".skip-link");
    await skipLink.trigger("click");

    // Blur the main content
    mainContent.blur();

    // Check if tabindex is removed
    expect(mainContent.hasAttribute("tabindex")).toBe(false);

    // Clean up
    document.body.removeChild(mainContent);
  });
});

describe("SkipLinks - focus handling", () => {
  beforeEach(async () => {
    await router.push("/test");
    await router.isReady();
  });

  afterEach(() => {
    document.getElementById("main")?.remove();
  });

  test("clicking the skip link without a main element does nothing", async () => {
    const wrapper = mount(SkipLinks, { global: { plugins: [router] } });
    await flushPromises();

    await wrapper.find(".skip-link").trigger("click");

    expect(document.getElementById("main")).toBeNull();
  });

  test("changing page moves focus back to the top of the page", async () => {
    router.addRoute({ path: "/other", component: defineComponent({ render: () => h("div") }) });
    const wrapper = mount(SkipLinks, {
      attachTo: document.body,
      global: { plugins: [router] },
    });
    await flushPromises();

    await router.push("/other");
    await flushPromises();

    expect(document.activeElement).toBe(wrapper.find("span").element);
    wrapper.unmount();
  });
});
