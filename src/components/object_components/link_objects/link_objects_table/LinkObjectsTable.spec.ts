import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {LinkObjectsTable} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import i18n from "@/i18n.ts";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

describe("LinkObjectsTable", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders object links", async () => {
    const objectLinkList = [
      {
        object_assignment_id: 1,
        object_id: 101,
        object_title: "Object 1",
        object_status: "Active",
        object_type: "Type 1",
        parent_link: "Parent 1",
        link_relationship: "Relationship 1",
        reverse_relation: false,
      },
      {
        object_assignment_id: 2,
        object_id: 102,
        object_title: "Object 2",
        object_status: "Inactive",
        object_type: "Type 2",
        parent_link: "Parent 2",
        link_relationship: "Relationship 2",
        reverse_relation: true,
      },
    ];

    const wrapper = mount(LinkObjectsTable, {
      props: {
        objectLinkList,
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const linkObjects = wrapper.findAll(".link-object");
    expect(linkObjects.length).toBe(objectLinkList.length);

    linkObjects.forEach((linkObject, index) => {
      const title = linkObject.find("h4").text();
      const status = linkObject.find("p").text();
      expect(title).toBe(objectLinkList[index].object_title);
      expect(status).toBe(objectLinkList[index].object_status);
    });
  });

  test("emits deleteObjectLink event", async () => {
    const objectLinkList = [
      {
        object_assignment_id: 1,
        object_id: 101,
        object_title: "Object 1",
        object_status: "Active",
        object_type: "Type 1",
        parent_link: "Parent 1",
        link_relationship: "Relationship 1",
        reverse_relation: false,
      },
    ];

    const wrapper = mount(LinkObjectsTable, {
      props: {
        objectLinkList,
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const deleteButton = wrapper.find(".link-object .delete-button");
    await deleteButton.trigger("click");

    await flushPromises();
    await nextTick();

    expect(wrapper.emitted().deleteObjectLink).toBeTruthy();
    expect(wrapper.emitted().deleteObjectLink[0]).toEqual([1]);
  });

  test("renders create message when showCreate is true", async () => {
    const wrapper = mount(LinkObjectsTable, {
      props: {
        showCreate: true,
        objectLinkList: [],
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const createMessage = wrapper.find(".create-message");
    expect(createMessage.exists()).toBe(true);
    expect(createMessage.text()).toBe("Create new object");
  });

  test("renders error message when errorMessage is provided", async () => {
    const wrapper = mount(LinkObjectsTable, {
      props: {
        errorMessage: "An error occurred",
        objectLinkList: [],
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const errorMessage = wrapper.find(".error-message");
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.text()).toBe("An error occurred");
  });

  test("renders loading message when isLoading is true", async () => {
    const wrapper = mount(LinkObjectsTable, {
      props: {
        isLoading: true,
        objectLinkList: [],
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const loadingMessage = wrapper.find(".loading-message");
    expect(loadingMessage.exists()).toBe(true);
    expect(loadingMessage.text()).toBe("Loading...");
  });
});