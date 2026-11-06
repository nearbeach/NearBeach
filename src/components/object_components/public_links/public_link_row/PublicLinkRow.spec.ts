import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import i18n from "@/i18n.ts";
import { createPinia, setActivePinia } from "pinia";
import { usePermissionStore } from "@/stores/permissions/permission.ts";
import { PublicLinkRow } from ".";

function mountRow(props = {}) {
  return mount(PublicLinkRow, {
    props: { id: "abc-123", isActive: true, index: 2, ...props },
    global: { plugins: [i18n] },
    // The component renders <td>s, so give it a valid parent
    attachTo: document.body.appendChild(
      document.createElement("tr"),
    ),
  });
}

describe("PublicLinkRow", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    usePermissionStore().currentObjectPermissions.currentObject = 2;
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  test("renders the link id", () => {
    const wrapper = mountRow();

    expect(wrapper.find(".link").text()).toBe("abc-123");
    expect(wrapper.findAll("td")).toHaveLength(3);
  });

  test("copies the public url to the clipboard and shows the status", async () => {
    vi.useFakeTimers();
    const writeText = vi.fn().mockResolvedValue(undefined);
    vi.spyOn(navigator.clipboard, "writeText").mockImplementation(writeText);

    const wrapper = mountRow();
    await wrapper.findAll("td")[0].trigger("click");
    await flushPromises();

    expect(writeText).toHaveBeenCalledWith(
      `${window.location.origin}/public_link/abc-123/`,
    );
    expect(wrapper.find(".copied-status").exists()).toBe(true);
    expect(wrapper.find(".link").exists()).toBe(false);

    // The status disappears after twenty seconds
    vi.advanceTimersByTime(20000);
    await wrapper.vm.$nextTick();

    expect(wrapper.find(".copied-status").exists()).toBe(false);
    expect(wrapper.find(".link").exists()).toBe(true);
  });

  test("shows an error status when the copy fails", async () => {
    vi.spyOn(navigator.clipboard, "writeText").mockRejectedValue(
      new Error("denied"),
    );

    const wrapper = mountRow();
    await wrapper.findAll("td")[0].trigger("click");
    await flushPromises();

    const status = wrapper.find(".copied-status");
    expect(status.classes()).toContain("error");
    expect(status.text()).toContain("denied");
  });

  test("emits updateActive with the id and index", async () => {
    const wrapper = mountRow();

    await wrapper.findAll("td")[1].trigger("click");

    expect(wrapper.emitted("updateActive")).toEqual([
      [{ id: "abc-123", index: 2 }],
    ]);
  });

  test("emits deleteLink with the id", async () => {
    const wrapper = mountRow();

    await wrapper.findAll("td")[2].trigger("click");

    expect(wrapper.emitted("deleteLink")).toEqual([[{ id: "abc-123" }]]);
  });

  test.each([true, false])("renders the active icon for isActive=%s", (isActive) => {
    const wrapper = mountRow({ isActive });

    expect(wrapper.findAll("td")[1].find("svg").exists()).toBe(true);
  });
});
