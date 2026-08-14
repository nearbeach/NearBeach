import { describe, expect, test } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import ErrorComponent from "./ErrorComponent.vue";

const defaultProps = {
  title: "Something went wrong",
  message: "Please try again later.",
};

describe("ErrorComponent", () => {
  test("mounting component", () => {
    expect(ErrorComponent).toBeTruthy();
  });

  test("renders the supplied title", async () => {
    const wrapper = mount(ErrorComponent, {
      props: defaultProps,
    });

    await flushPromises();

    const heading = wrapper.find("h1");
    expect(heading.exists()).toBe(true);
    expect(heading.text()).toBe(defaultProps.title);

    wrapper.unmount();
  });

  test("renders the supplied message", async () => {
    const wrapper = mount(ErrorComponent, {
      props: defaultProps,
    });

    await flushPromises();

    const message = wrapper.find("p");
    expect(message.exists()).toBe(true);
    expect(message.text()).toBe(defaultProps.message);

    wrapper.unmount();
  });

  test("adds the error-component class to the card", async () => {
    const wrapper = mount(ErrorComponent, {
      props: defaultProps,
    });

    await flushPromises();

    const error_component = wrapper.find(".error-component");
    expect(error_component.exists()).toBe(true);

    wrapper.unmount();
  });
});

describe("ErrorComponent - A11Y checks", () => {
  test("main title exists on page", async () => {
    const wrapper = mount(ErrorComponent, {
      props: defaultProps,
    });

    await flushPromises();

    const h1_elements = wrapper.findAll("h1");
    const main_title_elements = wrapper.findAll("#main-title");

    expect(h1_elements.length).toBe(1);
    expect(main_title_elements.length).toBe(1);

    wrapper.unmount();
  });

  test("main title contains text", async () => {
    const wrapper = mount(ErrorComponent, {
      props: defaultProps,
    });

    await flushPromises();

    const main_title = wrapper.find("#main-title");
    expect(main_title.text()).not.toBe("");

    wrapper.unmount();
  });
});
