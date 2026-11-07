import { afterEach, describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";
import { SsoPanel } from ".";
import i18n from "@/i18n.ts";

const providers = [
  { name: "Keycloak", slug: "keycloak", login_url: "/api/v1/authentication/oidc/keycloak/login/" },
  { name: "Google", slug: "google", login_url: "/api/v1/authentication/oidc/google/login/" },
];

function mountPanel(props: { providers: typeof providers }) {
  return mount(SsoPanel, { props, global: { plugins: [i18n] } });
}

describe("SsoPanel", () => {
  afterEach(() => {
    globalThis.history.replaceState({}, "", "/");
  });

  test("renders nothing when there are no providers", () => {
    const wrapper = mountPanel({ providers: [] });
    expect(wrapper.find(".sso-panel").exists()).toBe(false);
  });

  test("renders a link for each provider", () => {
    const wrapper = mountPanel({ providers });
    const links = wrapper.findAll("a.sso-button");

    expect(links).toHaveLength(2);
    expect(links[0].text()).toBe("Sign in with Keycloak");
    expect(links[0].attributes("href")).toBe("/api/v1/authentication/oidc/keycloak/login/");
    expect(links[1].text()).toBe("Sign in with Google");
  });

  test("passes the next page on to the provider login", () => {
    globalThis.history.replaceState({}, "", "/login/?next=/project/1/");
    const wrapper = mountPanel({ providers });

    expect(wrapper.find("a.sso-button").attributes("href")).toBe(
      "/api/v1/authentication/oidc/keycloak/login/?next=%2Fproject%2F1%2F",
    );
  });
});
