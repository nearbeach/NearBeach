import { beforeEach, describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { defineComponent, h } from "vue";
import { useObjectStore } from "@/stores/object/object.ts";
import i18n from "@/i18n.ts";
import AssociatedCustomers from "./AssociatedCustomers.vue";
import CustomerList from "./customer_list/CustomerList.vue";
import {WlkButton} from "whelk-ui";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

const RouterLinkStub = defineComponent({
  props: ["to"],
  setup: (props, { slots }) => () => h("a", { href: props.to }, slots.default?.()),
});

describe("AssociatedCustomers", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    useObjectStore().id = 7;
    usePermissionStore().currentObjectPermissions.currentObject = 2;
  });

  test("shows the customer list", () => {
    const wrapper = mount(AssociatedCustomers, {
      global: { plugins: [i18n], stubs: { CustomerList: true, RouterLink: RouterLinkStub } },
    });

    expect(wrapper.findComponent(CustomerList).exists()).toBe(true);
  });

  test("links to the new customer page of the current organisation", () => {
    const wrapper = mount(AssociatedCustomers, {
      global: {
        plugins: [i18n],
        stubs: {
          CustomerList: true,
          RouterLink: RouterLinkStub
        }
        },
    });

    // List item goes to correct place
    expect(wrapper.find("a").attributes("href")).toBe("/organisation/7/customer/new/");
    // const dashboardItem = wrapper.findAllComponents(NavMenuItem).at(0);
    // expect(wrapper.find("button").text()).toBe("Create Customer");

    // Create button exists
    const createButton = wrapper.findAllComponents(WlkButton).at(0);
    expect(createButton?.text()).toBe("Create Customer");
  });
});
