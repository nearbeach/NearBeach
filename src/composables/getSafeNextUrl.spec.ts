import { describe, expect, test } from "vitest";
import { getSafeNextUrl } from "./getSafeNextUrl.ts";

describe("getSafeNextUrl", () => {
  test.each([
    ["/", "/"],
    ["/project/1/", "/project/1/"],
    ["/project/1/?tab=notes#top", "/project/1/?tab=notes#top"],
  ])("lets the local path %s through", (next, expected) => {
    expect(getSafeNextUrl(next)).toBe(expected);
  });

  test("falls back to the home page when there is no next", () => {
    expect(getSafeNextUrl(null)).toBe("/");
    expect(getSafeNextUrl("")).toBe("/");
  });

  test.each([
    ["javascript:alert(1)"],
    ["JaVaScRiPt:alert(1)"],
    ["data:text/html,<script>alert(1)</script>"],
    ["https://evil.example.com/"],
    ["http://evil.example.com/"],
    ["//evil.example.com/"],
    ["/\\evil.example.com/"],
    ["/\t/evil.example.com/"],
    ["/\n/evil.example.com/"],
    ["evil.example.com"],
    ["project/1/"],
    [" /project/1/"],
  ])("sends %j to the home page", (next) => {
    expect(getSafeNextUrl(next)).toBe("/");
  });
});
