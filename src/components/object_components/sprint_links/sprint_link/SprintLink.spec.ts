import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {SprintLink} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("SprintLink", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders sprint title and dates", async () => {
    const sprint = {
      id: "1",
      title: "Sprint 1",
      requirement: [],
      project: [],
      total_story_points: 10,
      completed_story_points: 5,
      status: "active",
      start_date: "2023-10-01T00:00:00Z",
      end_date: "2023-10-15T00:00:00Z",
    };

    const wrapper = mount(SprintLink, {
      props: {
        index: 0,
        sprint: sprint,
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Check sprint title
    const sprintTitle = wrapper.find(".sprint-title a");
    expect(sprintTitle.text()).toBe("Sprint 1");

    // Check sprint dates
    const sprintDates = wrapper.find(".sprint-dates");
    expect(sprintDates.text()).toBe("2023-10-01 - 2023-10-15");
  });

  test("emits deleteSprint event when trash icon is clicked", async () => {
    const sprint = {
      id: "1",
      title: "Sprint 1",
      requirement: [],
      project: [],
      total_story_points: 10,
      completed_story_points: 5,
      status: "active",
      start_date: "2023-10-01T00:00:00Z",
      end_date: "2023-10-15T00:00:00Z",
    };

    const wrapper = mount(SprintLink, {
      props: {
        index: 0,
        sprint: sprint,
      },
    });

    // Flush all promises
    await flushPromises();
    await nextTick();

    // Click on the trash icon
    const trashIcon = wrapper.findComponent(TrashIcon);
    await trashIcon.trigger("click");

    // Check if deleteSprint event is emitted
    expect(wrapper.emitted()).toHaveProperty("deleteSprint");
    expect(wrapper.emitted()["deleteSprint"]).toEqual([["1"]]);
  });
});