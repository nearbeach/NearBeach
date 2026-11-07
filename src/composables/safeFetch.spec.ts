import { afterEach, describe, expect, test, vi } from "vitest";
import { safeFetch } from "./safeFetch.ts";

describe("safeFetch", () => {
    afterEach(() => {
        vi.restoreAllMocks();
    });

    test("passes the arguments through and returns the response", async () => {
        const response = new Response("{}", { status: 200 });
        const fetchSpy = vi.spyOn(globalThis, "fetch").mockResolvedValue(response);

        const result = await safeFetch("/api/test/", { method: "POST" });

        expect(result).toBe(response);
        expect(fetchSpy).toHaveBeenCalledWith("/api/test/", { method: "POST" });
    });

    test("turns a network failure into a 503 carrying the error message", async () => {
        vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("offline"));

        const result = await safeFetch("/api/test/");

        expect(result.status).toBe(503);
        expect(result.statusText).toBe("offline");
    });

    test("handles a non-Error rejection and strips line breaks", async () => {
        vi.spyOn(globalThis, "fetch").mockRejectedValue("bad\nthing");

        const result = await safeFetch("/api/test/");

        expect(result.status).toBe(503);
        expect(result.statusText).toBe("bad thing");
    });
});
