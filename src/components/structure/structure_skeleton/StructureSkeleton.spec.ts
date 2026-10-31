import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {StructureSkeleton} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

describe("StructureSkeleton", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("header exists", async () => {
    const wrapper = mount(StructureSkeleton, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // There exists only one header
    const header = wrapper.find("header");
    expect(header.exists()).toBe(true);
  });

  test("skeleton card exists", async () => {
    const wrapper = mount(StructureSkeleton, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // There exists only one skeleton card
    const skeletonCard = wrapper.find(".skeleton-card");
    expect(skeletonCard.exists()).toBe(true);
  });

  test("skeleton header exists", async () => {
    const wrapper = mount(StructureSkeleton, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // There exists only one skeleton header
    const skeletonHeader = wrapper.find(".skeleton-header");
    expect(skeletonHeader.exists()).toBe(true);
  });

  test("skeleton lines exist", async () => {
    const wrapper = mount(StructureSkeleton, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // There are four skeleton lines
    const skeletonLines = wrapper.findAll(".skeleton-line");
    expect(skeletonLines.length).toBe(4);
  });

  test("skeleton lines have correct classes", async () => {
    const wrapper = mount(StructureSkeleton, {
      global: {
        plugins: [router],
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // The first skeleton line has extra-margin class
    const firstSkeletonLine = wrapper.find(".skeleton-line.extra-margin");
    expect(firstSkeletonLine.exists()).toBe(true);

    // The other skeleton lines do not have extra-margin class
    const otherSkeletonLines = wrapper.findAll(".skeleton-line:not(.extra-margin)");
    expect(otherSkeletonLines.length).toBe(3);
  });
});