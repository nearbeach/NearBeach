import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {LinkObjectsTable} from ".";
import RelationshipLink from "@/components/object_components/link_objects/relationship_link/RelationshipLink.vue";
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

    // The delete control is the trash icon
    const deleteButton = wrapper.find(".link-object .link-object-delete svg");
    await deleteButton.trigger("click");

    await flushPromises();
    await nextTick();

    expect(wrapper.emitted().deleteObjectLink).toBeTruthy();
    expect(wrapper.emitted().deleteObjectLink[0]).toEqual([{ object_assignment_id: 1, index: 0 }]);
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

    const createMessage = wrapper.find(".link-create");
    expect(createMessage.exists()).toBe(true);
    expect(createMessage.text()).toBe("Please wait - creating object link");
  });

  test("renders error message when errorText is provided", async () => {
    const wrapper = mount(LinkObjectsTable, {
      props: {
        errorText: "An error occurred",
        objectLinkList: [],
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const errorMessage = wrapper.find(".link-error");
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.find("h4").text()).toBe("Error");
    expect(errorMessage.text()).toContain("An error occurred");
  });

  test("renders no create or error rows by default", async () => {
    const wrapper = mount(LinkObjectsTable, {
      props: {
        objectLinkList: [],
      },
      global: {
        plugins: [router, i18n],
      },
    });

    await flushPromises();
    await nextTick();

    expect(wrapper.find(".link-create").exists()).toBe(false);
    expect(wrapper.find(".link-error").exists()).toBe(false);
    expect(wrapper.findAll(".link-object").length).toBe(0);
  });

  test("passes updateRelationship through with the payload unwrapped", async () => {
    const wrapper = mount(LinkObjectsTable, {
      props: {
        objectLinkList: [
          {
            object_assignment_id: 1,
            object_id: 101,
            object_title: "Object 1",
            object_status: "Active",
            object_type: "task",
            parent_link: "Parent 1",
            link_relationship: "relates",
            reverse_relation: false,
          },
        ],
      },
      global: {
        plugins: [router, i18n],
      },
    });

    wrapper.findComponent(RelationshipLink).vm.$emit("updateRelationship", {
      index: 0,
      link_relationship: "blocking",
    });
    await nextTick();

    expect(wrapper.emitted().updateRelationship).toEqual([
      [{ index: 0, link_relationship: "blocking" }],
    ]);
  });
});
