import { afterEach, beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { page } from "vitest/browser";
import {LoginImage} from ".";
import { createPinia, setActivePinia } from "pinia";
import { nextTick } from "vue";

// The image is hidden with a CSS media query (--medium-screen, 768px and up),
// so resize the real browser viewport and attach to the document so the
// scoped styles apply
async function mountAtWidth(width: number) {
  await page.viewport(width, 900);

  const wrapper = mount(LoginImage, {
    attachTo: document.body,
  });

  // Flush all promises
  await flushPromises();
  await nextTick();

  return wrapper;
}

describe("LoginImage", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  afterEach(async () => {
    // Restore the default viewport for the other tests
    await page.viewport(414, 896);
  });

  test("image is not displayed on small screens", async () => {
    const wrapper = await mountAtWidth(640);

    // Check that the login image is not visible
    const loginImage = wrapper.find(".login-image");
    expect(loginImage.isVisible()).toBe(false);

    wrapper.unmount();
  });

  test("image is displayed on medium screens", async () => {
    const wrapper = await mountAtWidth(1440);

    // Check that the login image is visible
    const loginImage = wrapper.find(".login-image");
    expect(loginImage.isVisible()).toBe(true);

    wrapper.unmount();
  });
});
