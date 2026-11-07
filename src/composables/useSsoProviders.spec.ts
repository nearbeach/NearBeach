import { afterEach, describe, expect, test, vi } from "vitest";
import { useSsoProviders } from "./useSsoProviders.ts";

const provider = { name: "Keycloak", slug: "keycloak", login_url: "/api/v1/authentication/oidc/keycloak/login/" };

describe("useSsoProviders", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("loads the providers from the api", async () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: () => Promise.resolve([provider]),
    } as Response);

    const { providers, loadProviders } = useSsoProviders();
    await loadProviders();

    expect(fetchSpy).toHaveBeenCalledWith("/api/v1/authentication/oidc/providers/");
    expect(providers.value).toEqual([provider]);
  });

  test("has no providers when the api fails", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({ status: 500 } as Response);

    const { providers, loadProviders } = useSsoProviders();
    await loadProviders();

    expect(providers.value).toEqual([]);
  });

  test("has no providers when the request throws", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));

    const { providers, loadProviders } = useSsoProviders();
    await loadProviders();

    expect(providers.value).toEqual([]);
  });

  test("ignores a response that is not a list", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      status: 200,
      json: () => Promise.resolve({ status: "default" }),
    } as Response);

    const { providers, loadProviders } = useSsoProviders();
    await loadProviders();

    expect(providers.value).toEqual([]);
  });
});
