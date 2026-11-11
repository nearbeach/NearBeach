import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import { flushPromises, mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import { WlkButton, WlkTextInput } from "whelk-ui";
import { useErrorStore } from "@/stores/error/error.ts";
import i18n from "@/i18n.ts";
import NewOrganisation from "./NewOrganisation.vue";

const { pushMock } = vi.hoisted(() => ({ pushMock: vi.fn() }));
vi.mock("@/router/router.ts", () => ({ default: { push: pushMock } }));

function mockFetch(status: number, body: unknown = {}, statusText = "") {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue({
    status,
    statusText,
    json: () => Promise.resolve(body),
  } as Response);
}

function mountForm() {
  return mount(NewOrganisation, { global: { plugins: [i18n] } });
}

// Fills the name, website and email inputs (in that order) and marks them valid
function fillForm(wrapper: ReturnType<typeof mountForm>) {
  const [name, website, email] = wrapper.findAllComponents(WlkTextInput);
  name.vm.$emit("update:modelValue", "Acme");
  website.vm.$emit("update:modelValue", "https://acme.example.com");
  email.vm.$emit("update:modelValue", "hello@acme.example.com");
  for (const input of [name, website, email]) {
    input.vm.$emit("change", { isValid: true });
  }
}

describe("NewOrganisation", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    pushMock.mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("renders the heading and three inputs", () => {
    const wrapper = mountForm();

    expect(wrapper.find("h1").text()).toBe("Create your new Organisation");
    expect(wrapper.findAllComponents(WlkTextInput)).toHaveLength(3);
  });

  test("the create button is disabled until every field is valid", async () => {
    const wrapper = mountForm();
    const button = wrapper.findComponent(WlkButton);
    expect(button.attributes("disabled")).toBeDefined();

    const inputs = wrapper.findAllComponents(WlkTextInput);
    inputs[0].vm.$emit("change", { isValid: true });
    inputs[1].vm.$emit("change", { isValid: true });
    await wrapper.vm.$nextTick();
    expect(button.attributes("disabled")).toBeDefined();

    inputs[2].vm.$emit("change", { isValid: true });
    await wrapper.vm.$nextTick();
    expect(button.attributes("disabled")).toBeUndefined();
  });

  test("an invalid field disables the button again", async () => {
    const wrapper = mountForm();
    fillForm(wrapper);
    await wrapper.vm.$nextTick();

    wrapper.findAllComponents(WlkTextInput)[0].vm.$emit("change", { isValid: false });
    await wrapper.vm.$nextTick();

    expect(wrapper.findComponent(WlkButton).attributes("disabled")).toBeDefined();
  });

  test("each input reports validity for its own field", async () => {
    const wrapper = mountForm();
    const inputs = wrapper.findAllComponents(WlkTextInput);
    const button = wrapper.findComponent(WlkButton);
    inputs[0].vm.$emit("change", { isValid: true });
    inputs[1].vm.$emit("change", { isValid: true });
    inputs[2].vm.$emit("change", { isValid: true });

    // Only the email is invalid - the button must stay disabled even though the website is valid
    inputs[2].vm.$emit("change", { isValid: false });
    await wrapper.vm.$nextTick();
    expect(button.attributes("disabled")).toBeDefined();

    // Fixing the email alone re-enables it
    inputs[2].vm.$emit("change", { isValid: true });
    await wrapper.vm.$nextTick();
    expect(button.attributes("disabled")).toBeUndefined();
  });

  test("creating posts the details and redirects to the new organisation", async () => {
    const fetchSpy = mockFetch(201, { id: 14 });
    const wrapper = mountForm();
    fillForm(wrapper);
    await wrapper.vm.$nextTick();

    await wrapper.findComponent(WlkButton).trigger("click");
    await flushPromises();

    expect(fetchSpy.mock.calls[0][0]).toBe("/api/v1/organisation/");
    expect(fetchSpy.mock.calls[0][1]?.method).toBe("POST");
    expect(JSON.parse(fetchSpy.mock.calls[0][1]?.body as string)).toEqual({
      name: "Acme",
      website: "https://acme.example.com",
      email: "hello@acme.example.com",
    });
    expect(pushMock).toHaveBeenCalledWith("/organisation/14/");
  });

  test("a 403 redirects to the forbidden page", async () => {
    mockFetch(403);
    const wrapper = mountForm();
    fillForm(wrapper);
    await wrapper.vm.$nextTick();

    await wrapper.findComponent(WlkButton).trigger("click");
    await flushPromises();

    expect(pushMock).toHaveBeenCalledWith({ name: "forbidden" });
  });

  test("any other failure records the error and redirects to the server error page", async () => {
    mockFetch(500, {}, "Internal Server Error");
    const wrapper = mountForm();
    fillForm(wrapper);
    await wrapper.vm.$nextTick();

    await wrapper.findComponent(WlkButton).trigger("click");
    await flushPromises();

    expect(useErrorStore().message).toBe("Internal Server Error");
    expect(pushMock).toHaveBeenCalledWith({ name: "server-error" });
  });
});
