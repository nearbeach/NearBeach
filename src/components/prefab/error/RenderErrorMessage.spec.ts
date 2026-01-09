// RenderErrorMessage.spec.ts
import { describe, test, expect } from "vitest";
import { render } from "vitest-browser-vue";
import RenderErrorMessage from "./RenderErrorMessage.vue";
import { mount } from "@vue/test-utils";

describe("RenderErrorMessage", async () => {
  test("Renders the error message", async () => {
    const { getByText } = render(RenderErrorMessage, {
      props: {
        errorMessage: "Unknown Error",
      },
    });

    await expect.element(getByText("Unknown Error")).toBeInTheDocument();
  });

  test("Renders different error message", async () => {
    const { getByText } = render(RenderErrorMessage, {
      props: {
        errorMessage: "Different Error Message",
      },
    });

    // Test for positives
    await expect
      .element(getByText("Different Error Message"))
      .toBeInTheDocument();

    // Test for negatives
    await expect.element(getByText("Unknown Error")).not.toBeInTheDocument();
  });

  test("Throws an error message when missing required props", async () => {
    expect(() => mount(RenderErrorMessage)).toThrow();
  });
});
