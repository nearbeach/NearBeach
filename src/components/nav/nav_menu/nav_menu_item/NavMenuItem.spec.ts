import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createMemoryHistory } from "vue-router";
import {NavMenuItem} from ".";
import { useNavStore } from "@/stores/nav/nav.ts";
import { defineComponent, h } from "vue";

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    {
      path: "/test-route",
      component: defineComponent({ render: () => h("div") }),
    },
  ],
});

describe("NavMenuItem", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1440,
    });
  });

  test("renders with correct class when active", async () => {
    await router.push("/test-route");
    await router.isReady();

    const wrapper = mount(NavMenuItem, {
      props: {
        destination: "test",
        overrideAriaLabel: "Test Item",
        routeAddress: "/test-route",
        title: "Test Item",
      },
      global: {
        plugins: [router],
      },
    });

    await flushPromises();
    await nextTick();

    expect(wrapper.classes()).toContain("current");
  });

  test("renders with correct class when not active", async () => {
    await router.push("/another-route");
    await router.isReady();

    const wrapper = mount(NavMenuItem, {
      props: {
        destination: "test",
        overrideAriaLabel: "Test Item",
        routeAddress: "/test-route",
        title: "Test Item",
      },
      global: {
        plugins: [router],
      },
    });

    await flushPromises();
    await nextTick();

    expect(wrapper.classes()).not.toContain("current");
  });

  test("emits closeMenu event on click", async () => {
    const navStore = useNavStore();
    const wrapper = mount(NavMenuItem, {
      props: {
        destination: "test",
        overrideAriaLabel: "Test Item",
        routeAddress: "/test-route",
        title: "Test Item",
      },
      global: {
        plugins: [router],
      },
    });

    await flushPromises();
    await nextTick();

    const link = wrapper.find(".nav-bar--menu--item-search");
    await link.trigger("click");

    expect(navStore.isNavOpen).toBe(false);
  });

  test("renders new route link when routeAddressNew is provided", async () => {
    const wrapper = mount(NavMenuItem, {
      props: {
        destination: "test",
        overrideAriaLabel: "Test Item",
        routeAddress: "/test-route",
        routeAddressNew: "/new-test-route",
        title: "Test Item",
      },
      global: {
        plugins: [router],
      },
    });

    await flushPromises();
    await nextTick();

    const newLink = wrapper.find(".nav-bar--menu--item-new");
    expect(newLink.exists()).toBe(true);
    expect(newLink.attributes("to")).toBe("/new-test-route");
  });

  test("does not render new route link when routeAddressNew is not provided", async () => {
    const wrapper = mount(NavMenuItem, {
      props: {
        destination: "test",
        overrideAriaLabel: "Test Item",
        routeAddress: "/test-route",
        title: "Test Item",
      },
      global: {
        plugins: [router],
      },
    });

    await flushPromises();
    await nextTick();

    const newLink = wrapper.find(".nav-bar--menu--item-new");
    expect(newLink.exists()).toBe(false);
  });
});