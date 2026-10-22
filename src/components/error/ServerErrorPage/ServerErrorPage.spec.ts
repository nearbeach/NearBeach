import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import ServerErrorPage from "./ServerErrorPage.vue";
import { useErrorStore } from "@/stores/error/error.ts";

describe("ServerErrorPage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders the server error message", async () => {
    const errorStore = useErrorStore();
    errorStore.message = "Something went wrong!";

    const wrapper = mount(ServerErrorPage, {});

    await flushPromises();

    const errorMessage = wrapper.find("p");
    expect(errorMessage.text()).toBe("Something went wrong!");
  });

  test("displays the correct title", async () => {
    const wrapper = mount(ServerErrorPage, {});

    await flushPromises();

    const title = wrapper.find("#main-title");
    expect(title.text()).toBe("Server Error");
  });
});