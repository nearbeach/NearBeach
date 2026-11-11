import { describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import ProfilePicture from "./ProfilePicture.vue";

describe("ProfilePicture", () => {
  test("shows the image when a url is given", () => {
    const wrapper = mount(ProfilePicture, { props: { url: "/media/luke.png", name: "Luke" } });

    const img = wrapper.find("img");
    expect(img.attributes("src")).toBe("/media/luke.png");
    expect(img.attributes("alt")).toBe("Luke's profile picture");
    expect(wrapper.find(".no-profile-picture").exists()).toBe(false);
  });

  test.each([[""], [null]])("shows the placeholder when the url is %s", (url) => {
    const wrapper = mount(ProfilePicture, { props: { url, name: "Luke" } });

    expect(wrapper.find(".no-profile-picture").exists()).toBe(true);
    expect(wrapper.find("img").exists()).toBe(false);
  });

  test.each([[undefined], [""]])("falls back to a generic alt text when the name is %s", (name) => {
    const wrapper = mount(ProfilePicture, { props: { url: "/media/luke.png", name } });

    expect(wrapper.find("img").attributes("alt")).toBe("Profile Picture");
  });
});
